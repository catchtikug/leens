from django.contrib import admin
from .models import User, SideEffectReport, DrugResistanceReport, Facility, Drug, Disease

admin.site.register(User)
admin.site.register(SideEffectReport)
admin.site.register(DrugResistanceReport)
admin.site.register(Facility)
admin.site.register(Drug)
admin.site.register(Disease)
