from django.contrib import admin
from .models import Person, Vehicle, Log, Owner
    

# Register your models here.

admin.site.register(Person) 
admin.site.register(Vehicle)
admin.site.register(Log)
admin.site.register(Owner)