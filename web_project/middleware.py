from django.http import HttpResponse
from vue.models import Experiment, Order

'''class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.
        participant_id = request.COOKIES.get('participant_id')
        if not participant_id:
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
            currentExp.save()
            response = self.get_response(request)
            response.set_cookie('participant_id', currentExp.participant_id)
        else:
            response = self.get_response(request)
        
        return response
        '''