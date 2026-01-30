# Threadify — نسخة مصغّرة من تويتر (ثريدز)

مشروع ويب كامل باستخدام **Django** مع:
- تسجيل حساب + تسجيل دخول/خروج
- نشر ثريدز (منشورات) + ردود (Replies)
- إعجاب (Like) بالمنشورات (AJAX)
- متابعة/إلغاء متابعة المستخدمين (Follow) (AJAX)
- صفحة بروفايل + تعديل الملف الشخصي
- **قاعدة بيانات محلية SQLite** (الافتراضي في Django)
- تصميم حديث Responsive باستخدام **Bootstrap 5 (RTL)**

## المتطلبات
- Python 3.10+ (يفضّل 3.11 أو أحدث)

## التشغيل محلياً (Windows / macOS / Linux)

1) فك الضغط ثم ادخل مجلد المشروع:
```bash
cd threads_clone_django
```

2) أنشئ بيئة افتراضية وثبّت الحزم:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

3) أنشئ قاعدة البيانات (SQLite) وطبّق الهجرات:
```bash
python manage.py migrate
```

4) (اختياري) أنشئ مستخدم admin للوحة التحكم:
```bash
python manage.py createsuperuser
```

5) شغّل السيرفر:
```bash
python manage.py runserver
```

ثم افتح:
- الصفحة الرئيسية: http://127.0.0.1:8000/
- لوحة التحكم: http://127.0.0.1:8000/admin/

## ملاحظات
- رفع الصور (Avatar وصور الثريدز) مفعل عبر `MEDIA_URL` و `MEDIA_ROOT` أثناء التطوير.
- في الإنتاج يلزم إعدادات إضافية للـ static/media و DEBUG=False.

## بنية المشروع
- `threader/` إعدادات مشروع Django
- `core/` التطبيق الأساسي (الموديلات، الفورمز، الفيوز)
- `templates/` القوالب
- `static/` ملفات CSS/JS


## استكشاف الأخطاء (إذا واجهتك مشكلة عند التسجيل)
- تأكد أنك طبّقت الهجرات:
  ```bash
  python manage.py migrate
  ```
- إذا كنت لعبت بالملفات/الموديلات أو ظهرت رسالة (no such table):
  احذف ملف `db.sqlite3` ثم نفّذ:
  ```bash
  python manage.py migrate
  ```
- تأكد تثبيت الحزم:
  ```bash
  pip install -r requirements.txt
  ```
