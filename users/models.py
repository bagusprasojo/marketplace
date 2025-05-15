from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_designer = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

class Provinsi(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Kabupaten(models.Model):
    name = models.CharField(max_length=100)
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE, related_name='kabupatens')

    def __str__(self):
        return self.name
    
class Kecamatan(models.Model):
    name = models.CharField(max_length=100)
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE, related_name='kecamatans')

    def __str__(self):
        return self.name
    
class Kelurahan(models.Model):
    name = models.CharField(max_length=100)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE, related_name='kelurahans')

    def __str__(self):
        return self.name
    
class Alamat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alamats')
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
    detail_alamat = models.CharField(max_length=255)
    kode_pos = models.CharField(max_length=10, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    nama_alamat = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.detail_alamat}"