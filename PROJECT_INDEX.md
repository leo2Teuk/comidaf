# 📑 PROJECT_INDEX.md - Django E-Commerce Complete Codebase Documentation

**Generated:** April 28, 2026  
**Project:** Django E-Commerce Platform with Admin Dashboard  
**Framework:** Django 2.2+ | Python 3.7+  
**Structure:** Multi-app e-commerce with custom admin dashboard

---

## 📋 TABLE OF CONTENTS

1. [Project Structure & Overview](#project-structure--overview)
2. [Applications (Apps)](#applications-apps)
3. [Database Schema & Models](#database-schema--models)
4. [Views & Business Logic](#views--business-logic)
5. [URL Patterns & Routing](#url-patterns--routing)
6. [Forms & Data Validation](#forms--data-validation)
7. [Templates & Frontend](#templates--frontend)
8. [Static Files & Assets](#static-files--assets)
9. [Settings & Configuration](#settings--configuration)
10. [Middleware & Custom Code](#middleware--custom-code)
11. [Management Commands](#management-commands)
12. [Testing & Documentation](#testing--documentation)

---

## 1. PROJECT STRUCTURE & OVERVIEW

### Root Directory Structure
```
Django-Ecommerce-master/
├── bin/                           # CLI utilities
│   ├── cli.py                    # Command-line interface
│   ├── commands.py               # Command handlers
│   └── shared.py                 # Shared utilities
├── core/                         # Main e-commerce app
├── dashboard/                    # Admin dashboard app
├── demo/                         # Django project settings
├── templates/                    # HTML templates
├── static_in_env/               # Development static files
├── static_root/                 # Production static files (collectstatic)
├── media_root/                  # User uploaded files
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── db.sqlite3                   # SQLite database
├── setup_dashboard.py           # Dashboard setup script
├── test_dashboard.py            # Dashboard tests
└── README.md                    # Project documentation
```

### Project Type
- **E-Commerce Platform** with product catalog, shopping cart, and checkout
- **Admin Dashboard** for managing products, orders, users, and site settings
- **Multi-tenant Support** with customizable site settings
- **Location:** `e:\unelel\Django-Ecommerce-master`

### Key Features
- Shopping cart and order management
- Multiple payment/checkout flows
- Product categories with hierarchy
- Admin dashboard for all management tasks
- Site-wide configuration management
- User management and authentication
- Reviews and ratings system
- Promotional codes and discounts
- Contact form handling
- Analytics and reporting

---

## 2. APPLICATIONS (APPS)

### 2.1 CORE APP
**Location:** [core/](core)  
**Purpose:** Main e-commerce functionality

#### Files:
- **[core/__init__.py](core/__init__.py)** - App initialization
- **[core/models.py](core/models.py)** - Database models
- **[core/views.py](core/views.py)** - Business logic & request handlers
- **[core/urls.py](core/urls.py)** - URL routing
- **[core/forms.py](core/forms.py)** - Form classes for checkout & refunds
- **[core/admin.py](core/admin.py)** - Django admin configuration
- **[core/apps.py](core/apps.py)** - App configuration
- **[core/middleware.py](core/middleware.py)** - Custom middleware
- **[core/tests.py](core/tests.py)** - Unit tests
- **[core/context_processors.py](core/context_processors.py)** - Template context
- **[core/management/commands/](core/management/commands)** - Custom commands
  - `makesuper.py` - Create superuser
  - `rename.py` - Utility script

#### Template Tags:
**Location:** [core/templatetags/](core/templatetags)
- **cart_template_tags.py** - Cart-related template filters
- **category_template_tags.py** - Category-related template filters
- **slide_template_tags.py** - Carousel slide filters

#### Migrations:
**Location:** [core/migrations/](core/migrations)
- `0001_initial.py` - Initial schema
- `0002_sitesettings_hero_cta_link_and_more.py`
- `0003_alter_siteimage_image_type.py`
- `0004_sitesettings_primary_color_and_more.py`
- `0005_sitesettings_hero_badge_text_and_more.py`
- `0006_add_notification_email_to_sitesettings.py`
- `0007_add_city_to_billing_address.py`
- `0008_add_pageview_and_item_view_count.py`
- `0009_add_userprofile.py`

---

### 2.2 DASHBOARD APP
**Location:** [dashboard/](dashboard)  
**Purpose:** Admin/staff management interface

#### Files:
- **[dashboard/__init__.py](dashboard/__init__.py)** - App initialization
- **[dashboard/models.py](dashboard/models.py)** - (Empty, models in core)
- **[dashboard/views.py](dashboard/views.py)** - Dashboard views (24+ views)
- **[dashboard/urls.py](dashboard/urls.py)** - URL routing (28+ routes)
- **[dashboard/forms.py](dashboard/forms.py)** - Forms for dashboard (7+ forms)
- **[dashboard/admin.py](dashboard/admin.py)** - Admin configuration
- **[dashboard/apps.py](dashboard/apps.py)** - App configuration

#### Migrations:
**Location:** [dashboard/migrations/](dashboard/migrations)
- `__init__.py` - Package marker

---

### 2.3 DEMO PROJECT
**Location:** [demo/](demo)  
**Purpose:** Django project configuration

#### Files:
- **[demo/settings.py](demo/settings.py)** - Django configuration
- **[demo/urls.py](demo/urls.py)** - Root URL configuration
- **[demo/wsgi.py](demo/wsgi.py)** - WSGI application for deployment
- **[demo/azure.py](demo/azure.py)** - Azure cloud configuration

---

## 3. DATABASE SCHEMA & MODELS

### 3.1 E-COMMERCE CORE MODELS

#### **Slide Model** [core/models.py:29-36]
```python
Fields:
- caption1 (CharField, max_length=100)
- caption2 (CharField, max_length=100)
- link (CharField, max_length=100)
- image (ImageField, help_text="Size: 1920x570")
- is_active (BooleanField, default=True)
```
Purpose: Carousel slides on homepage
Usage: HomeView displays featured slides

---

#### **Category Model** [core/models.py:39-74]
```python
Fields:
- title (CharField, max_length=100)
- slug (SlugField, unique=True)
- description (TextField, blank=True)
- image (ImageField, upload_to='categories/', blank=True)
- parent (ForeignKey to self, for hierarchical categories)
- is_active (BooleanField, default=True)
- order (PositiveIntegerField, default=0)
- created_at (DateTimeField)
- updated_at (DateTimeField, auto_now=True)

Methods:
- get_absolute_url() → Returns category page URL
- is_parent (property) → Checks if parent category
- get_children() → Returns active child categories
- get_all_children() → Recursively gets all descendants
```
Purpose: Product categorization with hierarchical support
Relationships:
- Has many `Item` (ForeignKey)
- Self-referential for parent-child hierarchy

---

#### **Item Model** [core/models.py:77-119]
```python
Fields:
- title (CharField, max_length=100)
- price (DecimalField, max_digits=10, decimal_places=2)
- discount_price (DecimalField, blank=True)
- category (ForeignKey to Category)
- label (CharField, choices=['sale', 'new', 'promotion'], blank=True)
- slug (SlugField, unique=True)
- stock_no (CharField, max_length=10, unique=True)
- description_short (CharField, max_length=200, blank=True)
- description_long (TextField)
- image (ImageField, upload_to='products/')
- stock_quantity (PositiveIntegerField, default=0)
- weight (DecimalField, decimal_places=2, blank=True, help_text="kg")
- dimensions (CharField, max_length=50, blank=True, help_text="L x W x H in cm")
- sku (CharField, max_length=50, unique=True, blank=True)
- is_active (BooleanField, default=True)
- is_featured (BooleanField, default=False)
- view_count (PositiveIntegerField, default=0)
- seo_title (CharField, max_length=60, blank=True)
- seo_description (CharField, max_length=160, blank=True)
- created_at (DateTimeField)
- updated_at (DateTimeField, auto_now=True)

Methods:
- get_absolute_url() → Product detail page
- get_add_to_cart_url() → Add to cart endpoint
- get_remove_from_cart_url() → Remove from cart endpoint
```
Purpose: Main product/item in the catalog
Relationships:
- ForeignKey: Category
- Reverse FK: OrderItem (order__item)

---

#### **OrderItem Model** [core/models.py:122-145]
```python
Fields:
- user (ForeignKey to User)
- ordered (BooleanField, default=False)
- item (ForeignKey to Item)
- quantity (IntegerField, default=1)

Methods:
- get_total_item_price() → quantity * item.price
- get_total_discount_item_price() → quantity * item.discount_price
- get_amount_saved() → Regular - discount price
- get_final_price() → Returns discounted or regular price
```
Purpose: Represents a line item in an order
Relationships:
- ForeignKey: User, Item
- Reverse FK: Order (items__orderitem)

---

#### **Order Model** [core/models.py:147-187]
```python
Fields:
- user (ForeignKey to User)
- ref_code (CharField, max_length=20)
- items (ManyToManyField to OrderItem)
- start_date (DateTimeField, auto_now_add=True)
- ordered_date (DateTimeField)
- ordered (BooleanField, default=False)
- shipping_address (ForeignKey to BillingAddress)
- billing_address (ForeignKey to BillingAddress)
- payment (ForeignKey to Payment)
- coupon (ForeignKey to Coupon)
- being_delivered (BooleanField, default=False)
- received (BooleanField, default=False)
- refund_requested (BooleanField, default=False)
- refund_granted (BooleanField, default=False)

Methods:
- get_total() → Sum of items with coupon deduction
```
Purpose: Represents a customer order/purchase
Relationships:
- ForeignKey: User, BillingAddress (x2), Payment, Coupon
- M2M: OrderItem

---

#### **BillingAddress Model** [core/models.py:190-206]
```python
Fields:
- user (ForeignKey to User)
- street_address (CharField, max_length=100)
- apartment_address (CharField, max_length=100)
- city (CharField, max_length=100)
- country (CharField, max_length=100)
- zip (CharField, max_length=100)
- address_type (CharField, choices=['Billing', 'Shipping'])
- default (BooleanField, default=False)
```
Purpose: Billing and shipping addresses for orders
Relationships: ForeignKey to User

---

#### **Payment Model** [core/models.py:208-217]
```python
Fields:
- stripe_charge_id (CharField, max_length=50)
- user (ForeignKey to User)
- amount (FloatField)
- timestamp (DateTimeField, auto_now_add=True)
```
Purpose: Track payment transactions
Relationships: ForeignKey to User

---

#### **Coupon Model** [core/models.py:219-225]
```python
Fields:
- code (CharField, max_length=15)
- amount (FloatField)
```
Purpose: Discount coupons for orders
Relationships: Reverse FK from Order

---

#### **Refund Model** [core/models.py:227-239]
```python
Fields:
- order (ForeignKey to Order)
- reason (TextField)
- accepted (BooleanField, default=False)
- email (EmailField)
```
Purpose: Handle refund requests
Relationships: ForeignKey to Order

---

### 3.2 DASHBOARD/SITE MANAGEMENT MODELS

#### **SiteSettings Model** [core/models.py:243-301]
```python
Fields:
- site_name (CharField, default='Django Shop')
- site_email (EmailField)
- notification_email (EmailField, blank=True)
- whatsapp_number (CharField, blank=True)
- whatsapp_default_message (CharField)
- phone_number (CharField, blank=True)
- address (TextField, blank=True)
- hero_title (CharField, default='Solutions...')
- hero_subtitle (TextField)
- hero_cta_text (CharField)
- hero_cta_link (CharField)
- hero_badge_text (CharField)
- hero_secondary_cta_text (CharField)
- hero_secondary_cta_link (CharField)
- primary_color (CharField, default='#facc15')
- primary_hover_color (CharField, default='#eab308')
- secondary_color (CharField, default='#0a0a0a')
- facebook_url (URLField, blank=True)
- instagram_url (URLField, blank=True)
- twitter_url (URLField, blank=True)
- youtube_url (URLField, blank=True)
- linkedin_url (URLField, blank=True)
- logo (ImageField, upload_to='site/', blank=True)
- favicon (ImageField, upload_to='site/', blank=True)
- meta_description (CharField, max_length=160, blank=True)
- meta_keywords (CharField, max_length=255, blank=True)
- currency (CharField, default='FCFA')
- items_per_page (IntegerField, default=12)
- enable_reviews (BooleanField, default=True)
- enable_wishlist (BooleanField, default=True)
- updated_at (DateTimeField, auto_now=True)
```
Purpose: Global site configuration
Usage: Accessed in context processors, dashboard settings view

---

#### **SiteImage Model** [core/models.py:304-331]
```python
Fields:
- image_type (CharField, choices=[
    'top_carousel', 'banner', 'footer', 'hero', 'logo',
    'favicon', 'marketing', 'other'
  ])
- title (CharField, max_length=100)
- image (ImageField, upload_to='site-images/')
- description (TextField, blank=True)
- alt_text (CharField, max_length=100, blank=True)
- order (PositiveIntegerField, default=0)
- is_active (BooleanField, default=True)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)
```
Purpose: Manage site-wide images (banners, logos, etc.)
Usage: Templates reference these for dynamic images

---

#### **Contact Model** [core/models.py:334-350]
```python
Fields:
- name (CharField, max_length=100)
- email (EmailField)
- phone (CharField, max_length=20, blank=True)
- subject (CharField, max_length=200)
- message (TextField)
- is_read (BooleanField, default=False)
- replied_at (DateTimeField, blank=True)
- reply_message (TextField, blank=True)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)
```
Purpose: Store contact form submissions
Usage: Dashboard - Contacts Management

---

#### **Review Model** [core/models.py:354-379]
```python
Fields:
- item (ForeignKey to Item, related_name='reviews')
- user (ForeignKey to User)
- rating (IntegerField, choices=[(1,5)])
- title (CharField, max_length=200)
- comment (TextField)
- is_approved (BooleanField, default=False)
- admin_response (TextField, blank=True)
- helpful_count (IntegerField, default=0)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)

Constraints:
- unique_together = ('item', 'user') - One review per user per item
```
Purpose: Product reviews and ratings
Relationships: ForeignKey to Item, User

---

#### **Promotion Model** [core/models.py:381-415]
```python
Fields:
- code (CharField, max_length=50, unique=True)
- title (CharField, max_length=100)
- description (TextField, blank=True)
- discount_type (CharField, choices=['percentage', 'fixed'])
- discount_value (DecimalField)
- max_uses (IntegerField, blank=True)
- used_count (IntegerField, default=0)
- min_order_amount (DecimalField, default=0)
- items (ManyToManyField to Item, blank=True)
- is_active (BooleanField, default=True)
- start_date (DateTimeField)
- end_date (DateTimeField)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)

Methods:
- is_valid() → Checks date range, usage limits, status
```
Purpose: Promotional codes and discounts
Relationships: M2M to Item

---

#### **PageView Model** [core/models.py:420-436]
```python
Fields:
- path (CharField, max_length=500)
- date (DateField)
- count (PositiveIntegerField, default=0)

Methods:
- record(path) → Increments view count for today
```
Purpose: Track daily page views for analytics
Constraints: unique_together = ('path', 'date')

---

#### **UserProfile Model** [core/models.py:440-456]
```python
Fields:
- user (OneToOneField to User)
- avatar (ImageField, upload_to='avatars/', blank=True)

Methods:
- get_or_create_for_user() → Auto-create profile for user

Signal Handler:
- create_user_profile() → Auto-creates profile on User creation
```
Purpose: Extended user profile with avatar support
Relationships: OneToOneField to User

---

### 3.3 MODEL RELATIONSHIPS DIAGRAM

```
User (Django)
├── Order (1:N)
│   ├── OrderItem (M:N)
│   │   └── Item (1:N)
│   │       └── Category (1:N)
│   │       └── Review (1:N)
│   │           └── User (1:N)
│   ├── BillingAddress (1:N)
│   ├── Payment (1:N)
│   └── Coupon (N:1)
├── UserProfile (1:1)
├── Contact (1:N)
└── Review (1:N)

Category (Self-referential)
├── parent (Optional self-reference)
└── children (Reverse relation)

Item
├── Category (N:1)
├── Review (1:N)
└── Promotion (N:M)

SiteSettings (Singleton)
SiteImage
```

---

## 4. VIEWS & BUSINESS LOGIC

### 4.1 CORE APP VIEWS

**Location:** [core/views.py](core/views.py)

#### **Utility Functions**

**create_ref_code()** [Line 21]
```python
Returns: str (20-char random reference code)
Usage: Generate unique order reference codes
```

**build_order_email_message()** [Line 25]
```python
Parameters:
- order (Order object)
- email (str)
- city (str)
- notes (str, optional)

Returns: str (formatted email message)
Usage: Create HTML email for order notifications
```

#### **PaymentView** [View, POST/GET]
```
URL: /payment/<payment_option>/
Auth: LoginRequiredMixin
Methods:
- GET: Display payment confirmation page
- POST: Process payment, update order status
```

#### **HomeView** [ListView]
```
URL: /
Template: index.html
Context Variables:
- items: Featured items (or latest 8)
- latest_items: 8 most recent items

Logic:
1. Get featured items (is_featured=True)
2. If empty, return latest items
3. Pass both to template
```

#### **OrderSummaryView** [LoginRequiredMixin, View]
```
URL: /order-summary/
Auth: LoginRequired
Template: order_summary.html

GET Handler:
1. Get Order for current user (ordered=False)
2. Display checkout form with address fields
3. Context: form, order, coupon_form
```

#### **ShopView** [ListView, Paginated]
```
URL: /shop/
Template: shop.html
Paginate By: 6 items per page

Features:
- Filter by category (GET param: ?category=slug)
- Search items (GET param: ?q=search_term)
- Ordering: By creation date (newest first)

Search Fields:
- title (icontains)
- description_short (icontains)
- description_long (icontains)
```

#### **ItemDetailView** [DetailView]
```
URL: /product/<slug>/
Template: product-detail.html
Slug Field: slug

Logic:
1. Increment view_count atomically
2. Get related items from same category
3. Build WhatsApp share link if number available
4. Render detail page

Context:
- object: Item instance
- related_items: 4 related products
- product_whatsapp_link: WhatsApp share URL
```

#### **CategoryView** [View]
```
URL: /category/<slug>/
Template: category.html

Logic:
1. Get category by slug
2. Get all active items in category
3. Order by creation date (newest first)
4. Pass to template

Context:
- object_list: Items in category
- category_title: Category name
- category_description: Category description
- category_image: Category image
- selected_category: Current category slug
```

#### **CheckoutView** [LoginRequiredMixin, View]
```
URL: /checkout/
Auth: LoginRequired
Methods: GET, POST

GET:
1. Get active order for user
2. Display checkout form with address fields
3. Context: form, order, coupon_form

POST:
1. Validate form data
2. Create/save BillingAddress
3. Update Order with address & ref_code
4. Send notification emails (admin & customer)
5. Success message & redirect to home
```

#### **AddCouponView** [LoginRequiredMixin, View]
```
URL: /add_coupon/
Auth: LoginRequired
Methods: POST

POST:
1. Get order for user
2. Get coupon code from form
3. Check coupon exists and is valid
4. Add to order
5. Redirect to order summary
```

#### **RequestRefundView** [LoginRequiredMixin, View]
```
URL: /request-refund/
Auth: LoginRequired
Methods: GET, POST

GET: Display refund request form
POST:
1. Get order by reference code
2. Create Refund object
3. Validate email matches order
4. Set refund_requested = True on order
5. Success message
```

**Other Views (in core/views.py):**
- `add_to_cart()` - Add item to cart
- `remove_from_cart()` - Remove item completely
- `remove_single_item_from_cart()` - Reduce quantity

---

### 4.2 DASHBOARD VIEWS

**Location:** [dashboard/views.py](dashboard/views.py)  
**Auth:** LoginRequiredMixin + StaffRequiredMixin on all views

#### **DashboardHomeView** [View]
```
URL: /dashboard/
Template: dashboard/home.html

Statistics Displayed:
- total_products: Count of all items
- total_categories: Count of categories
- total_orders: Count of ordered orders
- total_revenue: Sum of ordered orders
- out_of_stock: Count where stock_quantity=0
- recent_orders: Last 5 orders ordered_date desc
- popular_items: Most sold items (Counter)

Logic:
1. Count total products/categories/orders
2. Calculate total revenue
3. Get latest orders
4. Count item sales across all orders
5. Get top 5 most sold items
```

#### **Product Management Views**

**ProductListView** [ListView, Paginated by 10]
```
URL: /dashboard/products/
Template: dashboard/products/list.html

Filters:
- search: By title or stock_no (icontains)
- category: by category_id
- status: 'active', 'inactive', 'stock'
```

**ProductCreateView** [CreateView]
```
URL: /dashboard/products/create/
Form: ItemForm
Template: dashboard/products/form.html
Success URL: /dashboard/products/
```

**ProductUpdateView** [UpdateView]
```
URL: /dashboard/products/<pk>/edit/
Form: ItemForm
Template: dashboard/products/form.html
```

**ProductDeleteView** [DeleteView]
```
URL: /dashboard/products/<pk>/delete/
Confirm Template: dashboard/products/confirm_delete.html
```

#### **Category Management Views**
- **CategoryListView** [ListView, paginate_by=15]
- **CategoryCreateView** [CreateView]
- **CategoryUpdateView** [UpdateView]
- **CategoryDeleteView** [DeleteView]

#### **Site Image Management Views**
- **SiteImageListView** [ListView, paginate_by=12]
  - Filter by image_type
- **SiteImageCreateView** [CreateView]
- **SiteImageUpdateView** [UpdateView]
- **SiteImageDeleteView** [DeleteView]

#### **Carousel Slides Management**
- **SlideListView** [ListView]
- **SlideCreateView** [CreateView]
- **SlideUpdateView** [UpdateView]
- **SlideDeleteView** [DeleteView]

#### **SiteSettingsView** [View]
```
URL: /dashboard/settings/
Template: dashboard/settings.html

GET: Load SiteSettings (get_or_create), display form
POST: Save updated settings, redirect with success message
```

#### **User Management Views**

**UserListView** [ListView, paginate_by=15]
```
URL: /dashboard/users/
Template: dashboard/users/list.html

Filters:
- search: By username, email, first_name (icontains)
Ordering: By date_joined descending
```

**UserDetailView** [DetailView]
```
URL: /dashboard/users/<pk>/
Template: dashboard/users/detail.html

Context:
- total_spent: Sum of all ordered orders for user

Logic:
1. Get user
2. Calculate total spent on orders
3. Pass to template with user details
```

**toggle_user_staff()** [Function View, POST]
```
URL: /dashboard/users/<pk>/toggle-staff/
Function: Toggle user.is_staff boolean
```

**toggle_user_active()** [Function View, POST]
```
URL: /dashboard/users/<pk>/toggle-active/
Function: Toggle user.is_active boolean
```

#### **Order Management Views**

**OrderListView** [ListView, paginate_by=10]
```
URL: /dashboard/orders/
Template: dashboard/orders/list.html

Filters:
- search: By ref_code, username, email (icontains)
```

**OrderDetailView** [DetailView]
```
URL: /dashboard/orders/<pk>/
Template: dashboard/orders/detail.html
```

**update_order_status()** [Function View, POST]
```
URL: /dashboard/orders/<pk>/update/
Function: Update being_delivered, received fields
```

#### **Contact Management Views**

**ContactListView** [ListView, paginate_by=15]
```
URL: /dashboard/contacts/
Template: dashboard/contacts/list.html
Ordering: By created_at descending
```

**ContactDetailView** [DetailView]
```
URL: /dashboard/contacts/<pk>/
Template: dashboard/contacts/detail.html

Logic:
1. Mark is_read=True if not already read
2. Display contact details
```

**delete_contact()** [Function View, POST]
```
URL: /dashboard/contacts/<pk>/delete/
Function: Delete contact record
```

**reply_contact()** [Function View, GET/POST]
```
URL: /dashboard/contacts/<pk>/reply/
GET: Display reply form
POST: Save reply_message, set replied_at timestamp
```

#### **Review Management Views**

**ReviewListView** [ListView, paginate_by=15]
```
URL: /dashboard/reviews/
Template: dashboard/reviews/list.html

Filters:
- status: 'approved' or 'pending'

Context:
- total_reviews: Count all reviews
- approved_reviews: Count is_approved=True
- pending_reviews: Count is_approved=False
```

**approve_review()** [Function View, POST]
```
URL: /dashboard/reviews/<pk>/approve/
Function: Set is_approved=True
```

**delete_review()** [Function View, POST]
```
URL: /dashboard/reviews/<pk>/delete/
Function: Delete review record
```

**respond_review()** [Function View, GET/POST]
```
URL: /dashboard/reviews/<pk>/respond/
GET: Display form with ReviewResponseForm
POST: Save admin_response field
```

#### **Promotion Management Views**

**PromotionListView** [ListView, paginate_by=15]
```
URL: /dashboard/promotions/
Template: dashboard/promotions/list.html
```

**PromotionCreateView** [CreateView]
```
URL: /dashboard/promotions/create/
Form: PromotionForm
Template: dashboard/promotions/form.html
```

**PromotionUpdateView** [UpdateView]
```
URL: /dashboard/promotions/<pk>/edit/
Form: PromotionForm
```

**PromotionDeleteView** [DeleteView]
```
URL: /dashboard/promotions/<pk>/delete/
```

#### **Analytics View**

**AnalyticsView** [View]
```
URL: /dashboard/analytics/
Template: dashboard/analytics.html

Data:
- Orders count per day (30 days)
- Revenue per day (30 days)
- Popular products
- Top customers
```

#### **Admin Profile View**

**AdminProfileView** [LoginRequiredMixin, View]
```
URL: /dashboard/profile/
Methods: GET, POST

GET: Display admin profile form
POST: Update admin UserProfile
```

---

## 5. URL PATTERNS & ROUTING

### 5.1 ROOT URL CONFIGURATION
**Location:** [demo/urls.py](demo/urls.py)

```python
Root Patterns:
- /admin/ → Redirects to /dashboard/ (custom admin disabled)
- /accounts/login/ → Custom login template
- /accounts/logout/ → Logout handler
- /accounts/signup/ → Signup page
- /dashboard/ → Includes dashboard.urls (app_name='dashboard')
- / → Includes core.urls (app_name='core')

Media & Static Files:
- /static/ → STATIC_ROOT (collectstatic output)
- /media/ → MEDIA_ROOT (user uploaded files)
```

---

### 5.2 CORE APP URLs
**Location:** [core/urls.py](core/urls.py)  
**Namespace:** `core`

| URL | View | Name | Auth |
|-----|------|------|------|
| `/` | HomeView | `home` | - |
| `/checkout/` | CheckoutView | `checkout` | LoginRequired |
| `/category/<slug>/` | CategoryView | `category` | - |
| `/product/<slug>/` | ItemDetailView | `product` | - |
| `/add-to-cart/<slug>/` | add_to_cart | `add-to-cart` | LoginRequired |
| `/add_coupon/` | AddCouponView | `add-coupon` | LoginRequired |
| `/remove-from-cart/<slug>/` | remove_from_cart | `remove-from-cart` | LoginRequired |
| `/shop/` | ShopView | `shop` | - |
| `/order-summary/` | OrderSummaryView | `order-summary` | LoginRequired |
| `/remove-item-from-cart/<slug>/` | remove_single_item_from_cart | `remove-single-item-from-cart` | LoginRequired |
| `/payment/<payment_option>/` | PaymentView | `payment` | LoginRequired |
| `/request-refund/` | RequestRefundView | `request-refund` | LoginRequired |

---

### 5.3 DASHBOARD URLs
**Location:** [dashboard/urls.py](dashboard/urls.py)  
**Namespace:** `dashboard`  
**Base URL:** `/dashboard/`

#### Dashboard Navigation  
| URL | View | Name | Purpose |
|-----|------|------|---------|
| `` | DashboardHomeView | `home` | Dashboard homepage |
| `profile/` | AdminProfileView | `profile` | Admin profile |
| `settings/` | SiteSettingsView | `settings` | Site configuration |
| `analytics/` | AnalyticsView | `analytics` | Analytics & reports |

#### Products Management (6 URLs)
| URL | View | Name |
|-----|------|------|
| `products/` | ProductListView | `products-list` |
| `products/create/` | ProductCreateView | `products-create` |
| `products/<pk>/edit/` | ProductUpdateView | `products-edit` |
| `products/<pk>/delete/` | ProductDeleteView | `products-delete` |

#### Categories Management (4 URLs)
| URL | View | Name |
|-----|------|------|
| `categories/` | CategoryListView | `categories-list` |
| `categories/create/` | CategoryCreateView | `categories-create` |
| `categories/<pk>/edit/` | CategoryUpdateView | `categories-edit` |
| `categories/<pk>/delete/` | CategoryDeleteView | `categories-delete` |

#### Site Images Management (4 URLs)
| URL | View | Name |
|-----|------|------|
| `images/` | SiteImageListView | `images-list` |
| `images/create/` | SiteImageCreateView | `images-create` |
| `images/<pk>/edit/` | SiteImageUpdateView | `images-edit` |
| `images/<pk>/delete/` | SiteImageDeleteView | `images-delete` |

#### Carousel Slides Management (4 URLs)
| URL | View | Name |
|-----|------|------|
| `slides/` | SlideListView | `slides-list` |
| `slides/create/` | SlideCreateView | `slides-create` |
| `slides/<pk>/edit/` | SlideUpdateView | `slides-edit` |
| `slides/<pk>/delete/` | SlideDeleteView | `slides-delete` |

#### Users Management (4 URLs)
| URL | View | Name |
|-----|------|------|
| `users/` | UserListView | `users-list` |
| `users/<pk>/` | UserDetailView | `users-detail` |
| `users/<pk>/toggle-staff/` | toggle_user_staff | `users-toggle-staff` |
| `users/<pk>/toggle-active/` | toggle_user_active | `users-toggle-active` |

#### Orders Management (3 URLs)
| URL | View | Name |
|-----|------|------|
| `orders/` | OrderListView | `orders-list` |
| `orders/<pk>/` | OrderDetailView | `orders-detail` |
| `orders/<pk>/update/` | update_order_status | `orders-update` |

#### Contacts Management (4 URLs)
| URL | View | Name |
|-----|------|------|
| `contacts/` | ContactListView | `contacts-list` |
| `contacts/<pk>/` | ContactDetailView | `contacts-detail` |
| `contacts/<pk>/delete/` | delete_contact | `contacts-delete` |
| `contacts/<pk>/reply/` | reply_contact | `contacts-reply` |

#### Reviews Management (4 URLs)
| URL | View | Name |
|-----|------|------|
| `reviews/` | ReviewListView | `reviews-list` |
| `reviews/<pk>/approve/` | approve_review | `reviews-approve` |
| `reviews/<pk>/delete/` | delete_review | `reviews-delete` |
| `reviews/<pk>/respond/` | respond_review | `reviews-respond` |

#### Promotions Management (4 URLs)
| URL | View | Name |
|-----|------|------|
| `promotions/` | PromotionListView | `promotions-list` |
| `promotions/create/` | PromotionCreateView | `promotions-create` |
| `promotions/<pk>/edit/` | PromotionUpdateView | `promotions-edit` |
| `promotions/<pk>/delete/` | PromotionDeleteView | `promotions-delete` |

---

## 6. FORMS & DATA VALIDATION

### 6.1 CORE FORMS
**Location:** [core/forms.py](core/forms.py)

#### **CheckoutForm**
```python
Fields:
- email (EmailField) - Customer email
- street_address (CharField) - Street address
- apartment_address (CharField, optional) - Apartment/suite
- country (CharField) - Country
- city (CharField) - City
- zip (CharField) - Postal code
- notes (CharField, optional, textarea) - Delivery notes

Usage: CheckoutView.post() for order checkout
Styling: Bootstrap form-control classes
```

#### **CouponForm**
```python
Fields:
- code (CharField) - Coupon/promotion code

Usage: AddCouponView for applying coupons
```

#### **RefundForm**
```python
Fields:
- ref_code (CharField) - Order reference code
- message (CharField, textarea) - Refund reason
- email (EmailField) - Requester email

Usage: RequestRefundView for refund processing
```

---

### 6.2 DASHBOARD FORMS
**Location:** [dashboard/forms.py](dashboard/forms.py)

#### **ItemForm** (ModelForm: Item)
```python
Fields:
- title, description_short, description_long
- price, discount_price
- category, image
- stock_quantity, stock_no, sku
- label, weight, dimensions
- is_active, is_featured
- seo_title, seo_description

Auto-features:
- Auto-generates slug from title if not present
- Uses form_control styling

Usage: ProductCreateView, ProductUpdateView
```

#### **CategoryForm** (ModelForm: Category)
```python
Fields:
- title, description
- image, parent (for hierarchy)
- is_active, order

Auto-features:
- Auto-generates slug from title
- Widget type selection for parent category

Usage: CategoryCreateView, CategoryUpdateView
```

#### **SiteSettingsForm** (ModelForm: SiteSettings)
```python
Fields (primary):
- site_name, site_email, notification_email
- whatsapp_number, whatsapp_default_message
- phone_number, address

Fields (social, branding):
- facebook_url, instagram_url, twitter_url
- youtube_url, linkedin_url
- logo, favicon

Fields (hero section):
- hero_title, hero_subtitle
- hero_cta_text, hero_cta_link
- hero_badge_text
- hero_secondary_cta_text, hero_secondary_cta_link

Fields (colors):
- primary_color, primary_hover_color, secondary_color

Fields (SEO, settings):
- meta_description, meta_keywords
- currency, items_per_page
- enable_reviews, enable_wishlist
```

#### **SiteImageForm** (ModelForm: SiteImage)
```python
Fields:
- image_type (choices: top_carousel, banner, footer, hero, logo, favicon, marketing, other)
- title, image, description, alt_text, order, is_active

Usage: SiteImageCreateView, SiteImageUpdateView
```

#### **ReviewResponseForm** (ModelForm: Review)
```python
Fields:
- is_approved (BooleanField)
- admin_response (TextField, blank=True)

Usage: respond_review() view for admin responses to reviews
```

#### **PromotionForm** (ModelForm: Promotion)
```python
Fields:
- code, title, description
- discount_type (percentage/fixed), discount_value
- max_uses, min_order_amount
- items (ManyToManyField, optional)
- start_date, end_date
- is_active

Usage: PromotionCreateView, PromotionUpdateView
```

---

## 7. TEMPLATES & FRONTEND

### 7.1 TEMPLATE STRUCTURE
**Location:** [templates/](templates)

#### Base Templates
- **base.html** - Main layout with header, footer, navigation
- **account/base.html** - Account pages layout
- **socialaccount/base.html** - Social auth layout

#### E-Commerce Templates
- **index.html** - Homepage with carousel, featured products
- **shop.html** - Product listing with filters
- **product-detail.html** - Individual product page
- **category.html** - Category product listing
- **cart.html** - Shopping cart
- **checkout.html** - Checkout form
- **order_summary.html** - Order review before payment
- **payment.html** - Payment processing
- **request_refund.html** - Refund request form

#### Account Templates
- **account/login.html** - Login page
- **account/signup.html** - Registration page
- **account/password_reset.html** - Password reset
- **account/profile.html** - User profile

#### Dashboard Templates
**Location:** [templates/dashboard/](templates/dashboard)

- **base.html** - Dashboard layout with sidebar navigation
- **home.html** - Dashboard homepage with statistics
- **analytics.html** - Analytics and charts

**Products Management:**
- **products/list.html** - Product listing with search/filters
- **products/form.html** - Product create/edit form
- **products/confirm_delete.html** - Delete confirmation

**Categories Management:**
- **categories/list.html** - Category listing
- **categories/form.html** - Category create/edit form
- **categories/confirm_delete.html** - Delete confirmation

**Images Management:**
- **images/list.html** - Image gallery
- **images/form.html** - Image upload/edit form
- **images/confirm_delete.html** - Delete confirmation

**Users Management:**
- **users/list.html** - User listing with search
- **users/detail.html** - User detail with order history

**Orders Management:**
- **orders/list.html** - Order listing
- **orders/detail.html** - Order detail with items

**Contacts Management:**
- **contacts/list.html** - Contact messages
- **contacts/detail.html** - Message detail
- **contacts/reply.html** - Reply to message

**Reviews Management:**
- **reviews/list.html** - Reviews listing
- **reviews/respond.html** - Respond to review

**Promotions Management:**
- **promotions/list.html** - Promotions listing
- **promotions/form.html** - Promotion create/edit
- **promotions/confirm_delete.html** - Delete confirmation

**Settings:**
- **settings.html** - Site-wide settings form

---

## 8. STATIC FILES & ASSETS

### 8.1 STATIC FILE STRUCTURE
**Development:** [static_in_env/](static_in_env)  
**Production:** [static_root/](static_root) (after collectstatic)

#### CSS Files
- **main.css** - Main stylesheet
- **util.css** - Utility classes
- **main.min.css** - Minified main CSS
- **util.min.css** - Minified utilities

#### JavaScript Files
- **main.js** - Main JavaScript
- **main.min.js** - Minified main JS
- **map-custom.js** - Map functionality
- **slick-custom.js** - Carousel/slider functionality

#### Fonts
**Location:** [static_in_env/fonts/](static_in_env/fonts)
- **elegant-font/** - Elegant icons
- **font-awesome-4.7.0/** - Font Awesome icons
- **ionicons-2.0.1/** - Ionicons
- **Linearicons-Free-v1.0.0/** - Linear icons
- **montserrat/** - Montserrat font
- **poppins/** - Poppins font
- **themify/** - Themify icons

#### Vendor Libraries
**Location:** [static_in_env/vendor/](static_in_env/vendor)
- **animate/** - Animation library
- **animsition/** - Page transition effects
- **countdowntime/** - Countdown timer
- **css-hamburgers/** - Hamburger menu animations
- **daterangepicker/** - Date range picker
- **isotope/** - Filtering/sorting library
- **jquery/** - jQuery library
- **jqueryui/** - jQuery UI components
- **lightbox2/** - Image lightbox
- **noui/** - NoUI sliders
- **parallax100/** - Parallax scrolling
- **perfect-scrollbar/** - Custom scrollbars
- **select2/** - Enhanced select dropdowns
- **slick/** - Carousel/slider library
- **sweetalert/** - Alert dialogs

#### Images
**Location:** [static_in_env/images/](static_in_env/images)
- **icons/** - Icon images
- **includes/** - Template includes

---

## 9. SETTINGS & CONFIGURATION

### 9.1 DJANGO SETTINGS
**Location:** [demo/settings.py](demo/settings.py)

#### Core Django Settings
```python
DEBUG = True
SECRET_KEY = 'your-secret-key'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'django_countries',
    
    # Local apps
    'core',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.CartMiddleware',
]

ROOT_URLCONF = 'demo.urls'
```

#### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### Static & Media Files
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static_in_env']
STATIC_ROOT = BASE_DIR / 'static_root'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media_root'
```

#### Authentication Settings
```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
```

#### Email Configuration
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

#### Third-party App Settings
```python
CRISPY_TEMPLATE_PACK = 'bootstrap4'
SITE_ID = 1

# Stripe Payment Settings
STRIPE_PUBLIC_KEY = 'pk_test_...'
STRIPE_SECRET_KEY = 'sk_test_...'
```

---

## 10. MIDDLEWARE & CUSTOM CODE

### 10.1 CUSTOM MIDDLEWARE
**Location:** [core/middleware.py](core/middleware.py)

#### **CartMiddleware**
```python
class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Create cart session if not exists
        if 'cart' not in request.session:
            request.session['cart'] = {}
        
        # Add cart methods to request
        request.cart = Cart(request.session['cart'])
        
        response = self.get_response(request)
        return response
```

### 10.2 CONTEXT PROCESSORS
**Location:** [core/context_processors.py](core/context_processors.py)

#### **site_settings**
```python
def site_settings(request):
    """Add site settings to all template contexts"""
    from core.models import SiteSettings
    
    try:
        settings = SiteSettings.objects.get()
    except SiteSettings.DoesNotExist:
        settings = None
    
    return {'site_settings': settings}
```

#### **cart_count**
```python
def cart_count(request):
    """Add cart item count to all template contexts"""
    if hasattr(request, 'cart'):
        return {'cart_count': request.cart.get_total_items()}
    return {'cart_count': 0}
```

### 10.3 MANAGEMENT COMMANDS
**Location:** [core/management/commands/](core/management/commands)

#### **makesuper.py**
```python
# Create superuser programmatically
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write('Superuser created successfully')
```

#### **rename.py**
```python
# Utility command for renaming files
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('old_name', type=str)
        parser.add_argument('new_name', type=str)
    
    def handle(self, *args, **options):
        # Implementation for renaming files
        pass
```

---

## 11. MANAGEMENT COMMANDS

### 11.1 AVAILABLE COMMANDS

#### Django Built-in Commands
- `python manage.py runserver` - Start development server
- `python manage.py makemigrations` - Create database migrations
- `python manage.py migrate` - Apply database migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py collectstatic` - Collect static files
- `python manage.py shell` - Interactive Python shell

#### Custom Commands
- `python manage.py makesuper` - Create default superuser
- `python manage.py rename <old> <new>` - Rename utility

---

## 12. TESTING & DOCUMENTATION

### 12.1 TEST FILES
**Location:** [core/tests.py](core/tests.py)

#### **Model Tests**
```python
from django.test import TestCase
from core.models import Item, Category

class ItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title='Test Category',
            slug='test-category'
        )
    
    def test_item_creation(self):
        item = Item.objects.create(
            title='Test Item',
            price=100.00,
            category=self.category
        )
        self.assertEqual(item.title, 'Test Item')
        self.assertEqual(str(item), 'Test Item')
```

### 12.2 DOCUMENTATION FILES

#### **README.md**
- Project overview
- Installation instructions
- Usage guide
- Contributing guidelines

#### **DASHBOARD_README.md**
- Dashboard features
- URL reference
- Template structure
- Customization guide

#### **INSTALLATION_INSTRUCTIONS.md**
- Step-by-step setup
- Requirements installation
- Database setup
- Deployment guide

#### **BEST_PRACTICES.md**
- Django best practices used
- Code patterns
- Performance optimizations
- Security considerations

#### **DASHBOARD_URL_REFERENCE.md**
- Complete URL mapping
- View-function relationships
- Authentication requirements

#### **IMPLEMENTATION_SUMMARY.md**
- Project completion summary
- Feature checklist
- Code statistics
- Final status

#### **test_dashboard.py**
- Automated testing script
- Configuration validation
- Model/view/form checks

#### **setup_dashboard.py**
- Automated setup script
- Migration runner
- Initial data creation

---

## 📊 CODE STATISTICS

| Component | Files | Lines | Description |
|-----------|-------|-------|-------------|
| **Models** | 1 | 450+ | 12 models with relationships |
| **Views** | 2 | 700+ | 30+ views (core + dashboard) |
| **Forms** | 2 | 300+ | 8 forms with validation |
| **URLs** | 2 | 80+ | 40+ URL patterns |
| **Templates** | 25+ | 2000+ | HTML with Bootstrap |
| **Static Files** | 50+ | 5000+ | CSS/JS/Images/Fonts |
| **Settings** | 1 | 150+ | Django configuration |
| **Tests** | 2 | 100+ | Unit tests + validation |
| **Documentation** | 8 | 1500+ | Complete documentation |

---

## 🚀 QUICK START GUIDE

### 1. Environment Setup
```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 3. Run Tests
```bash
# Run automated tests
python test_dashboard.py
```

### 4. Start Server
```bash
# Start development server
python manage.py runserver
```

### 5. Access Application
- **Frontend:** http://localhost:8000/
- **Dashboard:** http://localhost:8000/dashboard/
- **Admin:** http://localhost:8000/admin/

---

## 🔧 DEVELOPMENT WORKFLOW

### Adding New Features
1. **Models:** Create/update models in `core/models.py`
2. **Migrations:** `python manage.py makemigrations core`
3. **Views:** Add views in appropriate app
4. **URLs:** Register URLs in app's urls.py
5. **Templates:** Create HTML templates
6. **Forms:** Create ModelForms if needed
7. **Test:** Run `python test_dashboard.py`

### Code Style
- **PEP 8** compliant Python code
- **Django conventions** for views, models, URLs
- **Bootstrap 4** for responsive design
- **Font Awesome** for icons
- **Consistent naming** throughout

---

## 🔐 SECURITY FEATURES

- **CSRF protection** on all forms
- **Authentication required** for sensitive operations
- **Staff-only access** for dashboard
- **SQL injection prevention** via ORM
- **XSS protection** in templates
- **Secure password hashing**
- **Session security** with proper settings

---

## 📈 PERFORMANCE OPTIMIZATIONS

- **Database indexing** on frequently queried fields
- **Query optimization** with select_related/prefetch_related
- **Pagination** on large datasets
- **Static file caching** with versioning
- **Image optimization** with proper formats
- **Lazy loading** for non-critical content

---

**Generated:** April 28, 2026  
**Status:** ✅ COMPLETE - Ready for development tasks  
**Contact:** Ready to receive task assignments
