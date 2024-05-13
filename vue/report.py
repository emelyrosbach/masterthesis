import numpy as np 
import matplotlib.pyplot as plt
from vue.models import Experiment, Data
from vue.predictions import GroundTruth
from django.core.exceptions import ObjectDoesNotExist
import os
import pandas as pd
import fpdf as FPDF

class Report():
    def createGraphics (self):
        df = pd.DataFrame()
        df[""]=["Independent assessment", "With xAI assistance"]
        df['AI minimal estimation error'] = ["3.6","7.66"]
        df['AI substantial estimation error'] = ["1.40","14.25"]

        performanceBaseline = self.prepareData('Baseline')
        performanceXAI = self.prepareData('XAI')
        expList = Experiment.objects.all()
        for exp in expList:
            newBaseline = {}
            newXAI = {}
            i=1
            for participant in performanceBaseline:
                if participant == exp.email:
                    newBaseline["you"] = performanceBaseline[participant]
                    newXAI["you"] = performanceXAI[participant]
                else:
                    newBaseline[str(i)] = performanceBaseline[participant]
                    newXAI[str(i)] = performanceXAI[participant]
                i = i + 1
            
            exclude = ['test@bla.de','marc.aubreville@thi.de','chloe.puget@fu-berlin.de','vk.ca@gmail.com', 'm.c.e.polderdijk@umcutrecht.nl', 'christof.bertram@vetmeduni.ac.at']
            #if exp.statusBaseline == 'completed' and exp.statusXAI=='completed'and exp.email not in exclude:
            if exp.email == 'p.j.vandiest@umcutrecht.nl':
                emailList = list(newBaseline.keys())
                baseline = list(newBaseline.values())
                xAI = list(newXAI.values())
                plt.figure(figsize=(35, 7), dpi=80)
                n=len(emailList)
                r = np.arange(n)
                width = 0.3
                bar1 = plt.bar(r, baseline, color = '#FFE6E9', width = width, edgecolor = '#FFE6E9', label='independent assesment') 
                bar2 = plt.bar(r + width, xAI, color = '#DBEEFF', width = width, edgecolor = '#DBEEFF', label='with xAI assistance')
                for rect in bar1 + bar2:
                    height = rect.get_height()
                    x = rect.get_x() + rect.get_width() / 2.0
                    plt.text (x, height,f'{height:.1f}', ha='center', va='bottom')
                plt.xlabel("Participant number") 
                plt.ylabel("Absolute mean deviation from the ground truth") 
                plt.title("Participant performance with and without aid from an explainable AI")
                plt.xticks(r + width/2,emailList)
                legend = plt.legend()
                legend.get_frame().set_linewidth(0.0)
                plt.rcParams.update({'font.size': 22})
               
                
                filename = './plots/' + exp.email + '.pdf'
                if os.path.isfile(filename):
                    os.remove(filename) 
                plt.savefig(filename)
                plt.close() 

    def prepareData(self, condition):
        performance = {}
        exclude = ['test@bla.de','marc.aubreville@thi.de','chloe.puget@fu-berlin.de','vk.ca@gmail.com', 'm.c.e.polderdijk@umcutrecht.nl', 'christof.bertram@vetmeduni.ac.at']
        expList = Experiment.objects.all()
        for exp in expList:
            if exp.statusBaseline == 'completed' and exp.statusXAI=='completed' and exp.email not in exclude:
                try:
                    slides = [10,11,12,13,14,15,16,17,18,19,20,21,22,24,23,25,26,27,28,29]
                    sumDev = 0
                    for col_num in range(len(slides)):
                        data = Data.objects.get(experiment=exp, condition=condition, slide=slides[col_num])
                        sumDev = sumDev + self.calcDeviation(data.slide, data.tcp_est)
                    sysDev = sumDev / 20
                    performance[exp.email] = abs(sysDev)
                except ObjectDoesNotExist:
                    print("ups")
        return performance

    def calcDeviation (self, slide, tcpEst):
            gt = GroundTruth.getGroundTruth(slide)
            deviation = float(tcpEst)-float(gt)
            return deviation
        
        

                
        
        



        
    
                    
                    
        
    
        
    