from django.contrib import admin
from .models import Experiment, Order, Data, PreStudy, PostStudy, Training

admin.site.register(Experiment)
admin.site.register(Order)
admin.site.register(Data)
admin.site.register(PreStudy)
admin.site.register(PostStudy)
admin.site.register(Training)

