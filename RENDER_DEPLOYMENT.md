# Render.com Deployment Guide

## Problem Fixed ✅

**Issue:** Users could register but couldn't login, data wasn't saving.

**Root Cause:** 
1. SQLite database on Render (ephemeral filesystem - data gets deleted)
2. Email not configured (users couldn't activate)
3. Environment variables not set

---

## Step-by-Step Solution

### 1️⃣ Add PostgreSQL Database on Render

1. Go to [render.com](https://render.com)
2. Click **"New +"** in dashboard
3. Select **"PostgreSQL"**
4. Fill in details:
   - **Name:** `shoppingkart-db`
   - **PostgreSQL Version:** 15
   - **Region:** Same as your web service
5. Click **"Create Database"**
6. Copy the **Internal Database URL** (looks like: `postgresql://user:password@dpg-xxx:5432/dbname`)

---

### 2️⃣ Update Environment Variables on Render

Go to your **Web Service** → **Environment** tab:

Add these variables:

```env
DEBUG=False
SECRET_KEY=your-very-long-random-secure-key-here
DATABASE_URL=postgresql://user:password@dpg-xxx:5432/dbname
RENDER=True

# Email Configuration (Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-google-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Security (enable on production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
ALLOWED_HOSTS=shoppingkart-rdlq.onrender.com,your-custom-domain.com
```

---

### 3️⃣ Get Gmail App Password

1. Open [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Select **App:** Mail
3. Select **Device:** Windows Computer (or your platform)
4. Click **Generate**
5. Copy the generated 16-character password
6. Use this as `EMAIL_HOST_PASSWORD`

---

### 4️⃣ Deploy to Render

Push your code with the updated `requirements.txt`:

```bash
git add .
git commit -m "Fix registration: auto-activate users, add PostgreSQL support"
git push
```

Render will auto-deploy. Check build logs in dashboard.

---

### 5️⃣ Run Migrations on Production

After deployment succeeds:

1. Go to **Web Service** → **Shell**
2. Run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## Test Registration

1. Visit your domain
2. Register with test email
3. User should be created immediately
4. Can login with credentials
5. Data persisted in PostgreSQL ✅

---

## Future: Email Verification (Optional)

Currently registration auto-activates users. To enable email verification:

1. Remove `user.is_active = True` from [accounts/views.py](accounts/views.py#L46)
2. Keep email sending code
3. Users will need to click activation link
4. Production email must be working for this

---

## Troubleshooting

### "Database connection refused"
- Check DATABASE_URL is correct
- Database must be in SAME region as web service
- Wait 2-3 minutes after creating database

### "Email not sending"
- Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- Try different email app password
- Check spam folder

### "Static files not found"
- Run: `python manage.py collectstatic --noinput --clear`
- Restart service

### "500 Error after deploy"
- Check logs: `tail -f logs/django.log` in Shell
- Verify all env vars are set
- Run migrations again

---

## Production Checklist

- [x] Database: PostgreSQL (not SQLite)
- [x] Email: SMTP configured
- [x] Environment variables: All set
- [x] DEBUG: False
- [ ] Security: Run `python manage.py check --deploy`
- [ ] SSL: Render auto-provides (HTTPS enabled)
- [ ] Admin password: Created superuser
- [ ] Admin rename: `/admin/` → something random (future improvement)

---

## Current Setup

✅ **Registration:** Auto-activates (no email verification needed yet)  
✅ **Database:** PostgreSQL (persistent)  
✅ **Email:** SMTP backend configured (optional to use)  
✅ **Security:** SSL redirect enabled  

Users can now:
- Register successfully
- Login immediately  
- Data persists across restarts
