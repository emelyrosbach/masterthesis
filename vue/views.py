from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from vue.models import Experiment, Order
from vue.forms import Registration, PreStudy, PostStudy
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
    if request.method =='POST':
        #savelogic
        return redirect('training', participant_id, condition, timer_active, slide_counter)
    else:
        currentExp = Experiment.objects.get(pk=participant_id)
        slide_list = currentExp.order.slide_order.split(",")
        context = {
            'id': currentExp.participant_id,
            'condition': condition,
            'showTimer' : timer_active,
            'slideCounter' : slide_counter
        }
        return render(request, 'training.html', context)
    
def experimentFirstSlide(request, participant_id, condition):
    currentExp = Experiment.objects.get(pk=participant_id)
    slide_list = currentExp.order.slide_order.split(",")
    context = {
        'id': currentExp.participant_id,
        'group':currentExp.group,
        'slides' : slide_list,
        'showTimer' : None,
        'slideCounter' : 0,
        'condition' : condition
    }    
    show_timer = None
    if currentExp.group=='A' or currentExp.group=='B':
        show_timer = 1
    else:
        show_timer = 0
    context['showTimer'] = show_timer
    return render(request, 'experiment.html', context)

def experiment(request, participant_id, condition, timer_active, slide_counter):
    if request.method =='POST':
        content = json.loads(request.body)
        tcpEst = content['tcp_est']
        print (tcpEst)
        return redirect('experiment', participant_id, condition, timer_active, slide_counter)
    else:
        currentExp = Experiment.objects.get(pk=participant_id)
        slide_list = currentExp.order.slide_order.split(",")
        context = {
            'id': currentExp.participant_id,
            'group':currentExp.group,
            'slides' : slide_list,
            'showTimer' : timer_active,
            'slideCounter' : slide_counter,
            'condition' : condition
        }
        return render(request, 'experiment.html', context)

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
            return redirect('experimentFirstSlide', participant_id, condition)
    else:
        form = PreStudy()
    return render(request, 'prestudy.html', {'form': form})

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