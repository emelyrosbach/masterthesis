import xlsxwriter
from vue.models import Experiment, PostStudyData, PreStudyData, TrainingData, Data
from django.core.exceptions import ObjectDoesNotExist
from io import BytesIO
import os
from vue.predictions import GroundTruth, AIPredictions

class Results():
    def createConsistentError(self, workbook, condition):
        worksheet = workbook.add_worksheet('Consistent Error '+ condition)
        #Headers
        worksheet.write(0, 0, 'ID')
        slide_names = ['slide1', 'slide2', 'slide3', 'slide4', 'slide5', 'slide6', 'slide7', 'slide8', 'slide9', 'slide10', 'slide11', 'slide12', 'slide13', 'slide14', 'slide15', 'slide16', 'slide17', 'slide18', 'slide19', 'slide20']
        for col_num, data in enumerate(slide_names):
            worksheet.write(0, col_num+1, data)
        worksheet.write(0, 21, 'consistent error')
        worksheet.write(0,22, 'label')
        #Data
        expList = Experiment.objects.all()
        i = 1
        for exp in expList:
            worksheet.write(i, 0, exp.email)
            try:
                slides = [10,11,12,13,14,15,16,17,18,19,20,21,22,24,23,25,26,27,28,29]
                sum = 0
                for col_num in range(len(slides)):
                    data = Data.objects.get(experiment=exp, condition=condition, slide=slides[col_num]) 
                    worksheet.write(i, col_num+1, data.tcp_est)
                    sum = sum + self.calcDeviation(data.slide, data.tcp_est)
                mean = sum / 20
                worksheet.write(i, 21, mean)
                #value to be changed later
                label = ''
                if mean < 0:
                    label = 'underestimation'
                elif mean > 0:
                    label = 'overestimation'
                else:
                    label = 'no tendency'
                worksheet.write(i, 22, label)
            except ObjectDoesNotExist:
                print ("ups in consisten Error" + condition)
            i = i + 1

    def compareToAI(self, workbook):
        worksheetJAS = workbook.add_worksheet('JAS')
        worksheetErr = workbook.add_worksheet('Consistent Error AI')
        worksheetAn = workbook.add_worksheet('Anchoring')
        worksheet3 = workbook.add_worksheet('3groups')
        #Headers
        worksheetJAS.write(0, 0, 'ID')
        worksheetErr.write(0, 0, 'ID')
        worksheetAn.write(0, 0, 'ID')
        worksheet3.write(0, 0, 'ID')
        worksheetJAS.write(0, 1, 'AI-underestimation')
        worksheetErr.write(0, 1, 'AI-underestimation')
        worksheetAn.write(0, 1, 'AI-underestimation')
        worksheet3.write(0, 1, 'AI-underestimation')
        worksheetJAS.write(0, 2, 'AI-overestimation')
        worksheetErr.write(0, 2, 'AI-overestimation')
        worksheetAn.write(0, 2, 'AI-overestimation')
        worksheet3.write(0, 2, 'AI-overestimation')
        #Data
        expList = Experiment.objects.all()
        i = 1
        for exp in expList:
            worksheetJAS.write(i, 0, exp.email)
            worksheetErr.write(i, 0, exp.email)
            worksheetAn.write(i, 0, exp.email)
            worksheet3.write((i*2)-1, 0, exp.email)
            underestimation = [10,12,16,21,23,29,22,20]
            overestimation = [14,15,24,25,27,28,19,17,13,18,11,16]
            sumUnder = 0
            sumOver = 0
            sumJASUnder = 0
            sumJASOver = 0
            sumAnUnder = 0
            sumAnOver = 0
            sumBUnder = 0
            sumBOver = 0
            try:
                #for underestimation (5 entries)
                for col_num in range(len(underestimation)):
                    dataUnderestimation = Data.objects.get(experiment=exp, condition='XAI', slide=underestimation[col_num]) 
                    #Baseline data for JAS
                    dataUnderestimationBaseline = Data.objects.get(experiment=exp, condition='Baseline', slide=underestimation[col_num]) 
                    #consist error
                    sumUnder = sumUnder + self.calcDeviation(dataUnderestimation.slide, dataUnderestimation.tcp_est)
                    #JAS
                    sumJASUnder = sumJASUnder + self.calcJAS(dataUnderestimation.slide, dataUnderestimationBaseline.tcp_est, dataUnderestimation.tcp_est)
                    #An
                    sumAnUnder = sumAnUnder + self.calcAn(dataUnderestimation.slide, dataUnderestimation.tcp_est)
                    #3groups
                    sumBUnder = sumBUnder + self.calcDeviation(dataUnderestimation.slide, dataUnderestimationBaseline.tcp_est)
                for col_num in range(len(overestimation)):
                    dataOverestimation = Data.objects.get(experiment=exp, condition='XAI', slide=overestimation[col_num])
                    #Baseline data for JAS
                    dataOverestimationBaseline = Data.objects.get(experiment=exp, condition='Baseline', slide=overestimation[col_num])
                    #consist error
                    sumOver = sumOver + self.calcDeviation(dataOverestimation.slide, dataOverestimation.tcp_est)
                    #JAS
                    sumJASOver = sumJASOver + self.calcJAS(dataOverestimation.slide, dataOverestimationBaseline.tcp_est, dataOverestimation.tcp_est)
                    #An
                    sumAnOver = sumAnOver + self.calcAn(dataOverestimation.slide, dataOverestimation.tcp_est)
                    #3groups
                    sumBOver = sumBOver + self.calcDeviation(dataOverestimation.slide, dataOverestimationBaseline.tcp_est)
                meanUnder = sumUnder / 8
                meanOver = sumOver / 12
                meanJASUnder = sumJASUnder / 8
                meanJASOver = sumJASOver / 12
                meanAnUnder = sumAnUnder / 8
                meanAnOver = sumAnOver/ 12
                meanBUnder = sumBUnder / 8
                meanBOver = sumBOver / 12
                worksheetErr.write(i, 1, meanUnder)
                worksheetErr.write(i, 2, meanOver)
                worksheetJAS.write(i, 1, meanJASUnder)
                worksheetJAS.write(i, 2, meanJASOver)
                worksheetAn.write(i, 1, meanAnUnder)
                worksheetAn.write(i, 2, meanAnOver)
                worksheet3.write((i*2)-1, 1, meanBUnder)
                worksheet3.write((i*2)-1, 2, meanBOver)
                worksheet3.write((i*2), 1, meanUnder)
                worksheet3.write((i*2), 2, meanOver)
            except ObjectDoesNotExist:
                print ("ups in comp to AI")
            i = i + 1

    def calcDeviation (self, slide, tcpEst):
        gt = GroundTruth.getGroundTruth(slide)
        deviation = float(tcpEst)-float(gt)
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
            jas = 1
        return jas
    
    def calcAn (self, slide, tcpXAI):
        aiPRed= AIPredictions.getAIPredictions()
        prediction = float(aiPRed.get(slide))
        xai = float(tcpXAI)
        an = abs(xai - prediction)
        return an

    def exportResults(self):
        if os.path.isfile('../results.xlsx'):
           os.remove('../results.xlsx') 
        workbook = xlsxwriter.Workbook('results.xlsx')
        self.createConsistentError(workbook,'Baseline')
        self.createConsistentError(workbook,'XAI')
        self.compareToAI(workbook)
        workbook.close()