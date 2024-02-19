import xlsxwriter
from vue.models import Experiment, PostStudyData, PreStudyData, TrainingData, Data
from django.core.exceptions import ObjectDoesNotExist
from io import BytesIO
import os
from vue.predictions import GroundTruth, AIPredictions

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
    
    def createConsistentError(self, workbook, condition):
        worksheet = workbook.add_worksheet('Consistent Error '+ condition)
        #Headers
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
                sum = 0
                for col_num, entry in enumerate(data):
                    worksheet.write(i, col_num+1, entry.tcp_est)
                    sum = sum + self.calcDeviation(entry.slide, entry.tcp_est)
                mean = sum / 18
                worksheet.write(i, 19, mean)
                #value to be changed later
                label = ''
                if mean < -1:
                    label = 'underestimation'
                elif mean > 1:
                    label = 'overestimation'
                else:
                    label = 'no tendency'
                worksheet.write(i, 20, label)
            except ObjectDoesNotExist:
                print ("ups in consisten Error" + condition)
            i = i + 1

    def consistenErrorConditions(self, workbook, condition):
        worksheetNoTP = workbook.add_worksheet('Consistent Error '+ condition+ '-NoTP')
        worksheetTP = workbook.add_worksheet('Consistent Error '+ condition+ '-TP')
        #Headers
        worksheetNoTP.write(0, 0, 'ID')
        worksheetTP.write(0, 0, 'ID')
        slide_names = ['slide1', 'slide2', 'slide3', 'slide4', 'slide5', 'slide6', 'slide7', 'slide8', 'slide9']
        for col_num, data in enumerate(slide_names):
            worksheetNoTP.write(0, col_num+1, data)
            worksheetTP.write(0, col_num+1, data)
        worksheetNoTP.write(0, 10, 'consistent error')
        worksheetTP.write(0, 10, 'consistent error')
        worksheetNoTP.write(0,11, 'label')
        worksheetTP.write(0,11, 'label')
        #Data
        expList = Experiment.objects.all()
        i = 1
        for exp in expList:
            worksheetNoTP.write(i, 0, exp.email)
            worksheetTP.write(i, 0, exp.email)
            try:
                slideList = exp.order.slide_order.split(",")
                firstSplit = slideList[:len(slideList)//2]
                secondSplit = slideList[len(slideList)//2:]
                sumNoTP = 0
                sumTP = 0
                for col_num,slide in enumerate(firstSplit):
                    dataFirst = Data.objects.get(experiment=exp, condition=condition, slide=firstSplit[col_num]) 
                    dataSecond = Data.objects.get(experiment=exp, condition=condition, slide=secondSplit[col_num])
                    if (exp.group == 'A' or exp.group== 'B'):
                        #starts with the TP condition
                        worksheetNoTP.write(i, col_num+1, dataSecond.tcp_est)
                        worksheetTP.write(i, col_num+1, dataFirst.tcp_est)
                        sumNoTP = sumNoTP + self.calcDeviation(dataSecond.slide, dataSecond.tcp_est)
                        sumTP = sumTP+  self.calcDeviation(dataFirst.slide, dataFirst.tcp_est)
                    else:
                        #starts with the noTP condition
                        worksheetNoTP.write(i, col_num+1, dataFirst.tcp_est)
                        worksheetTP.write(i, col_num+1, dataSecond.tcp_est)
                        sumNoTP = sumNoTP + self.calcDeviation(dataFirst.slide, dataFirst.tcp_est)
                        sumTP = sumTP+  self.calcDeviation(dataSecond.slide, dataSecond.tcp_est)
                meanNoTP = sumNoTP / 9
                meanTP = sumTP / 9
                worksheetNoTP.write(i, 10, meanNoTP)
                worksheetTP.write(i, 10, meanTP)
                #value to be changed later
                labelNoTP = ''
                if meanNoTP < -1:
                    labelNoTP = 'underestimation'
                elif meanNoTP > 1:
                    labelNoTP = 'overestimation'
                else:
                    labelNoTP = 'no tendency'
                worksheetNoTP.write(i, 11, labelNoTP)
                labelTP = ''
                if meanTP < -1:
                    labelTP = 'underestimation'
                elif meanTP > 1:
                    labelTP = 'overestimation'
                else:
                    labelTP = 'no tendency'
                worksheetTP.write(i, 11, labelTP)
            except ObjectDoesNotExist:
                print ("ups in filling conditions with data")
            i = i + 1
    
    def compareToAI(self, workbook):
        worksheetJAS = workbook.add_worksheet('JAS')
        worksheetErr = workbook.add_worksheet('Consistent Error AI')
        #Headers
        worksheetJAS.write(0, 0, 'ID')
        worksheetErr.write(0, 0, 'ID')
        worksheetJAS.write(0, 1, 'AI-underestimation')
        worksheetErr.write(0, 1, 'AI-underestimation')
        worksheetJAS.write(0, 2, 'AI-no-deviation')
        worksheetErr.write(0, 2, 'AI-no-deviation')
        worksheetJAS.write(0, 3, 'AI-overestimation')
        worksheetErr.write(0, 3, 'AI-overestimation')
        #Data
        expList = Experiment.objects.all()
        i = 1
        for exp in expList:
            worksheetJAS.write(i, 0, exp.email)
            worksheetErr.write(i, 0, exp.email)
            underestimation = [10,12,17,21,23,28]
            overestimation = [14,15,16,24,25,26]
            nothing = [11,13,18,20,22,27]
            sumUnder = 0
            sumNothing = 0
            sumOver = 0
            sumJASUnder = 0
            sumJASNothing = 0
            sumJASOver = 0
            try:
                data = Data.objects.filter(experiment=exp, condition='XAI')
                for col_num,slide in enumerate(underestimation):
                    dataUnderestimation = Data.objects.get(experiment=exp, condition='XAI', slide=underestimation[col_num]) 
                    dataNothing = Data.objects.get(experiment=exp, condition='XAI', slide=nothing[col_num])
                    dataOverestimation = Data.objects.get(experiment=exp, condition='XAI', slide=overestimation[col_num])
                    #Baseline data for JAS
                    dataUnderestimationBaseline = Data.objects.get(experiment=exp, condition='Baseline', slide=underestimation[col_num]) 
                    dataNothingBaseline = Data.objects.get(experiment=exp, condition='Baseline', slide=nothing[col_num])
                    dataOverestimationBaseline = Data.objects.get(experiment=exp, condition='Baseline', slide=overestimation[col_num])
                    #consist error
                    sumUnder = sumUnder + self.calcDeviation(dataUnderestimation.slide, dataUnderestimation.tcp_est)
                    sumNothing = sumNothing + self.calcDeviation(dataNothing.slide, dataNothing.tcp_est)
                    sumOver = sumOver + self.calcDeviation(dataOverestimation.slide, dataOverestimation.tcp_est)
                    #JAS
                    sumJASUnder = sumJASUnder + self.calcJAS(dataUnderestimation.slide, dataUnderestimationBaseline.tcp_est, dataUnderestimation.tcp_est)
                    sumJASNothing = sumJASNothing + self.calcJAS(dataNothing.slide, dataNothingBaseline.tcp_est, dataNothing.tcp_est)
                    sumJASOver = sumJASOver + self.calcJAS(dataOverestimation.slide, dataOverestimationBaseline.tcp_est, dataOverestimation.tcp_est)
                meanUnder = sumUnder / 6
                meanNothing = sumNothing / 6
                meanOver = sumOver / 6
                meanJASUnder = sumJASUnder / 6
                meanJASNothing = sumJASNothing/ 6
                meanJASOver = sumJASOver / 6
                worksheetErr.write(i, 1, meanUnder)
                worksheetErr.write(i, 2, meanNothing)
                worksheetErr.write(i, 3, meanOver)
                worksheetJAS.write(i, 1, meanJASUnder)
                worksheetJAS.write(i, 2, meanJASNothing)
                worksheetJAS.write(i, 3, meanJASOver)
            except ObjectDoesNotExist:
                print ("ups in comp to AI")
            i = i + 1

    def calcDeviation (self, slide, tcpEst):
        gt = GroundTruth.getGroundTruth(slide)
        deviation = float(tcpEst)-gt
        return deviation
     
    def calcJAS (self, slide, tcpBaseline, tcpXAI):
        aiPRed= AIPredictions.getAIPredictions()
        prediction = float(aiPRed.get(slide))
        xai = float(tcpXAI)
        baseline = float(tcpBaseline)
        jas = None
        try:
            jas = abs(xai-baseline)/(abs(xai-prediction)+abs(xai-baseline))
        except ZeroDivisionError:
            #xai=baselien=prediction
            jas = 0
        return jas

    def exportResults(self):
        if os.path.isfile('../results.xlsx'):
           os.remove('../results.xlsx') 
        workbook = xlsxwriter.Workbook('results.xlsx')
        self.createGeneralOverview(workbook)
        self.createConsistentError(workbook,'Baseline')
        self.createConsistentError(workbook,'XAI')
        self.consistenErrorConditions(workbook,'Baseline')
        self.consistenErrorConditions(workbook,'XAI')
        self.compareToAI(workbook)
        workbook.close()
