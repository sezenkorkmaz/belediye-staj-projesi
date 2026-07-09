from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Kullanici, IzinTalebi, Bildirim

@admin.register(Kullanici)
class KullaniciAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'rol', 'departman', 'email')
    list_filter = ('rol', 'departman')
    fieldsets = UserAdmin.fieldsets + (
        ('Ek Bilgiler', {'fields': ('rol', 'departman', 'telefon')}),
    )

@admin.register(IzinTalebi)
class IzinTalebiAdmin(admin.ModelAdmin):
    list_display = ('personel', 'izin_turu', 'baslangic_tarihi', 'bitis_tarihi', 'durum')
    list_filter = ('durum', 'izin_turu')

@admin.register(Bildirim)
class BildirimAdmin(admin.ModelAdmin):
    list_display = ('kullanici', 'mesaj', 'okundu', 'olusturma_tarihi')