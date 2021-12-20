from django.urls import path
from .views import VerifView

urlpatterns = [
    path('', VerifView.as_view(), name='verif'),
]