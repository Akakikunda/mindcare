from django.contrib import admin
from .models import CustomUser, Appointment
from django.contrib.auth.admin import UserAdmin
from .models import Resource
from django.contrib import admin
from .models import CustomUser
from .models import CustomUser, Appointment, Assessment, Resource, Message



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
                ('Extra Info', {'fields': ('role', 'specialty', 'location', 'bio', 'image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Appointment)
admin.site.register(Resource)
admin.site.register(Assessment)
admin.site.register(Message)


