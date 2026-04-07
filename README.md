# Shopping Kart - Quick Reference Guide

## 🚀 Project Start करना

```bash
# Virtual environment create करें
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Dependencies install करें
pip install -r requirements.txt

# Database migrations apply करें
python manage.py migrate

# Superuser बनाएं (admin के लिए)
python manage.py createsuperuser

# Server चलाएं
python manage.py runserver
```

## 📁 Project का Simple Overview

| Folder | Purpose | Main File |
|--------|---------|-----------|
| **accounts** | User login/register/profile | models.py, views.py |
| **store** | Products, reviews, search | models.py (Product, ReviewRating) |
| **carts** | Shopping cart functionality | models.py (Cart, CartItem) |
| **category** | Product categories | models.py (Category) |
| **orders** | Order & payment management | models.py (Order, Payments) |
| **templates** | HTML files | base.html, index.html |
| **static** | CSS, JS, images | custom.css, script.js |

## 🗂️ Database Models (सरल परिचय)

### **Account** - User की information
- `username`, `email`, `phone_number`
- `is_active`, `is_staff`, `is_admin`

### **Product** - Product की details
- `product_name`, `price`, `stock`, `image`
- `category` (किस category में है)
- `is_available` (available है या नहीं)

### **Cart & CartItem** - Shopping cart
- `CartItem` में product quantity और variations
- User के साथ linked है

### **Order & OrderProduct** - Orders
- `Order` में address, total amount, status
- `OrderProduct` में कौन से products ordered हैं

### **Variation** - Product options
- Size (S, M, L, XL)
- Color (Red, Blue, etc.)

### **ReviewRating** - Customer reviews
- Rating (0-5 stars)
- Review text

## 🔑 Important Commands

```bash
# नई migration बनाएं (model change के बाद)
python manage.py makemigrations

# Migrations apply करें
python manage.py migrate

# Admin panel खोलें (localhost:8000/admin)
python manage.py runserver

# Django shell में database query करें
python manage.py shell

# Static files collect करें (production के लिए)
python manage.py collectstatic

# Tests run करें
python manage.py test
```

## 💡 Key URLs Pattern

```
/ - Homepage
/account/register/ - Registration
/account/login/ - Login
/store/ - All products
/store/category-slug/ - Category products
/store/category/product-slug/ - Product detail
/cart/ - Shopping cart
/order/ - Checkout
/order/order-number/ - Order details
/account/dashboard/ - User dashboard
```

## 🎯 Feature Checklist

- ✅ User Registration & Authentication
- ✅ Product Browsing by Category
- ✅ Product Search
- ✅ Shopping Cart Management
- ✅ Multiple variations (Color, Size)
- ✅ Customer Reviews & Ratings
- ✅ Order Placement
- ✅ Order History
- ✅ User Profile Management
- ✅ Payment Integration Support

## ⚠️ Important Notes

1. **Development Mode**: `DEBUG = True` है settings.py में
2. **Database**: SQLite3 use हो रहा है (local development के लिए)
3. **Secret Key**: Production में change करें
4. **Media Files**: `media/` folder में user uploads जाते हैं

## 🔐 Django Admin में कैसे काम करें

```
1. localhost:8000/admin/ खोलें
2. Superuser credentials से login करें
3. Products, Orders, Users manage कर सकते हैं
4. Reviews, Variations को moderate कर सकते हैं
```

## 📦 Project Structure

```
shoppingKart/
├── Kart/              - Main project settings
├── accounts/          - User authentication
├── store/             - Products & reviews
├── carts/             - Cart functionality
├── category/          - Product categories
├── orders/            - Order management
├── templates/         - HTML files
├── static/            - CSS, JS, Images
├── media/             - User uploads
├── db.sqlite3         - Database file
└── manage.py          - Django command tool
```

## 🐛 Common Issues & Solutions

**Issue**: Database error
```bash
python manage.py migrate --run-syncdb
```

**Issue**: Static files not loading
```bash
python manage.py collectstatic --noinput
```

**Issue**: Permission denied on media folder
```bash
chmod -R 755 media/
```

## 📚 Development Tips

1. **Browser Developer Tools** - CSS/JS debugging के लिए
2. **Django Debug Toolbar** - Query optimization के लिए
3. **Django Shell** - Database testing के लिए
4. **Logs** - `print()` और `logging` से debug करें

## 🎓 अगले Steps (Improvement के लिए)

1. PostgreSQL में shift करें
2. Celery add करें (async tasks के लिए)
3. Redis add करें (caching के लिए)
4. Email service integrate करें
5. Payment gateway (Razorpay/Stripe) add करें
6. Unit tests लिखें
7. Docker containerize करें
8. Deploy करें (Heroku/AWS/Azure)

---

**अधिक details के लिए `PROJECT_DOCUMENTATION.md` पढ़ें**
