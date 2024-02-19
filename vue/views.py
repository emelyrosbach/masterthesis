from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from vue.predictions import AIPredictions, TrainingAIPredictions
from vue.results import Results
from vue.models import Experiment, Order, Data, PostStudyData, PreStudyData, TrainingData
from vue.forms import Registration, PreStudy, PostStudy, Confidence
import json
import csv
import time

def startingpageBaseline(request):
    if request.user_agent.is_mobile:
        return redirect('mobile')
    else:
        if request.method =='POST':
            form = Registration(request.POST)
            if form.is_valid():
                form_email = form.cleaned_data["email"]
                try:
                    currentExp = Experiment.objects.get(email=form_email)
                except ObjectDoesNotExist:
                    currentExp = Experiment.objects.create()
                    group = ""
                    match int(currentExp.participant_id)%4:
                        case 1:
                            group = "A"
                        case 2:
                            group = "B"
                        case 3:
                            group = "C"
                        case 0:
                            group = "D"
                        case _:
                            print("we should not get here")
                    currentExp.group = group
                    #assign slide order
                    order_nr = currentExp.participant_id%10
                    if order_nr == 0:
                        order_nr = 10
                    currentExp.order = Order.objects.get(pk=order_nr)
                    currentExp.email = form_email
                    currentExp.save()
                #log to csv
                currentExp = Experiment.objects.get(email=form_email)
                row = [time.ctime(), currentExp.email, 'Baseline', 'register', 'status:' + currentExp.statusBaseline]    
                with open('log.csv', 'a') as f:
                    w = csv.writer(f)
                    w.writerow(row)
                return redirect('training', currentExp.participant_id, 'Baseline', 0, 0)
        else:
            form = Registration()
        return render(request, 'startingpageBaseline.html', {'form': form})

def startingpageXAI(request):
    if request.user_agent.is_mobile:
        return redirect('mobile')
    else:
        if request.method =='POST':
            form = Registration(request.POST)
            if form.is_valid():
                form_email = form.cleaned_data["email"]
                try:
                    currentExp = Experiment.objects.get(email=form_email)
                except ObjectDoesNotExist:
                    currentExp = Experiment.objects.create()
                    group = ""
                    match int(currentExp.participant_id)%4:
                        case 1:
                            group = "A"
                        case 2:
                            group = "B"
                        case 3:
                            group = "C"
                        case 0:
                            group = "D"
                        case _:
                            print("we should not get here")
                    currentExp.group = group
                    #assign slide order
                    order_nr = currentExp.participant_id%10
                    if order_nr == 0:
                        order_nr = 10
                    currentExp.order = Order.objects.get(pk=order_nr)
                    currentExp.email = form_email
                    currentExp.save()
                #log to csv
                currentExp = Experiment.objects.get(email=form_email)
                row = [time.ctime(), currentExp.email, 'XAI', 'register', 'status:' + currentExp.statusBaseline]    
                with open('log.csv', 'a') as f:
                    w = csv.writer(f)
                    w.writerow(row)
                return redirect('training', currentExp.participant_id, 'XAI', 0, 0)
        else:
            form = Registration()
        return render(request, 'startingpageXAI.html', {'form': form})

def training(request, participant_id, condition, timer_active, slide_counter):
    currentExp = Experiment.objects.get(pk=participant_id)
    if request.method =='POST':
        content = json.loads(request.body)
        tcpEst = content['tcp_est']
        trainingData = None
        try:
            trainingData = TrainingData.objects.get(experiment=currentExp, condition=condition, slide=slide_counter-1)
        except ObjectDoesNotExist:
            trainingData = TrainingData.objects.create()
            trainingData.experiment = currentExp
            trainingData.condition = condition
            trainingData.slide = slide_counter-1
        trainingData.tcp_est = tcpEst
        trainingData.save()
        #log to csv
        row = [time.ctime(), currentExp.email, condition, 'training', 'TCP estimation for slide ' + str(trainingData.slide) + ': ' + tcpEst]    
        with open('log.csv', 'a') as f:
            w = csv.writer(f)
            w.writerow(row)
        if slide_counter==2:
            return redirect('startexperiment', participant_id, condition)
        else:
            return redirect('training', participant_id, condition, timer_active, slide_counter)
    else:
        predictions = TrainingAIPredictions.getTrainingAIPredictions()
        tumorCells= TrainingAIPredictions.getTrainingAITumorCellCount()
        totalCells= TrainingAIPredictions.getTrainingAITotalCellCount()
        context = {
            'id': currentExp.participant_id,
            'condition': condition,
            'showTimer' : timer_active,
            'slideCounter' : slide_counter,
            'predictions': predictions,
            'tumorCells': tumorCells,
            'totalCells': totalCells
        }
        return render(request, 'training.html', context)
    
def experiment(request, participant_id, condition, timer_active, slide_counter):
    currentExp = Experiment.objects.get(pk=participant_id)
    slide_list = currentExp.order.slide_order.split(",")
    if request.method =='POST':
        content = json.loads(request.body)
        tcpEst = content['tcp_est']
        taskTime = content['task_time']
        expData = None
        try:
            expData = Data.objects.get(experiment=currentExp, condition=condition, slide=slide_list[slide_counter-1])
        except ObjectDoesNotExist:
            expData = Data.objects.create()
            expData.experiment = currentExp
            expData.condition = condition
            expData.slide = slide_list[slide_counter-1]
        expData.tcp_est = tcpEst
        expData.save()
        #log to csv
        row = [time.ctime(), currentExp.email, condition, 'experiment', 'TCP estimation for slide ' + str(expData.slide) + ': ' + tcpEst + ' with timerActive = ' + str(timer_active)]    
        with open('log.csv', 'a') as f:
            w = csv.writer(f)
            w.writerow(row)
        #log time
        rowTime = [currentExp.email, condition, slide_list[slide_counter-1], timer_active, taskTime]    
        with open('timeLog.csv', 'a') as f:
            x = csv.writer(f)
            x.writerow(rowTime)
        return redirect('confidence', participant_id, condition, timer_active, slide_counter)
    else:
        predictions = AIPredictions.getAIPredictions()
        tumorCells= AIPredictions.getAITumorCellCount()
        totalCells= AIPredictions.getAITotalCellCount()
        context = {
            'id': currentExp.participant_id,
            'group':currentExp.group,
            'slides' : slide_list,
            'condition' : condition,
            'slideCounter' : slide_counter,
            'predictions': predictions,
            'tumorCells': tumorCells,
            'totalCells': totalCells
        }
        if slide_counter == 0:
            show_timer = None
            if currentExp.group=='A' or currentExp.group=='B':
                show_timer = 1
            else:
                show_timer = 0
            context['showTimer'] = show_timer
        else:
            context['showTimer'] = timer_active
        return render(request, 'experiment.html', context)
  

def confidence(request, participant_id, condition, timer_active, slide_counter):
    currentExp = Experiment.objects.get(pk=participant_id)
    slide_list = currentExp.order.slide_order.split(",")
    if request.method =='POST':
        form = Confidence(request.POST)
        if form.is_valid():
            form_likertScale = form.cleaned_data["likertScale"]
            expData = None
            try:
                expData = Data.objects.get(experiment=currentExp, condition=condition, slide=slide_list[slide_counter-1])
            except ObjectDoesNotExist:
                expData = Data.objects.create()
                expData.experiment = currentExp
                expData.condition = condition
                expData.slide = slide_list[slide_counter-1]
            expData.confidence_score = form_likertScale
            expData.save()
            #log to csv
            row = [time.ctime(), currentExp.email, condition, 'confidence', 'confidence for slide ' + str(expData.slide) + ': ' + str(form_likertScale) + ' with timerActive = ' + str(timer_active)]    
            with open('log.csv', 'a') as f:
                w = csv.writer(f)
                w.writerow(row)
            if slide_counter==18:
                return redirect('poststudy', participant_id, condition)
            else:
                return redirect('experiment', participant_id, condition, timer_active, slide_counter)
    else:
        form = Confidence()
    return render(request, 'confidence.html', {'form': form})

def endpage(request):
    return render(request, 'endpage.html')
    
def prestudy(request, participant_id, condition):
    currentExp = Experiment.objects.get(pk=participant_id)
    if request.method =='POST':
        form = PreStudy(request.POST)
        if form.is_valid():
            form_gender = form.cleaned_data["gender"]
            form_age = form.cleaned_data["age"]
            form_experience = form.cleaned_data["experience"]
            form_interest = form.cleaned_data["interest"]
            form_adopt = form.cleaned_data["adopt"]
            form_aiexp = form.cleaned_data["aiexp"]
            prestudyData = None
            try:
                prestudyData = PreStudyData.objects.get(experiment=currentExp)
            except ObjectDoesNotExist:
                prestudyData = PreStudyData.objects.create()
                prestudyData.experiment = currentExp
            prestudyData.gender = form_gender
            prestudyData.age = form_age
            prestudyData.experience = form_experience
            prestudyData.interest_in_tech = form_interest
            prestudyData.adoption_of_new_tech = form_adopt
            prestudyData.familiarity_with_AI = form_aiexp
            prestudyData.save()
            #log to csv
            row = [time.ctime(), currentExp.email, condition, 'demographic data', 'gender: ' + prestudyData.gender + ', ' + 'age: ' + prestudyData.age + ', ' + 'experience: ' + prestudyData.experience + ', ' + 'interest in technology: ' + prestudyData.interest_in_tech + ', ' + 'adoption of new technologies: ' + prestudyData.adoption_of_new_tech + ', ' + 'familiarity with AI: ' + prestudyData.familiarity_with_AI]    
            with open('log.csv', 'a') as f:
                w = csv.writer(f)
                w.writerow(row)
            return redirect('experiment', participant_id, condition, 0, 0)
    else:
        form = PreStudy()
    return render(request, 'prestudy.html', {'form': form})

def startexperiment(request, participant_id, condition):
    if request.method =='POST':
        if condition == 'XAI':
            return redirect('experiment', participant_id, condition, 0, 0)
        else:
            return redirect('prestudy', participant_id, condition)
    currentExp = Experiment.objects.get(pk=participant_id)
    status = None
    if condition == 'XAI':
        status = currentExp.statusXAI
    else:
        status = currentExp.statusBaseline
    return render(request, 'startExperiment.html', {'status':status})

def poststudy(request, participant_id, condition):
    currentExp = Experiment.objects.get(pk=participant_id)
    if request.method =='POST':
        form = PostStudy(request.POST)
        if form.is_valid():
            form_item1 = form.cleaned_data["item1"]
            form_item2 = form.cleaned_data["item2"]
            form_item3 = form.cleaned_data["item3"]
            form_item4 = form.cleaned_data["item4"]
            form_item5 = form.cleaned_data["item5"]
            form_item6 = form.cleaned_data["item6"]
            form_item7 = form.cleaned_data["item7"]
            form_item8 = form.cleaned_data["item8"]
            poststudyData = None
            try:
                poststudyData = PostStudyData.objects.get(experiment=currentExp, condition=condition)
            except ObjectDoesNotExist:
                poststudyData = PostStudyData.objects.create()
                poststudyData.experiment = currentExp
                poststudyData.condition = condition
            poststudyData.item1 = form_item1
            poststudyData.item2 = form_item2
            poststudyData.item3 = form_item3
            poststudyData.item4 = form_item4
            poststudyData.item5 = form_item5
            poststudyData.item6 = form_item6
            poststudyData.item7 = form_item7
            poststudyData.item8 = form_item8
            poststudyData.save()
            if condition == 'Baseline':
                currentExp.statusBaseline = 'completed'
            else:
                currentExp.statusXAI = 'completed'
            currentExp.save()
              #log to csv
            row = [time.ctime(), currentExp.email, condition, 'UEQS', 'item1: ' + poststudyData.item1 + ', ' + 'item2: ' + poststudyData.item2 + ', ' + 'item3: ' + poststudyData.item3 + ', ' + 'item4: ' + poststudyData.item4 + ', ' + 'item5: ' + poststudyData.item5 + ', ' + 'item6: ' + poststudyData.item6 + ', ' + 'item7: ' + poststudyData.item7 + ', ' + 'item8: ' + poststudyData.item8]    
            with open('log.csv', 'a') as f:
                w = csv.writer(f)
                w.writerow(row)
            return redirect('endpage')
    else:
        form = PostStudy()
        negAttrib = ["obstructive", "complicated", "inefficient", "confusing", "boring", "not interesting", "conventional", "usual"]
        posAttrib = ["supportive", "easy", "efficient", "clear", "exciting", "interesting", "inventive", "leading edge"]
        context = {
            'form': form,
            'negAttrib': negAttrib,
            'posAttrib' : posAttrib
        }
    return render(request, 'poststudy.html', context)

def mobile(request):
    return render(request, 'mobile.html')

def results(request):
    result = Results()
    result.exportResults()
    return render(request, 'results.html')