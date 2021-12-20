from django.views import View
from django.shortcuts import render
#from django.contrib.auth.views import LoginView, LogoutView
from .models import Person, Vehicle, Owner
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, Http404
import random, string

class VerifView(View):
    template_name = 'verif/verification.html'

    def get(self, request):
        return render(request, self.template_name)