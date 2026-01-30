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


## نشر المشروع على Vercel (Django)

### 1) ملفات جاهزة داخل المشروع
- `vercel.json` جاهز
- `api/index.py` كنقطة دخول لـ Vercel
- `build_files.sh` لتجهيز المتطلبات و `collectstatic`

### 2) إعدادات مهمّة (لتفادي خطأ CSRF 403)
في Vercel افتح **Project → Settings → Environment Variables** وأضف:
- `SECRET_KEY` = قيمة قوية
- `DEBUG` = `0`
- (مستحسن) `ALLOWED_HOSTS` = `your-project.vercel.app`
- (مستحسن) `CSRF_TRUSTED_ORIGINS` = `https://your-project.vercel.app`

> ملاحظة: لو تستخدم دومين مخصص، أضفه في ALLOWED_HOSTS و CSRF_TRUSTED_ORIGINS.

### 3) قاعدة البيانات
- SQLite في Vercel **غير مناسبة للإنتاج** (بدون استمرارية + مشاكل تزامن).
- الأفضل تستخدم Postgres وتضع `DATABASE_URL`.
  أي خدمة مثل: Vercel Postgres / Neon / Supabase.

### 4) Build Command في Vercel
من **Settings → Build & Development Settings** اجعل:
- Build Command: `bash build_files.sh`

### 5) الميجريشن
إذا تستخدم Postgres، شغّل:
- محلياً: `python manage.py migrate`
- أو فعّل سطر `migrate` داخل `build_files.sh` بعد ضبط `DATABASE_URL`.
