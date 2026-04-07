# Shopping Kart - Setup & Configuration Guide

## 📋 Prerequisites

- Python 3.8 या उसके ऊपर
- pip (Python package manager)
- Git
- Text Editor या IDE (VS Code, PyCharm)

## 🔧 Installation Steps

### Step 1: Repository Clone करें (अगर GitHub पर है)

```bash
git clone <repository-url>
cd shoppingKart
```

### Step 2: Virtual Environment बनाएं

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Dependencies Install करें

```bash
pip install -r requirements.txt
```

**अगर requirements.txt नहीं है तो यह install करें:**

```bash
pip install django==6.0.1
pip install pillow  # Image handling
pip install python-decouple  # Environment variables
```

### Step 4: Database Setup करें

```bash
# Migrations apply करें
python manage.py migrate

# अगर error आए तो:
python manage.py migrate --run-syncdb
```

### Step 5: Superuser (Admin) बनाएं

```bash
python manage.py createsuperuser
```

यहाँ username, email, password दें

### Step 6: Server Start करें

```bash
python manage.py runserver
```

अब `http://localhost:8000` खोलें

## 🎯 First Time Setup Checklist

- [ ] Virtual environment activate किया
- [ ] Dependencies install किए
- [ ] `.env` file बनाई (अगर required है)
- [ ] `python manage.py migrate` चलाया
- [ ] Superuser बनाया
- [ ] Server शुरू किया
- [ ] Homepage खुला (http://localhost:8000)
- [ ] Admin panel खुला (http://localhost:8000/admin)

## 📁 Project Structure Config

```
shoppingKart/
├── Kart/settings.py          ← यहाँ settings बदलें
├── Kart/urls.py              ← main URLs
├── templates/base.html       ← master template
├── static/                   ← CSS/JS/Images
├── media/                    ← User uploads
└── manage.py                 ← Django command tool
```

## ⚙️ Settings.py की महत्वपूर्ण Settings

```python
# Debug Mode (केवल development में True)
DEBUG = True  # Production में False करें

# Allowed Hosts (production में domain add करें)
ALLOWED_HOSTS = []  # Production: ['yourdomain.com']

# Database (SQLite से PostgreSQL में बदलें)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static Files Location
STATIC_URL = '/static/'
STATICFILES_DIRS = ['static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media Files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Custom User Model
AUTH_USER_MODEL = 'accounts.Account'

# Installed Apps
INSTALLED_APPS = [
    # Default apps...
    'category',
    'accounts',
    'store',
    'carts',
    'orders',
]

# Context Processors (template में data send करते हैं)
'context_processors': [
    'category.context_processors.menulinks',
    'carts.context_processors.counter',
]
```

## 🗄️ Database Configuration

### SQLite से PostgreSQL में Change करना

```bash
# PostgreSQL install करें
pip install psycopg2-binary

# settings.py में बदलाव करें:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shopping_kart_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# फिर migration दोबारा करें
python manage.py migrate
```

## 🔐 Security Setup (Production के लिए)

### 1. Settings.py में

```python
# settings.py

# SECRET_KEY को safe रखें (environment variable से लें)
from os import environ
SECRET_KEY = environ.get('SECRET_KEY', 'fallback-key')

# Debug Mode बंद करें
DEBUG = False

# ALLOWED_HOSTS set करें
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS enforce करें
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS settings (अगर API है)
CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com'
]

# Static files के लिए
STATIC_ROOT = BASE_DIR / 'staticfiles'
python manage.py collectstatic
```

### 2. .env File बनाएं

```
# .env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=shopping_kart
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost

# Email (Gmail example)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Payment Gateway
RAZORPAY_KEY_ID=your_key
RAZORPAY_SECRET=your_secret
```

### 3. .gitignore में Add करें

```
.env
*.pyc
__pycache__/
venv/
*.log
db.sqlite3
*.egg-info/
dist/
build/
```

## 📧 Email Configuration

### Gmail से Email भेजने के लिए

```python
# settings.py में

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
```

Gmail से App Password कैसे जनरेट करें:
1. https://myaccount.google.com/apppasswords खोलें
2. 16-character password copy करें
3. settings.py में paste करें

## 🖼️ Media Files Setup

### Product Images Upload करने के लिए

```python
# settings.py में already है
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# urls.py में add करें (development के लिए)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... existing patterns
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                         document_root=settings.MEDIA_ROOT)
```

## 🧪 Testing Setup करना

### Unit Tests लिखुए

```python
# app/tests.py में

from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            product_name='Test Product',
            slug='test-product',
            price=99.99,
            stock=10
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.product_name, 'Test Product')
        self.assertTrue(self.product.is_available)
```

### Tests चलाएं

```bash
# सभी tests
python manage.py test

# एक app के tests
python manage.py test accounts

# Verbosity के साथ
python manage.py test -v 2
```

## 🐛 Common Issues & Solutions

### Issue 1: ModuleNotFoundError
```
Error: No module named 'django'

Solution:
pip install django==6.0.1
```

### Issue 2: Database Migration Error
```
Error: Your models have changes that are not yet reflected in a migration

Solution:
python manage.py makemigrations
python manage.py migrate
```

### Issue 3: Image Upload Not Working
```
Error: Image files not saving to media folder

Solution:
1. media/ folder permission check करें
2. MEDIA_URL और MEDIA_ROOT check करें
3. urls.py में static files configuration check करें
chmod -R 755 media/
```

### Issue 4: Static Files Not Loading (CSS/JS)
```
Error: CSS/JS files 404

Solution:
python manage.py collectstatic
Check STATIC_FILES_DIRS in settings.py
```

### Issue 5: Port Already in Use
```
Error: Address already in use

Solution:
# Different port पर चलाएं
python manage.py runserver 8001

# या existing process kill करें
lsof -ti:8000 | xargs kill -9
```

### Issue 6: Permission Denied
```
Error: PermissionError

Solution:
# Files को read/write permission दें
chmod -R u+w shoppingKart/
```

## 📝 Development Commands Cheat Sheet

```bash
# Project शुरू करना
source venv/bin/activate
python manage.py runserver

# Model बदलाव करना
python manage.py makemigrations
python manage.py migrate

# Django shell (database debugging)
python manage.py shell
>>> from store.models import Product
>>> Product.objects.all()

# Admin user बनाना
python manage.py createsuperuser

# Database reset करना (सावधानी से!)
python manage.py flush
python manage.py migrate

# New app बनाना
python manage.py startapp appname

# Static files collect करना (production)
python manage.py collectstatic

# Tests चलाना
python manage.py test

# Code validation
python manage.py check
```

## 🚀 Production Deployment

### Heroku पर Deploy करना

```bash
# 1. Heroku account बनाएं चलो

# 2. Heroku CLI install करें

# 3. projekta के लिए Procfile बनाएं
echo "web: gunicorn Kart.wsgi --log-file -" > Procfile

# 4. requirements.txt अपडेट करें
pip freeze > requirements.txt

# 5. Heroku app बनाएं
heroku create your-app-name

# 6. Config variables सेट करें
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False

# 7. Database सेट करें (Heroku PostgreSQL)
heroku addons:create heroku-postgresql:hobby-dev

# 8. Deploy करें
git push heroku main
```

### AWS पर Deploy करना

```bash
# EC2 instance बनाएं
# SSH से connect करें
# Project upload करें
# Gunicorn + Nginx setup करें
# Supervisor से process manage करें
```

## 📊 Performance Optimization

### 1. Database Queries Optimize करना

```python
# ❌ N+1 Query Problem
products = Product.objects.all()
for product in products:
    print(product.category.name)  # हर loop में query

# ✅ Optimized (select_related)
products = Product.objects.select_related('category').all()
```

### 2. Caching Add करना

```bash
pip install django-redis

# settings.py में
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 3. Pagination

```python
# views.py में already है
from django.core.paginator import Paginator

products = Product.objects.all()
paginator = Paginator(products, 10)  # 10 items per page
page_obj = paginator.get_page(request.GET.get('page'))
```

## 🔍 Debugging Tips

### 1. Django Debug Toolbar

```bash
pip install django-debug-toolbar

# settings.py में add करें
INSTALLED_APPS = [
    ...
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    ...
]

INTERNAL_IPS = ['127.0.0.1']
```

### 2. Logging Setup

```python
# settings.py में
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'ERROR',
    },
}
```

### 3. Print Statements

```python
print(f"User: {request.user}")
print(f"Cart Items: {cart.items.all()}")
import traceback; traceback.print_exc()
```

## ✅ Pre-Production Checklist

- [ ] `DEBUG = False` किया
- [ ] `ALLOWED_HOSTS` सेट किए
- [ ] `SECRET_KEY` safe है
- [ ] Email configuration सेही है
- [ ] Static files collectstatic किए
- [ ] Database backup ली
- [ ] HTTPS enabled है
- [ ] Error logging setup है
- [ ] Performance tested है
- [ ] Security audit की

---

अगर कोई issue आएगी तो Django documentation देखें: https://docs.djangoproject.com/

Happy Coding! 🚀
