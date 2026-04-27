"""
Script de test et vérification du Dashboard
Exécutez: python test_dashboard.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from django.urls import reverse, get_resolver
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_urls():
    """Vérifie que toutes les URLs du dashboard sont configurées"""
    
    print("\n" + "="*60)
    print("🔍 TEST DES URLS DU DASHBOARD")
    print("="*60 + "\n")
    
    urls_to_test = [
        ('dashboard:home', 'Dashboard Home'),
        ('dashboard:products-list', 'Products List'),
        ('dashboard:products-create', 'Product Create'),
        ('dashboard:categories-list', 'Categories List'),
        ('dashboard:categories-create', 'Category Create'),
        ('dashboard:images-list', 'Images List'),
        ('dashboard:images-create', 'Image Create'),
        ('dashboard:settings', 'Settings'),
        ('dashboard:users-list', 'Users List'),
        ('dashboard:orders-list', 'Orders List'),
        ('dashboard:contacts-list', 'Contacts List'),
        ('dashboard:reviews-list', 'Reviews List'),
        ('dashboard:promotions-list', 'Promotions List'),
        ('dashboard:promotions-create', 'Promotion Create'),
        ('dashboard:analytics', 'Analytics'),
    ]
    
    all_ok = True
    for url_name, label in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {label:30} -> {url}")
        except Exception as e:
            print(f"❌ {label:30} ERROR: {e}")
            all_ok = False
    
    return all_ok

def test_models():
    """Vérifie que tous les modèles existent"""
    
    print("\n" + "="*60)
    print("🔍 TEST DES MODÈLES")
    print("="*60 + "\n")
    
    try:
        from core.models import (
            Item, Category, Order, SiteSettings, 
            SiteImage, Contact, Review, Promotion
        )
        
        models = [
            ('Item', Item),
            ('Category', Category),
            ('Order', Order),
            ('SiteSettings', SiteSettings),
            ('SiteImage', SiteImage),
            ('Contact', Contact),
            ('Review', Review),
            ('Promotion', Promotion),
        ]
        
        all_exist = True
        for name, model in models:
            try:
                count = model.objects.count()
                print(f"✅ {name:20} exists ({count} records)")
            except Exception as e:
                print(f"❌ {name:20} ERROR: {e}")
                all_exist = False
        
        return all_exist
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_installed():
    """Vérifie que l'app dashboard est installée"""
    
    print("\n" + "="*60)
    print("🔍 TEST DE CONFIGURATION")
    print("="*60 + "\n")
    
    from django.conf import settings
    
    checks = {
        "Dashboard app installed": 'dashboard' in settings.INSTALLED_APPS,
        "Core app installed": 'core' in settings.INSTALLED_APPS,
        "Allauth installed": 'allauth' in settings.INSTALLED_APPS,
    }
    
    all_ok = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
        if not result:
            all_ok = False
    
    return all_ok

def test_admin_registered():
    """Vérifie que les modèles sont enregistrés dans l'admin"""
    
    print("\n" + "="*60)
    print("🔍 TEST DE L'ADMIN DJANGO")
    print("="*60 + "\n")
    
    from django.contrib import admin
    from core.models import (
        SiteSettings, SiteImage, Contact, Review, Promotion
    )
    
    models_to_check = [
        ('SiteSettings', SiteSettings),
        ('SiteImage', SiteImage),
        ('Contact', Contact),
        ('Review', Review),
        ('Promotion', Promotion),
    ]
    
    all_registered = True
    for name, model in models_to_check:
        is_registered = model in admin.site._registry
        status = "✅" if is_registered else "❌"
        print(f"{status} {name:20} registered in admin")
        if not is_registered:
            all_registered = False
    
    return all_registered

def test_views_exist():
    """Vérifie que les vues existent"""
    
    print("\n" + "="*60)
    print("🔍 TEST DES VUES")
    print("="*60 + "\n")
    
    try:
        from dashboard import views
        
        view_classes = [
            'DashboardHomeView',
            'ProductListView', 'ProductCreateView', 'ProductUpdateView', 'ProductDeleteView',
            'CategoryListView', 'CategoryCreateView', 'CategoryUpdateView', 'CategoryDeleteView',
            'SiteImageListView', 'SiteImageCreateView', 'SiteImageUpdateView', 'SiteImageDeleteView',
            'SiteSettingsView',
            'UserListView', 'UserDetailView',
            'OrderListView', 'OrderDetailView',
            'ContactListView', 'ContactDetailView',
            'ReviewListView',
            'PromotionListView', 'PromotionCreateView', 'PromotionUpdateView', 'PromotionDeleteView',
            'AnalyticsView',
        ]
        
        missing = []
        for view_name in view_classes:
            if not hasattr(views, view_name):
                missing.append(view_name)
        
        if missing:
            for view in missing:
                print(f"❌ {view} NOT FOUND")
            return False
        else:
            print(f"✅ All {len(view_classes)} views found")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_forms_exist():
    """Vérifie que les formulaires existent"""
    
    print("\n" + "="*60)
    print("🔍 TEST DES FORMULAIRES")
    print("="*60 + "\n")
    
    try:
        from dashboard import forms
        
        form_classes = [
            'ItemForm',
            'CategoryForm',
            'SiteSettingsForm',
            'SiteImageForm',
            'ReviewResponseForm',
            'PromotionForm',
        ]
        
        missing = []
        for form_name in form_classes:
            if not hasattr(forms, form_name):
                missing.append(form_name)
        
        if missing:
            for form in missing:
                print(f"❌ {form} NOT FOUND")
            return False
        else:
            print(f"✅ All {len(form_classes)} forms found")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Exécute tous les tests"""
    
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "TESTS DU DASHBOARD" + " "*25 + "║")
    print("╚" + "="*58 + "╝")
    
    results = {
        "Configuration": test_app_installed(),
        "URLs": test_urls(),
        "Modèles": test_models(),
        "Vues": test_views_exist(),
        "Formulaires": test_forms_exist(),
        "Admin": test_admin_registered(),
    }
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60 + "\n")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} -> {test_name}")
    
    all_pass = all(results.values())
    
    print("\n" + "="*60)
    if all_pass:
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("\nVous êtes prêt à:")
        print("  1. Exécuter: python manage.py makemigrations")
        print("  2. Exécuter: python manage.py migrate")
        print("  3. Créer admin: python manage.py createsuperuser")
        print("  4. Démarrer: python manage.py runserver")
        print("  5. Accéder: http://localhost:8000/dashboard/")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez l'installation et les fichiers")
    print("="*60 + "\n")
    
    return all_pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
