# 🏛️ Personel İzin Takip Sistemi

Adana Büyükşehir Belediyesi Bilgi İşlem Dairesi bünyesinde gerçekleştirilen staj kapsamında geliştirilmiş web tabanlı personel izin yönetim sistemi.

## 🌐 Canlı Demo

[sezenkorkmaz.pythonanywhere.com](http://sezenkorkmaz.pythonanywhere.com)

## 📋 Proje Hakkında

Bu sistem, belediye personelinin izin taleplerini dijital ortamda yönetmesini sağlar. Personel, amir ve admin olmak üzere üç farklı kullanıcı rolü bulunmaktadır.

## ✨ Özellikler

- 👤 3 farklı kullanıcı rolü (Personel, Amir, Admin)
- 📝 İzin talebi oluşturma ve takip etme
- ✅ Amir onaylama/reddetme sistemi
- 📊 İzin bakiyesi hesaplama
- 🔔 Site içi bildirim sistemi
- 📧 E-posta bildirim sistemi
- 📈 Dashboard grafikleri ve istatistikler
- 👥 Admin kullanıcı yönetimi
- 🔒 Rol bazlı erişim kontrolü
- ✔️ Form doğrulama ve hata kontrolleri

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Python, Django 6.0.7
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript, Chart.js
- **Veritabanı:** SQLite
- **Deployment:** PythonAnywhere
- **Versiyon Kontrolü:** Git, GitHub

## 🚀 Kurulum

```bash
git clone https://github.com/sezenkorkmaz/belediye-staj-projesi.git
cd belediye-staj-projesi
git checkout master
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 👤 Geliştirici

**Sezen Korkmaz** — Bilgisayar Mühendisliği 4. Sınıf Öğrencisi

Adana Büyükşehir Belediyesi Bilgi İşlem Dairesi Stajı — 2026