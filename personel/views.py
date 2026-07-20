from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Kullanici, IzinTalebi, Bildirim
from datetime import date


def giris(request):
    if request.user.is_authenticated:
        return redirect('panel')
    if request.method == 'POST':
        kullanici_adi = request.POST['kullanici_adi']
        sifre = request.POST['sifre']
        kullanici = authenticate(request, username=kullanici_adi, password=sifre)
        if kullanici is not None:
            login(request, kullanici)
            return redirect('panel')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
    return render(request, 'giris.html')


def cikis(request):
    logout(request)
    return redirect('giris')


@login_required
def panel(request):
    kullanici = request.user
    if kullanici.rol == 'admin':
        return redirect('admin_panel')
    elif kullanici.rol == 'amir':
        return redirect('amir_panel')
    else:
        return redirect('personel_panel')


@login_required
def personel_panel(request):
    talepler = IzinTalebi.objects.filter(personel=request.user).order_by('-olusturma_tarihi')
    bildirimler = Bildirim.objects.filter(kullanici=request.user, okundu=False)
    return render(request, 'personel_panel.html', {
        'talepler': talepler,
        'bildirimler': bildirimler,
    })


@login_required
def amir_panel(request):
    bekleyen = IzinTalebi.objects.filter(durum='beklemede').order_by('-olusturma_tarihi')
    bildirimler = Bildirim.objects.filter(kullanici=request.user, okundu=False)
    return render(request, 'amir_panel.html', {
        'bekleyen': bekleyen,
        'bildirimler': bildirimler,
    })


@login_required
def admin_panel(request):
    tum_talepler = IzinTalebi.objects.all().order_by('-olusturma_tarihi')
    tum_kullanicilar = Kullanici.objects.all()
    bildirimler = Bildirim.objects.filter(kullanici=request.user, okundu=False)
    return render(request, 'admin_panel.html', {
        'tum_talepler': tum_talepler,
        'tum_kullanicilar': tum_kullanicilar,
        'bildirimler': bildirimler,
    })


@login_required
def izin_talebi_olustur(request):
    if request.method == 'POST':
        izin_turu = request.POST['izin_turu']
        baslangic = request.POST['baslangic_tarihi']
        bitis = request.POST['bitis_tarihi']
        aciklama = request.POST.get('aciklama', '')
        talep = IzinTalebi.objects.create(
            personel=request.user,
            izin_turu=izin_turu,
            baslangic_tarihi=baslangic,
            bitis_tarihi=bitis,
            aciklama=aciklama,
        )
        messages.success(request, 'İzin talebiniz oluşturuldu!')
        return redirect('personel_panel')
    return render(request, 'izin_talebi_olustur.html')


@login_required
def talep_guncelle(request, talep_id):
    talep = get_object_or_404(IzinTalebi, id=talep_id)
    if request.method == 'POST':
        durum = request.POST['durum']
        amir_notu = request.POST.get('amir_notu', '')
        talep.durum = durum
        talep.amir_notu = amir_notu
        talep.save()
        Bildirim.objects.create(
            kullanici=talep.personel,
            mesaj=f'İzin talebiniz {talep.get_durum_display()} olarak güncellendi.',
        )
        messages.success(request, 'Talep güncellendi!')
        return redirect('amir_panel')
    return render(request, 'talep_guncelle.html', {'talep': talep})

@login_required
def bildirim_oku(request, bildirim_id):
    bildirim = get_object_or_404(Bildirim, id=bildirim_id, kullanici=request.user)
    bildirim.okundu = True
    bildirim.save()
    return redirect('panel')