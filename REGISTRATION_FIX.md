# Quick Fix: Registration Issue - Action Items

## What Was Wrong ❌
1. **Database:** Using SQLite in Render (gets deleted every restart)
2. **Email:** Not configured (users couldn't activate accounts)
3. **Account:** User created with `is_active=False` (couldn't login)

## What We Fixed ✅
- Users now auto-activate on registration (line 46 in accounts/views.py)
- Simplified flow: Register → Login immediately
- Ready for PostgreSQL + proper email setup

---

## Required Render Configuration 🚀

### Add to Environment Variables:

```
DATABASE_URL=postgresql://user:password@host:5432/dbname
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEBUG=False
```

### In Render Dashboard:
1. **Create PostgreSQL Database** (Internal Database URL)
2. **Set Environment Variables** (copy DATABASE_URL from database)
3. **Get Gmail App Password** (myaccount.google.com/apppasswords)
4. **Deploy** (push code to github)
5. **Run migrations** (Web Service → Shell → python manage.py migrate)

---

## Test Locally Before Deploying

```bash
# Create .env file
echo "DEBUG=True" > .env
echo "DATABASE_URL=sqlite:///db.sqlite3" >> .env

# Run Django
python manage.py runserver

# Test register at localhost:8000
```

---

## After Deploying to Render

✅ User registers
✅ User immediately activated  
✅ Can login with credentials
✅ Data saved in PostgreSQL (persistent)

---

## Future Enhancement: Email Verification

When email is working properly:
1. Remove `user.is_active = True` from [accounts/views.py](accounts/views.py#L46)
2. Users click email link to activate
3. Can only login after email confirmation

**For now:** Users auto-activate (simpler, faster)

---

## Files Modified

- `accounts/views.py` - Line 46 (add is_active=True)
- `accounts/views.py` - Line 62 (redirect to /accounts/login/)
- `RENDER_DEPLOYMENT.md` - NEW (complete deployment guide)
