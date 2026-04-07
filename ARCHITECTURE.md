# Shopping Kart - Technical Architecture

## 🏗️ System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Templates)                      │
│  (HTML/CSS/JavaScript) - Responsive Bootstrap UI            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Django Web Framework (6.0.1)                    │
├─────────────────────────────────────────────────────────────┤
│                   URL Routing Layer                          │
│   (Kart/urls.py → App specific urls.py)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  5 Django Apps Layer                         │
├─────────────────────────────────────────────────────────────┤
│ accounts/ │ store/ │ carts/ │ category/ │ orders/          │
│ (Users)   │(Prod)  │(Cart)  │(Category) │(Orders)          │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Django ORM (Object-Relational Mapping)          │
│              (Abstract database queries)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                Database Layer (SQLite3)                      │
│              (db.sqlite3 file storage)                       │
└──────────────────────────────────────────────────────────────┘

┌──────────────────┐        ┌──────────────────┐
│  Media Files     │        │  Static Files    │
│  (User uploads)  │        │  (CSS/JS/Images) │
│  media/          │        │  static/         │
└──────────────────┘        └──────────────────┘
```

## 📊 Data Flow Architecture

### 1. **User Registration & Login Flow**

```
User visits /account/register/
         │
         ▼
Django View (accounts/views.py::register)
         │
         ├─→ Form Validation (accounts/forms.py)
         │
         ├─→ Password Hashing (Django security)
         │
         └─→ Database Save (Account model)
         │
         ▼
Redirect to Login Page
```

### 2. **Shopping Flow**

```
Browse Products (/store/) 
         │
         ├─→ Get all Products from DB
         ├─→ Pagination (3 products per page)
         └─→ Render store.html
         
         ▼

View Product Detail (/store/category/product/)
         │
         ├─→ Get single Product
         ├─→ Get Reviews & Ratings
         ├─→ Check if in cart
         └─→ Render product_detail.html

         ▼

Add to Cart (/carts/add/)
         │
         ├─→ Get or Create Cart (session-based)
         ├─→ Get or Create CartItem
         ├─→ Add variations (selected size/color)
         ├─→ Update quantity
         └─→ Save to Database

         ▼

View Cart (/cart/)
         │
         ├─→ Get all CartItems for user
         ├─→ Calculate subtotal for each item
         ├─→ Calculate total amount
         └─→ Render cart.html
```

### 3. **Order Placement Flow**

```
Checkout (/order/place/)
         │
         ├─→ Verify User is Authenticated
         ├─→ Validate Delivery Address
         ├─→ Calculate total + tax
         │
         ▼
Create Order (Order model)
         │
         ├─→ Generate unique order_number
         ├─→ Save shipping details
         ├─→ Set status = 'New'
         │
         ▼
Create OrderProducts (link cart items to order)
         │
         ├─→ For each CartItem:
         │   ├─→ Create OrderProduct
         │   ├─→ Store product price (historical)
         │   ├─→ Store variations selected
         │   └─→ Store quantity
         │
         ▼
Process Payment
         │
         └─→ Create Payments record
         │
         ▼
Clear Cart (delete CartItems)
         │
         ▼
Redirect to Order Confirmation
```

## 🔐 Authentication & Authorization

```
User Request (with session/token)
         │
         ▼
Django Middleware Chain
  ├─→ SecurityMiddleware
  ├─→ SessionMiddleware (check session)
  ├─→ AuthenticationMiddleware (identify user)
  ├─→ CsrfViewMiddleware (prevent CSRF)
  └─→ MessageMiddleware
         │
         ▼
View Checks: request.user.is_authenticated
         │
    ┌────┴────┐
    │          │
   Yes        No
    │          │
    ▼          ▼
  Allow    Redirect to Login
```

## 📦 Model Relationship Diagram

```
Account
├─ (1:1) UserProfile
│        ├─ address_line_1
│        ├─ address_line_2
│        ├─ city, state, country
│        └─ profile_picture
│
├─ (1:Many) Order
│           ├─ order_number
│           ├─ shipping address
│           ├─ status (New/Accepted/Completed/Cancelled)
│           ├─ order_total
│           └─ tax
│
├─ (1:Many) OrderProduct
│           ├─ product (FK)
│           ├─ variation (FK)
│           ├─ quantity
│           └─ product_price (at time of order)
│
├─ (1:Many) CartItem
│           ├─ product (FK)
│           ├─ variation (M2M)
│           ├─ quantity
│           └─ is_active
│
└─ (1:Many) ReviewRating
            ├─ product (FK)
            ├─ rating (float)
            ├─ review (text)
            └─ status (approved/not)

Product
├─ (Many:1) Category (slug-based)
│
├─ (1:Many) Variation
│           ├─ color/size
│           └─ is_active
│
├─ (1:Many) ReviewRating
│           └─ average rating calculated
│
├─ (1:Many) ProductGallery
│           └─ multiple images
│
├─ (1:Many) CartItem
│
└─ (1:Many) OrderProduct

Cart
└─ (1:Many) CartItem
            ├─ product
            ├─ user (optional - for cart persistence)
            └─ variations
```

## 🔄 Request-Response Cycle

```
1. USER REQUEST
   GET /store/category/product/
   (HTTP Request with headers, cookies, etc.)
   │
   ▼
2. URL ROUTING (urls.py)
   Matches URL pattern
   → store.urls:product_detail
   │
   ▼
3. VIEW PROCESSING (views.py)
   - Extract parameters (category_slug, product_slug)
   - Query database
   - Check permissions
   - Prepare context data
   │
   ▼
4. CONTEXT PROCESSORS
   - Add cart counter via carts.context_processors
   - Add menu links via category.context_processors
   - Add user data
   │
   ▼
5. TEMPLATE RENDERING
   - Load product_detail.html
   - Populate with context
   - Include base.html, includes/
   │
   ▼
6. HTTP RESPONSE
   HTML page sent to browser
```

## 🗄️ Database Queries (ORM Examples)

### Create (Insert)
```python
# In views when adding to cart
cart_item = CartItem.objects.create(
    product=product,
    cart=cart,
    quantity=qty
)
```

### Read (Select)
```python
# Get all products in category
products = Product.objects.filter(
    category=category,
    is_available=True
).order_by('-created_date')

# Get user's orders
orders = Order.objects.filter(
    user=request.user,
    is_ordered=True
)
```

### Update
```python
# Update cart item quantity
cart_item.quantity += 1
cart_item.save()

# Update order status
order.status = 'Completed'
order.save()
```

### Delete
```python
# Remove from cart
CartItem.objects.filter(
    product=product,
    cart=cart
).delete()
```

## 🎨 Template Inheritance Structure

```
base.html (master template)
├─ navbar (includes/navbar.html)
│  └─ cart_counter (from carts context processor)
│
├─ sidebar (includes/sidebar.html)
│  └─ categories (from category context processor)
│
├─ content block (filled by child templates)
│
├─ footer
│
└─ scripts

store.html (inherits base.html)
├─ products grid/list
└─ pagination

product_detail.html
├─ product details
├─ reviews section
├─ add to cart button
└─ variations selector

cart.html
├─ cart items table
├─ quantity controls
└─ checkout button

order.html
├─ address form
├─ order summary
└─ payment button
```

## 💾 File Upload Structure

```
media/
├─ photos/
│  ├─ products/
│  │  ├─ product1.jpg
│  │  ├─ product2.jpg
│  │  └─ gallery/
│  │     └─ product1_img1.jpg
│  │
│  └─ categories/
│     └─ category_icon.jpg
│
└─ userprofile/
   ├─ profile_pic_user1.jpg
   └─ profile_pic_user2.jpg
```

## 🔌 API-like Views (Request-Response)

### Example: Add to Cart Endpoint

```
Request: POST /carts/add/
Payload: {
    'product_id': 5,
    'quantity': 2,
    'color': 'red',
    'size': 'M'
}

Process:
1. Get or Create Cart (session/user based)
2. Get Product by ID
3. Get or Create CartItem
4. Get Variation objects (color='red', size='M')
5. Add variations to CartItem
6. Increment quantity
7. Save to DB

Response: Redirect to /cart/ or JSON
```

## 📈 Performance Considerations

### Current Setup:
- SQLite (single file database)
- No caching
- No database indexing optimization
- Sequential query processing

### Optimizations for Scale:
```
Current (Small Scale)    →    Production (Large Scale)
─────────────────────         ────────────────────────
SQLite                   →    PostgreSQL
No Caching              →    Redis Cache
Single Thread           →    Gunicorn Workers
No Task Queue           →    Celery + RabbitMQ
No CDN                  →    Cloudflare/AWS CloudFront
Debug=True              →    Debug=False
All Requests Sync       →    Async with Uvicorn
```

## 🚀 Deployment Considerations

```
Development                 Production
─────────────────          ─────────────
DEBUG = True               DEBUG = False
SQLite                     PostgreSQL/MySQL
Localhost:8000             Domain name
django runserver           Gunicorn/UWSGI
No HTTPS                   HTTPS enforced
SECRET_KEY exposed         SECRET_KEY from env
ALLOWED_HOSTS=[]           ALLOWED_HOSTS set
No logging                 Structured logging
```

## 🔄 API Request Headers Flow

```
Browser Request
├─ Accept: text/html
├─ User-Agent: Mozilla/...
├─ Cookie: sessionid=...
├─ CSRF-Token: (for POST)
└─ Content-Type: application/x-www-form-urlencoded

Django Processes
├─ Session middleware validates
├─ CSRF middleware checks token
├─ Auth middleware identifies user
└─ View processes request

Response
├─ Content-Type: text/html
├─ Set-Cookie: sessionid=...
└─ Status: 200 OK
```

## 📊 Database Relationships Summary

```
▓▓▓ One-to-One (1:1)
▓░░ One-to-Many (1:*)
░▓▓ Many-to-Many (*:*)

Account ▓▓▓ UserProfile
Account ▓░░ Order
Account ▓░░ OrderProduct
Account ▓░░ CartItem
Account ▓░░ ReviewRating

Product ░▓░ Category (Foreign Key)
Product ▓░░ Variation
Product ▓░░ ReviewRating
Product ▓░░ ProductGallery
Product ▓░░ CartItem
Product ▓░░ OrderProduct

Cart ▓░░ CartItem
CartItem ░▓▓ Variation

Order ▓░░ OrderProduct
Order ▓░░ Payments
```

---

यह architecture scalable, maintainable, और future-proof है। Django की built-in features को सही तरीके से use किया गया है।
