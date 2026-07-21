from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
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
    onaylanan = tum_talepler.filter(durum='onaylandi').count()
    reddedilen = tum_talepler.filter(durum='reddedildi').count()
    beklemede = tum_talepler.filter(durum='beklemede').count()
    yillik = tum_talepler.filter(izin_turu='yillik').count()
    hastalik = tum_talepler.filter(izin_turu='hastalik').count()
    mazeret = tum_talepler.filter(izin_turu='mazeret').count()
    ucretsiz = tum_talepler.filter(izin_turu='ucretsiz').count()
    return render(request, 'admin_panel.html', {
        'tum_talepler': tum_talepler,
        'tum_kullanicilar': tum_kullanicilar,
        'bildirimler': bildirimler,
        'onaylanan': onaylanan,
        'reddedilen': reddedilen,
        'beklemede': beklemede,
        'yillik': yillik,
        'hastalik': hastalik,
        'mazeret': mazeret,
        'ucretsiz': ucretsiz,
    })


@login_required
def kullanici_ekle(request):
    if request.user.rol != 'admin':
        return redirect('panel')
    if request.method == 'POST':
        kullanici_adi = request.POST['kullanici_adi']
        sifre = request.POST['sifre']
        ad = request.POST['ad']
        soyad = request.POST['soyad']
        email = request.POST.get('email', '')
        rol = request.POST['rol']
        departman = request.POST.get('departman', '')
        telefon = request.POST.get('telefon', '')
        yillik_izin = request.POST.get('yillik_izin_hakki', 14)

        if Kullanici.objects.filter(username=kullanici_adi).exists():
            messages.error(request, 'Bu kullanıcı adı zaten kullanılıyor!')
            return render(request, 'kullanici_ekle.html')

        kullanici = Kullanici.objects.create_user(
            username=kullanici_adi,
            password=sifre,
            first_name=ad,
            last_name=soyad,
            email=email,
            rol=rol,
            departman=departman,
            telefon=telefon,
            yillik_izin_hakki=yillik_izin,
        )
        messages.success(request, f'{ad} {soyad} başarıyla eklendi!')
        return redirect('admin_panel')
    return render(request, 'kullanici_ekle.html')


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

        if talep.personel.email:
            try:
                send_mail(
                    subject='İzin Talebi Güncellendi',
                    message=f'Sayın {talep.personel.get_full_name()},\n\n'
                            f'İzin talebiniz {talep.get_durum_display()} olarak güncellendi.\n\n'
                            f'İzin Türü: {talep.get_izin_turu_display()}\n'
                            f'Başlangıç: {talep.baslangic_tarihi}\n'
                            f'Bitiş: {talep.bitis_tarihi}\n'
                            f'Amir Notu: {talep.amir_notu or "-"}\n\n'
                            f'Adana Büyükşehir Belediyesi Personel İzin Takip Sistemi',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[talep.personel.email],
                    fail_silently=False,
                )
            except Exception as e:
                pass

        messages.success(request, 'Talep güncellendi ve personele bildirim gönderildi!')
        return redirect('amir_panel')
    return render(request, 'talep_guncelle.html', {'talep': talep})


@login_required
def bildirimler(request):
    tum_bildirimler = Bildirim.objects.filter(kullanici=request.user).order_by('-olusturma_tarihi')
    okunmamis = Bildirim.objects.filter(kullanici=request.user, okundu=False)
    return render(request, 'bildirimler.html', {
        'tum_bildirimler': tum_bildirimler,
        'bildirimler': okunmamis,
    })


@login_required
def bildirim_oku(request, bildirim_id):
    bildirim = get_object_or_404(Bildirim, id=bildirim_id, kullanici=request.user)
    bildirim.okundu = True
    bildirim.save()
    return redirect('bildirimler')


@login_required
def tum_bildirimleri_oku(request):
    Bildirim.objects.filter(kullanici=request.user, okundu=False).update(okundu=True)
    return redirect('bildirimler')