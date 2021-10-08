from django.views import View
from django.shortcuts import render
#from django.contrib.auth.views import LoginView, LogoutView


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)