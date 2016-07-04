from django.contrib import admin
from .models import *

#Customizing Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'login_email', 'username', 'date_created')

class MainGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'date_created')

class ResponsibilityTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_created')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'date_created')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'service', 'date', 'time')

class ServiceOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

#Registering Models
admin.site.register(User, UserAdmin)
admin.site.register(MainGroup, MainGroupAdmin)
admin.site.register(ResponsibilityType, ResponsibilityTypeAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(ServiceOption, ServiceOptionAdmin)
admin.site.register(OptionInput)
# admin.site.register(ServiceCredential)
