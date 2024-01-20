from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from vue.models import Experiment, Order
from vue.forms import Registration

'''def frontpage(request):
    exp = Experiment.objects.get(pk=request.COOKIES.get('participant_id'))
    slide_list = exp.order.slide_order.split(",")
    context = {
        'group':exp.group,
        'slides' : slide_list
    }
    return render(request, 'frontpage.html', context)'''

def frontpage(request, participant_id):
    currentExp = Experiment.objects.get(pk=participant_id)
    slide_list = currentExp.order.slide_order.split(",")
    show_timer = None
    show_timer = True
    context = {
        'group':currentExp.group,
        'slides' : slide_list,
        'showTimer' : show_timer,
    }
    return render(request, 'frontpage.html', context)

def secondpage(request):
    return render(request, 'secondpage.html')

def startingpage(request):
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
            return redirect('frontpage', currentExp.participant_id)
    else:
        form = Registration()
    return render(request, 'startingpage.html', {'form': form})