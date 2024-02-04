from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from vue.predictions import AIPredictions, TrainingAIPredictions
from vue.models import Experiment, Order, Data, PostStudyData, PreStudyData, TrainingData
from vue.forms import Registration, PreStudy, PostStudy, Confidence
import json

def startingpageBaseline(request):
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
            return redirect('training', currentExp.participant_id, 'Baseline', 0, 0)
    else:
        form = Registration()
    return render(request, 'startingpageBaseline.html', {'form': form})

def startingpageXAI(request):
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
            return redirect('training', currentExp.participant_id, 'XAI', 0, 0)
    else:
        form = Registration()
    return render(request, 'startingpageXAI.html', {'form': form})

def training(request, participant_id, condition, timer_active, slide_counter):
    currentExp = Experiment.objects.get(pk=participant_id)
    if request.method =='POST':
        content = json.loads(request.body)
        tcpEst = content['tcp_est']
        try:
            trainingData = TrainingData.objects.get(experiment=currentExp, condition=condition)
        except ObjectDoesNotExist:
            trainingData = TrainingData.objects.create()
            trainingData.experiment = currentExp
            trainingData.condition = condition
        tcps = trainingData.tcp_ests.split(",")
        tcps[slide_counter-1] = tcpEst
        trainingData.tcp_ests = ','.join(tcps)
        trainingData.save()
        if slide_counter==2:
            if condition == 'XAI':
                return redirect('startexperiment', participant_id, condition)
            else:
                return redirect('prestudy', participant_id, condition)
        else:
            return redirect('training', participant_id, condition, timer_active, slide_counter)
    else:
        predictions = TrainingAIPredictions.getTrainingAIPredictions()
        context = {
            'id': currentExp.participant_id,
            'condition': condition,
            'showTimer' : timer_active,
            'slideCounter' : slide_counter,
            'predictions': predictions
        }
        return render(request, 'training.html', context)
    
def experiment(request, participant_id, condition, timer_active, slide_counter):
    currentExp = Experiment.objects.get(pk=participant_id)
    if request.method =='POST':
        content = json.loads(request.body)
        tcpEst = content['tcp_est']
        try:
            expData = Data.objects.get(experiment=currentExp, condition=condition)
        except ObjectDoesNotExist:
            expData = Data.objects.create()
            expData.experiment = currentExp
            expData.condition = condition
        tcps = expData.tcp_ests.split(",")
        tcps[slide_counter-1] = tcpEst
        expData.tcp_ests = ','.join(tcps)
        expData.save()
        return redirect('confidence', participant_id, condition, timer_active, slide_counter)
    else:
        slide_list = currentExp.order.slide_order.split(",")
        predictions = AIPredictions.getAIPredictions()
        context = {
            'id': currentExp.participant_id,
            'group':currentExp.group,
            'slides' : slide_list,
            'condition' : condition,
            'slideCounter' : slide_counter,
            'predictions': predictions,
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
    if request.method =='POST':
        form = Confidence(request.POST)
        if form.is_valid():
            form_likertScale = form.cleaned_data["likertScale"]
            try:
                expData = Data.objects.get(experiment=currentExp, condition=condition)
            except ObjectDoesNotExist:
                expData = Data.objects.create()
                expData.experiment = currentExp
                expData.condition = condition
            scores = expData.confidence_scores.split(",")
            scores[slide_counter-1] = form_likertScale
            expData.confidence_scores = ','.join(scores)
            expData.save()
            if slide_counter==18:
                return redirect('poststudy', participant_id, condition)
            else:
                return redirect('experiment', participant_id, condition, timer_active, slide_counter)
    else:
        form = Confidence()
    return render(request, 'confidence.html', {'form': form})

def endpage(request, participant_id, condition):
    return render(request, 'endpage.html')
    
def prestudy(request, participant_id, condition):
    if request.method =='POST':
        form = PreStudy(request.POST)
        if form.is_valid():
            form_gender = form.cleaned_data["gender"]
            try:
               #
                x = 0
            except ObjectDoesNotExist:
                #
                y = 0
            return redirect('experiment', participant_id, condition, 0, 0)
    else:
        form = PreStudy()
    return render(request, 'prestudy.html', {'form': form})

def startexperiment(request, participant_id, condition):
    if request.method =='POST':
        return redirect('experiment', participant_id, condition, 0, 0)
    else:
        form = PreStudy()
    return render(request, 'startExperiment.html')

def poststudy(request, participant_id, condition):
    if request.method =='POST':
        form = PostStudy(request.POST)
        if form.is_valid():
            form_UEQS = form.cleaned_data["UEQS"]
            try:
               #
                x = 0
            except ObjectDoesNotExist:
                #
                y = 0
             #savelogic
            return redirect('endpage', participant_id, condition)
    else:
        form = PostStudy()
    return render(request, 'poststudy.html', {'form': form})