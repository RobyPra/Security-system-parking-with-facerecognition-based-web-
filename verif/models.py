from django.db import models
from django.db.models.deletion import PROTECT, SET_NULL

# Create your models here.
class Person(models.Model):
    DESC_CHOICES = (
        ('Tamu', 'Pengunjung'),
        ('Penghuni', 'penghuni'),
    )
    GENDER_CHOICES = (
        ('P', 'Perempuan'),
        ('L', 'Laki-laki'),
    )
    no_ktp = models.CharField(primary_key= True, max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=10, choices=DESC_CHOICES)
    img = models.ImageField(upload_to="images/")
    last_modified = models.DateTimeField(auto_now_add = True)

    def __str__(self):
		     return str(self.no_ktp)

class Vehicle(models.Model):
    VEHICLES_CHOICES = (
        ('motor', 'Motor'),
        ('mobil', 'Mobil'),
    )
    no_polisi = models.CharField(max_length=100, primary_key=True)
    vehicleType = models.CharField(max_length=10, choices=VEHICLES_CHOICES)
    last_modified = models.DateTimeField(auto_now_add = True)
    

    def __str__(self):
		    return str(self.no_polisi)

class Owner(models.Model):
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    dbface = models.CharField(max_length=120)
    last_modified = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
		    return str(self.owner)



class Log(models.Model):
    LOG_CHOICES = (
        ('out', 'Out'),
        ('in', 'In'),
    )
    visitor = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    log = models.CharField(max_length=20, choices=LOG_CHOICES)
    time =models.DateTimeField(auto_now_add=True)
