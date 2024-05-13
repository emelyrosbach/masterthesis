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
        worksheet.write('M2', 't2-est')
        worksheet.write('N2', 'item1')
        worksheet.write('O2', 'item2')
        worksheet.write('P2', 'item3')
        worksheet.write('Q2', 'item4')
        worksheet.write('R2', 'item5')
        worksheet.write('S2', 'item6')
        worksheet.write('T2', 'item7')
        worksheet.write('U2', 'item8')
        worksheet.write('V1', 'XAI')
        worksheet.write('V2', 'status')
        worksheet.write('W2', 't0-est')
        worksheet.write('X2', 't1-est')
        worksheet.write('Y2', 'item1')
        worksheet.write('Z2', 'item2')
        worksheet.write('AA2', 'item3')
        worksheet.write('AB2', 'item4')
        worksheet.write('AC2', 'item5')
        worksheet.write('AD2', 'item6')
        worksheet.write('AE2', 'item7')
        worksheet.write('AF2', 'item8')
        worksheet.write('AG2', 'question1')
        worksheet.write('AH2', 'question2')
        worksheet.write('AI2', 'question3')
        worksheet.write('AJ2', 'question4')
        worksheet.write('AK2', 'question5')
        worksheet.write('AL2', 'question6')
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
                trainingData2 = TrainingData.objects.get(experiment=exp, condition='Baseline', slide='2')
                worksheet.write(i, 12 , trainingData2.tcp_est)
                poststudyData = PostStudyData.objects.get(experiment=exp, condition='Baseline')
                worksheet.write(i, 13, poststudyData.item1)
                worksheet.write(i, 14, poststudyData.item2)
                worksheet.write(i, 15, poststudyData.item3)
                worksheet.write(i, 16, poststudyData.item4)
                worksheet.write(i, 17, poststudyData.item5)
                worksheet.write(i, 18, poststudyData.item6)
                worksheet.write(i, 19, poststudyData.item7)
                worksheet.write(i, 20, poststudyData.item8)
                #XAI data
                worksheet.write(i, 21, exp.statusXAI)
                trainingData0 = TrainingData.objects.get(experiment=exp, condition='XAI', slide='0')
                worksheet.write(i, 22, trainingData0.tcp_est)
                trainingData1 = TrainingData.objects.get(experiment=exp, condition='XAI', slide='1')
                worksheet.write(i, 23, trainingData1.tcp_est)
                trainingData2 = TrainingData.objects.get(experiment=exp, condition='XAI', slide='2')
                worksheet.write(i, 24, trainingData2.tcp_est)
                poststudyData = PostStudyData.objects.get(experiment=exp, condition='XAI')
                worksheet.write(i, 25, poststudyData.item1)
                worksheet.write(i, 26, poststudyData.item2)
                worksheet.write(i, 27, poststudyData.item3)
                worksheet.write(i, 28, poststudyData.item4)
                worksheet.write(i, 29, poststudyData.item5)
                worksheet.write(i, 30, poststudyData.item6)
                worksheet.write(i, 31, poststudyData.item7)
                worksheet.write(i, 32, poststudyData.item8)
                worksheet.write(i, 33, poststudyData.question1)
                worksheet.write(i, 34, poststudyData.question2)
                worksheet.write(i, 35, poststudyData.question3)
                worksheet.write(i, 36, poststudyData.question4)
                worksheet.write(i, 37, poststudyData.question5)
                worksheet.write(i, 38, poststudyData.question6)
            except ObjectDoesNotExist:
                print ("")
            i = i + 1
    
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

    def consistenErrorConditions(self, workbook, condition):
        worksheetNoTP = workbook.add_worksheet('Consistent Error '+ condition+ '-NoTP')
        worksheetTP = workbook.add_worksheet('Consistent Error '+ condition+ '-TP')
        worksheetConfNoTP = workbook.add_worksheet('Confidence Error '+ condition+ '-NoTP')
        worksheetConfTP = workbook.add_worksheet('Confidence Error '+ condition+ '-TP')
        #Headers
        worksheetNoTP.write(0, 0, 'ID')
        worksheetTP.write(0, 0, 'ID')
        worksheetConfNoTP.write(0, 0, 'ID')
        worksheetConfTP.write(0, 0, 'ID')
        slide_names = ['slide1', 'slide2', 'slide3', 'slide4', 'slide5', 'slide6', 'slide7', 'slide8', 'slide9', 'slide10']
        for col_num, data in enumerate(slide_names):
            worksheetNoTP.write(0, col_num+1, data)
            worksheetTP.write(0, col_num+1, data)
            worksheetConfNoTP.write(0, col_num+1, data)
            worksheetConfTP.write(0, col_num+1, data)
        worksheetNoTP.write(0, 11, 'consistent error')
        worksheetTP.write(0, 11, 'consistent error')
        worksheetConfNoTP.write(0, 11, 'avg confidence')
        worksheetConfTP.write(0, 11, 'avg confidence')
        worksheetNoTP.write(0,12, 'label')
        worksheetTP.write(0,12, 'label')
        #Data
        expList = Experiment.objects.all()
        i = 1
        for exp in expList:
            worksheetNoTP.write(i, 0, exp.email)
            worksheetTP.write(i, 0, exp.email)
            worksheetConfNoTP.write(i, 0, exp.email)
            worksheetConfTP.write(i, 0, exp.email)
            try:
                slideList = exp.order.slide_order.split(",")
                firstSplit = slideList[:len(slideList)//2]
                secondSplit = slideList[len(slideList)//2:]
                sumNoTP = 0
                sumTP = 0
                sumConfNoTP = 0.
                sumConfTP = 0.
                sumConf = 0.
                for col_num,slide in enumerate(firstSplit):
                    #print(exp.email + " " + condition + " " + slide + " " + str(Data.objects.get(experiment=exp, condition=condition, slide=firstSplit[col_num])))
                    dataFirst = Data.objects.get(experiment=exp, condition=condition, slide=firstSplit[col_num]) 
                    dataSecond = Data.objects.get(experiment=exp, condition=condition, slide=secondSplit[col_num])
                    if (exp.group == 'A' or exp.group== 'B'):
                        #starts with the TP condition
                        worksheetNoTP.write(i, col_num+1, dataSecond.tcp_est)
                        worksheetTP.write(i, col_num+1, dataFirst.tcp_est)
                        worksheetConfNoTP.write(i, col_num+1, dataSecond.confidence_score)
                        worksheetConfTP.write(i, col_num+1, dataFirst.confidence_score)
                        sumNoTP = sumNoTP + self.calcDeviation(dataSecond.slide, dataSecond.tcp_est)
                        sumTP = sumTP+  self.calcDeviation(dataFirst.slide, dataFirst.tcp_est)
                        sumConfNoTP = sumConfNoTP + int(dataSecond.confidence_score)
                        sumConfTP = sumConfTP + int(dataFirst.confidence_score)
                        sumConf = sumConf + int(dataFirst.confidence_score)
                        sumConf = sumConf + int(dataSecond.confidence_score)
                    else:
                        #starts with the noTP condition
                        worksheetNoTP.write(i, col_num+1, dataFirst.tcp_est)
                        worksheetTP.write(i, col_num+1, dataSecond.tcp_est)
                        worksheetConfNoTP.write(i, col_num+1, dataFirst.confidence_score)
                        worksheetConfTP.write(i, col_num+1, dataSecond.confidence_score)
                        sumNoTP = sumNoTP + self.calcDeviation(dataFirst.slide, dataFirst.tcp_est)
                        sumTP = sumTP+  self.calcDeviation(dataSecond.slide, dataSecond.tcp_est)
                        sumConfNoTP = sumConfNoTP + int(dataFirst.confidence_score)
                        sumConfTP = sumConfTP + int(dataSecond.confidence_score)
                        sumConf = sumConf + int(dataFirst.confidence_score)
                        sumConf = sumConf + int(dataSecond.confidence_score)
                meanNoTP = sumNoTP / 10
                meanTP = sumTP / 10
                meanConfNoTP = sumConfNoTP /10
                meanConfTP = sumConfTP / 10
                meanConf = sumConf / 20
                worksheetNoTP.write(i, 11, meanNoTP)
                worksheetTP.write(i, 11, meanTP)
                worksheetConfNoTP.write(i, 11, meanConfNoTP)
                worksheetConfNoTP.write(i, 12, meanConf)
                worksheetConfTP.write(i, 11, meanConfTP)
                #value to be changed later
                labelNoTP = ''
                if meanNoTP < -1:
                    labelNoTP = 'underestimation'
                elif meanNoTP > 1:
                    labelNoTP = 'overestimation'
                else:
                    labelNoTP = 'no tendency'
                worksheetNoTP.write(i, 12, labelNoTP)
                labelTP = ''
                if meanTP < -1:
                    labelTP = 'underestimation'
                elif meanTP > 1:
                    labelTP = 'overestimation'
                else:
                    labelTP = 'no tendency'
                worksheetTP.write(i, 12, labelTP)
            except ObjectDoesNotExist:
                print ("")
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
        worksheetJAS.write(0, 2, 'AI-no-deviation')
        worksheetErr.write(0, 2, 'AI-no-deviation')
        worksheetAn.write(0, 2, 'AI-no-deviation')
        worksheet3.write(0, 2, 'AI-no-deviation')
        worksheetJAS.write(0, 3, 'AI-overestimation')
        worksheetErr.write(0, 3, 'AI-overestimation')
        worksheetAn.write(0, 3, 'AI-overestimation')
        worksheet3.write(0, 3, 'AI-overestimation')
        #Data
        expList = Experiment.objects.all()
        i = 1
        for exp in expList:
            worksheetJAS.write(i, 0, exp.email)
            worksheetErr.write(i, 0, exp.email)
            worksheetAn.write(i, 0, exp.email)
            worksheet3.write((i*2)-1, 0, exp.email)
            underestimation = [10,12,16,21,23]
            overestimation = [14,15,24,25,27]
            nothing = [11,13,17,18,19,20,22,26,28,29]
            sumUnder = 0
            sumNothing = 0
            sumOver = 0
            sumJASUnder = 0
            sumJASNothing = 0
            sumJASOver = 0
            sumAnUnder = 0
            sumAnNothing = 0
            sumAnOver = 0
            sumBUnder = 0
            sumBNothing = 0
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
                # for nothing
                for col_num in range(len(nothing)):
                    dataNothing = Data.objects.get(experiment=exp, condition='XAI', slide=nothing[col_num])
                    #Baseline data for JAS
                    dataNothingBaseline = Data.objects.get(experiment=exp, condition='Baseline', slide=nothing[col_num])
                    #consist error
                    sumNothing = sumNothing + self.calcDeviation(dataNothing.slide, dataNothing.tcp_est)
                    #JAS
                    sumJASNothing = sumJASNothing + self.calcJAS(dataNothing.slide, dataNothingBaseline.tcp_est, dataNothing.tcp_est)
                    #An
                    sumAnNothing = sumAnNothing + self.calcAn(dataNothing.slide, dataNothing.tcp_est)
                    #3groups
                    sumBNothing = sumBNothing + self.calcDeviation(dataNothing.slide, dataNothingBaseline.tcp_est)
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
                meanUnder = sumUnder / 5
                meanNothing = sumNothing / 10
                meanOver = sumOver / 5
                meanJASUnder = sumJASUnder / 5
                meanJASNothing = sumJASNothing/ 10
                meanJASOver = sumJASOver / 5
                meanAnUnder = sumAnUnder / 5
                meanAnNothing = sumAnNothing / 10
                meanAnOver = sumAnOver/ 5
                meanBUnder = sumBUnder / 5
                meanBNothing = sumBNothing / 10
                meanBOver = sumBOver / 5
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
    
    def avgConfidence(self, workbook):
        worksheetConf3 = workbook.add_worksheet('confidence')
        #Headers
        worksheetConf3.write(0, 0, 'ID')
        worksheetConf3.write(0, 1, 'AI-underestimation')
        worksheetConf3.write(0, 2, 'AI-nothing')
        worksheetConf3.write(0, 3, 'AI-overestimation')
        #Data
        expList = Experiment.objects.all()
        i = 1
        for exp in expList:
            worksheetConf3.write((i*2)-1, 0, exp.email)
            underestimation = [10,12,16,21,23]
            overestimation = [14,15,24,25,27]
            nothing = [11,13,17,18,19,20,22,26,28,29]
            sumConfUnder = 0
            sumConfNothing = 0
            sumConfOver = 0
            sumConfUnderB = 0
            sumConfNothingB = 0
            sumConfOverB = 0
            try:
                #for underestimation (5 entries)
                for col_num in range(len(underestimation)):
                    dataUnderestimation = Data.objects.get(experiment=exp, condition='XAI', slide=underestimation[col_num]) 
                    dataUnderestimationBaseline = Data.objects.get(experiment=exp, condition='Baseline', slide=underestimation[col_num])
                    #confidence
                    sumConfUnder = sumConfUnder + int(dataUnderestimation.confidence_score)
                    sumConfUnderB = sumConfUnderB + int(dataUnderestimationBaseline.confidence_score)
                # for nothing
                for col_num in range(len(nothing)):
                    dataNothing = Data.objects.get(experiment=exp, condition='XAI', slide=nothing[col_num])
                    dataNothingBaseline = Data.objects.get(experiment=exp, condition='Baseline', slide=nothing[col_num])
                    #confidence
                    sumConfNothing = sumConfNothing + int(dataNothing.confidence_score)
                    sumConfNothingB = sumConfNothingB + int(dataNothingBaseline.confidence_score)
                for col_num in range(len(overestimation)):
                    dataOverestimation = Data.objects.get(experiment=exp, condition='XAI', slide=overestimation[col_num])
                    dataOverestimationBaseline = Data.objects.get(experiment=exp, condition='Baseline', slide=overestimation[col_num])
                    #confidence
                    sumConfOver = sumConfOver + int(dataOverestimation.confidence_score)
                    sumConfOverB = sumConfOverB + int(dataOverestimationBaseline.confidence_score)
                meanConfUnder = sumConfUnder / 5
                meanConfNothing = sumConfNothing / 10
                meanConfOver = sumConfOver / 5
                meanConfUnderB = sumConfUnderB / 5
                meanConfNothingB = sumConfNothingB / 10
                meanConfOverB = sumConfOverB / 5
                worksheetConf3.write((i*2)-1, 1, meanConfUnderB)
                worksheetConf3.write((i*2)-1, 2, meanConfNothingB)
                worksheetConf3.write((i*2)-1, 3, meanConfOverB)
                worksheetConf3.write((i*2), 1, meanConfUnder)
                worksheetConf3.write((i*2), 2, meanConfNothing)
                worksheetConf3.write((i*2), 3, meanConfOver)
            except ObjectDoesNotExist:
                print ("ups in comp to AI")
            i = i + 1

    def JASXAI(self, workbook):
        worksheetJASNoTP = workbook.add_worksheet('JAS-XAI-noTP')
        worksheetJASTP = workbook.add_worksheet('JAS-XAI-TP')
        #Headers
        worksheetJASNoTP.write(0, 0, 'ID')
        worksheetJASTP.write(0, 0, 'ID')
        slide_names = ['slide1', 'slide2', 'slide3', 'slide4', 'slide5', 'slide6', 'slide7', 'slide8', 'slide9', 'slide10']
        for col_num, data in enumerate(slide_names):
            worksheetJASNoTP.write(0, col_num+1, data)
            worksheetJASTP.write(0, col_num+1, data)
        worksheetJASNoTP.write(0, 11, 'avg JAS')
        worksheetJASTP.write(0, 11, 'avgJAS')
        #Data
        expList = Experiment.objects.all()
        i = 1
        for exp in expList:
            worksheetJASNoTP.write(i, 0, exp.email)
            worksheetJASTP.write(i, 0, exp.email)
            try:
                slideList = exp.order.slide_order.split(",")
                firstSplit = slideList[:len(slideList)//2]
                secondSplit = slideList[len(slideList)//2:]
                sumJASNoTP = 0
                sumJASTP = 0
                for col_num,slide in enumerate(firstSplit):
                    dataFirst = Data.objects.get(experiment=exp, condition='XAI', slide=firstSplit[col_num]) 
                    dataSecond = Data.objects.get(experiment=exp, condition='XAI', slide=secondSplit[col_num])
                    dataFirstB = Data.objects.get(experiment=exp, condition='Baseline', slide=firstSplit[col_num]) 
                    dataSecondB = Data.objects.get(experiment=exp, condition='Baseline', slide=secondSplit[col_num])
                    if (exp.group == 'A' or exp.group== 'B'):
                        #starts with the TP condition
                        #JAS
                        JASFirst = self.calcJAS(dataFirst.slide, dataFirstB.tcp_est, dataFirst.tcp_est)
                        JASSceond = self.calcJAS(dataSecond.slide, dataSecondB.tcp_est, dataSecond.tcp_est)
                        worksheetJASNoTP.write(i, col_num+1, JASSceond)
                        worksheetJASTP.write(i, col_num+1, JASFirst)
                        sumJASNoTP = sumJASNoTP + JASSceond
                        sumJASTP = sumJASTP + JASFirst
                    else:
                        #starts with the noTP condition
                        JASFirst = self.calcJAS(dataFirst.slide, dataFirstB.tcp_est, dataFirst.tcp_est)
                        JASSceond = self.calcJAS(dataSecond.slide, dataSecondB.tcp_est, dataSecond.tcp_est)
                        worksheetJASNoTP.write(i, col_num+1, JASFirst)
                        worksheetJASTP.write(i, col_num+1, JASSceond)
                        sumJASNoTP = sumJASNoTP + JASFirst
                        sumJASTP = sumJASTP + JASSceond
                meanJASNoTP = sumJASNoTP / 10
                meanJASTP = sumJASTP / 10
                worksheetJASNoTP.write(i, 11, meanJASNoTP)
                worksheetJASTP.write(i, 11, meanJASTP)
            except ObjectDoesNotExist:
                print ("")
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
        self.createGeneralOverview(workbook)
        self.createConsistentError(workbook,'Baseline')
        self.createConsistentError(workbook,'XAI')
        self.consistenErrorConditions(workbook,'Baseline')
        self.consistenErrorConditions(workbook,'XAI')
        self.compareToAI(workbook)
        self.avgConfidence(workbook)
        self.JASXAI(workbook)
        workbook.close()