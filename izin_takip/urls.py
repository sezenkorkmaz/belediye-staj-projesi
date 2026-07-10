from django.contrib import admin
from django.urls import path
from personel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.giris, name='giris'),
    path('giris/', views.giris, name='giris'),
    path('cikis/', views.cikis, name='cikis'),
    path('panel/', views.panel, name='panel'),
    path('personel-panel/', views.personel_panel, name='personel_panel'),
    path('amir-panel/', views.amir_panel, name='amir_panel'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('izin-talebi-olustur/', views.izin_talebi_olustur, name='izin_talebi_olustur'),
    path('talep-guncelle/<int:talep_id>/', views.talep_guncelle, name='talep_guncelle'),
    path('bildirim-oku/<int:bildirim_id>/', views.bildirim_oku, name='bildirim_oku'),
]