import xlsxwriter
from vue.models import Experiment, PostStudyData, PreStudyData, TrainingData, Data
from django.core.exceptions import ObjectDoesNotExist
from io import BytesIO
import os

class Results():
    def createGeneralOverview(self, workbook):
        worksheet = workbook.add_worksheet('General data')
        #Header
        worksheet.write('A1', 'ID')
        worksheet.write('B1', 'group')
        worksheet.write('C1', 'order')
        worksheet.write('D1', 'Demographic data')
        worksheet.write('D2', 'Gender')
        worksheet.write('E2', 'Age')
        worksheet.write('F2', 'Experience')
        worksheet.write('G2', 'Interest in tech')
        worksheet.write('H2', 'Adoption of new tech')
        worksheet.write('I2', 'Familiarity with tech')
        worksheet.write('J1', 'Baseline')
        worksheet.write('J2', 'status')
        worksheet.write('K2', 't0-est')
        worksheet.write('L2', 't1-est')
        worksheet.write('M2', 'item1')
        worksheet.write('N2', 'item2')
        worksheet.write('O2', 'item3')
        worksheet.write('P2', 'item4')
        worksheet.write('Q2', 'item5')
        worksheet.write('R2', 'item6')
        worksheet.write('S2', 'item7')
        worksheet.write('T2', 'item8')
        worksheet.write('U1', 'XAI')
        worksheet.write('U2', 'status')
        worksheet.write('V2', 't0-est')
        worksheet.write('W2', 't1-est')
        worksheet.write('X2', 'item1')
        worksheet.write('Y2', 'item2')
        worksheet.write('Z2', 'item3')
        worksheet.write('AA2', 'item4')
        worksheet.write('AB2', 'item5')
        worksheet.write('AC2', 'item6')
        worksheet.write('AD2', 'item7')
        worksheet.write('AE2', 'item8')
        #data
        expList = Experiment.objects.all()
        i = 2
        for exp in expList:
            worksheet.write(i, 0, exp.email)
            worksheet.write(i, 1, exp.group)
            worksheet.write(i, 2, exp.order.slide_order)
            try:
                prestudyData = PreStudyData.objects.get(experiment=exp)
                worksheet.write(i, 3, prestudyData.gender)
                worksheet.write(i, 4, prestudyData.age)
                worksheet.write(i, 5, prestudyData.experience)
                worksheet.write(i, 6, prestudyData.interest_in_tech)
                worksheet.write(i, 7, prestudyData.adoption_of_new_tech)
                worksheet.write(i, 8, prestudyData.familiarity_with_AI)
                #Baseline data
                worksheet.write(i, 9, exp.statusBaseline)
                trainingData0 = TrainingData.objects.get(experiment=exp, condition='Baseline', slide='0')
                worksheet.write(i, 10, trainingData0.tcp_est)
                trainingData1 = TrainingData.objects.get(experiment=exp, condition='Baseline', slide='1')
                worksheet.write(i, 11 , trainingData1.tcp_est)
                poststudyData = PostStudyData.objects.get(experiment=exp, condition='Baseline')
                worksheet.write(i, 12, poststudyData.item1)
                worksheet.write(i, 13, poststudyData.item2)
                worksheet.write(i, 14, poststudyData.item3)
                worksheet.write(i, 15, poststudyData.item4)
                worksheet.write(i, 16, poststudyData.item5)
                worksheet.write(i, 17, poststudyData.item6)
                worksheet.write(i, 18, poststudyData.item7)
                worksheet.write(i, 19, poststudyData.item8)
                #XAI data
                worksheet.write(i, 20, exp.statusXAI)
                trainingData0 = TrainingData.objects.get(experiment=exp, condition='XAI', slide='0')
                worksheet.write(i, 21, trainingData0.tcp_est)
                trainingData1 = TrainingData.objects.get(experiment=exp, condition='XAI', slide='1')
                worksheet.write(i, 22, trainingData1.tcp_est)
                poststudyData = PostStudyData.objects.get(experiment=exp, condition='XAI')
                worksheet.write(i, 23, poststudyData.item1)
                worksheet.write(i, 24, poststudyData.item2)
                worksheet.write(i, 25, poststudyData.item3)
                worksheet.write(i, 26, poststudyData.item4)
                worksheet.write(i, 27, poststudyData.item5)
                worksheet.write(i, 28, poststudyData.item6)
                worksheet.write(i, 29, poststudyData.item7)
                worksheet.write(i, 30, poststudyData.item8)
            except ObjectDoesNotExist:
                print ("ups")
            i = i + 1
    
    def createConsistenError(self, workbook, condition):
        worksheet = workbook.add_worksheet('Consistent Error '+ condition)
        #Header
        worksheet.write(0, 0, 'ID')
        slide_names = ['slide1', 'slide2', 'slide3', 'slide4', 'slide5', 'slide6', 'slide7', 'slide8', 'slide9', 'slide10', 'slide11', 'slide12', 'slide13', 'slide14', 'slide15', 'slide16', 'slide17', 'slide18']
        for col_num, data in enumerate(slide_names):
            worksheet.write(0, col_num+1, data)
        worksheet.write(0, 19, 'consistent error')
        worksheet.write(0,20, 'label')
        #Data
        expList = Experiment.objects.all()
        i = 1
        for exp in expList:
            worksheet.write(i, 0, exp.email)
            try:
                data = Data.objects.filter(experiment=exp, condition=condition)
                for col_num, entry in enumerate(data):
                    worksheet.write(i, col_num+1, entry.tcp_est)
            except ObjectDoesNotExist:
                print ("ups in consisten Error" + condition)
            i = i + 1

    def exportResults(self):
        if os.path.isfile('../results.xlsx'):
           os.remove('../results.xlsx') 
        workbook = xlsxwriter.Workbook('results.xlsx')
        self.createGeneralOverview(workbook)
        self.createConsistenError(workbook,'Baseline')
        self.createConsistenError(workbook,'XAI')
        workbook.close()
