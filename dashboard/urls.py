from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard Home
    path('', views.DashboardHomeView.as_view(), name='home'),
    
    # Products Management
    path('products/', views.ProductListView.as_view(), name='products-list'),
    path('products/create/', views.ProductCreateView.as_view(), name='products-create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='products-edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='products-delete'),
    
    # Categories Management
    path('categories/', views.CategoryListView.as_view(), name='categories-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='categories-create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='categories-edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='categories-delete'),
    
    # Site Images Management
    path('images/', views.SiteImageListView.as_view(), name='images-list'),
    path('images/create/', views.SiteImageCreateView.as_view(), name='images-create'),
    path('images/<int:pk>/edit/', views.SiteImageUpdateView.as_view(), name='images-edit'),
    path('images/<int:pk>/delete/', views.SiteImageDeleteView.as_view(), name='images-delete'),
    
    # Site Settings
    path('settings/', views.SiteSettingsView.as_view(), name='settings'),
    
    # Users Management
    path('users/', views.UserListView.as_view(), name='users-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='users-detail'),
    path('users/<int:pk>/toggle-staff/', views.toggle_user_staff, name='users-toggle-staff'),
    path('users/<int:pk>/toggle-active/', views.toggle_user_active, name='users-toggle-active'),
    
    # Orders Management
    path('orders/', views.OrderListView.as_view(), name='orders-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='orders-detail'),
    path('orders/<int:pk>/update/', views.update_order_status, name='orders-update'),
    
    # Contacts Management
    path('contacts/', views.ContactListView.as_view(), name='contacts-list'),
    path('contacts/<int:pk>/', views.ContactDetailView.as_view(), name='contacts-detail'),
    path('contacts/<int:pk>/delete/', views.delete_contact, name='contacts-delete'),
    path('contacts/<int:pk>/reply/', views.reply_contact, name='contacts-reply'),
    
    # Reviews Management
    path('reviews/', views.ReviewListView.as_view(), name='reviews-list'),
    path('reviews/<int:pk>/approve/', views.approve_review, name='reviews-approve'),
    path('reviews/<int:pk>/delete/', views.delete_review, name='reviews-delete'),
    path('reviews/<int:pk>/respond/', views.respond_review, name='reviews-respond'),
    
    # Promotions Management
    path('promotions/', views.PromotionListView.as_view(), name='promotions-list'),
    path('promotions/create/', views.PromotionCreateView.as_view(), name='promotions-create'),
    path('promotions/<int:pk>/edit/', views.PromotionUpdateView.as_view(), name='promotions-edit'),
    path('promotions/<int:pk>/delete/', views.PromotionDeleteView.as_view(), name='promotions-delete'),
    
    # Analytics
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
]
