from django.db import models
from django.contrib.auth.models import AbstractUser

class Kullanici(AbstractUser):
    ROLLER = (
        ('personel', 'Personel'),
        ('amir', 'Amir'),
        ('admin', 'Admin'),
    )
    rol = models.CharField(max_length=20, choices=ROLLER, default='personel')
    departman = models.CharField(max_length=100, blank=True)
    telefon = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"


class IzinTalebi(models.Model):
    DURUMLAR = (
        ('beklemede', 'Beklemede'),
        ('onaylandi', 'Onaylandı'),
        ('reddedildi', 'Reddedildi'),
    )
    IZIN_TURLERI = (
        ('yillik', 'Yıllık İzin'),
        ('hastalik', 'Hastalık İzni'),
        ('mazeret', 'Mazeret İzni'),
        ('ucretsiz', 'Ücretsiz İzin'),
    )
    personel = models.ForeignKey(Kullanici, on_delete=models.CASCADE, related_name='izin_talepleri')
    izin_turu = models.CharField(max_length=20, choices=IZIN_TURLERI)
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField()
    aciklama = models.TextField(blank=True)
    durum = models.CharField(max_length=20, choices=DURUMLAR, default='beklemede')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    amir_notu = models.TextField(blank=True)

    def gun_sayisi(self):
        return (self.bitis_tarihi - self.baslangic_tarihi).days + 1

    def __str__(self):
        return f"{self.personel.get_full_name()} - {self.get_izin_turu_display()}"


class Bildirim(models.Model):
    kullanici = models.ForeignKey(Kullanici, on_delete=models.CASCADE, related_name='bildirimler')
    mesaj = models.TextField()
    okundu = models.BooleanField(default=False)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kullanici.username} - {self.mesaj[:50]}"