from django.db import models
from django.conf import settings
from django.db.models import fields
from django.forms import ModelForm
from django import  forms
from django.utils import timezone
import datetime
from .models import Person, Vehicle, Owner
import re

class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        fields = ['vehicle', 'owner']

class OwnerAuth(ModelForm):
    class Meta:
        model = Owner
        fields = ['vehicle']
        