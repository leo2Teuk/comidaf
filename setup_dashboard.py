#!/usr/bin/env python
"""
Script de configuration initial du Dashboard E-Commerce
Exécutez ce script après avoir installé le projet
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model
from core.models import SiteSettings

def install_dashboard():
    """Effectue l'installation complète du dashboard"""
    
    print("=" * 60)
    print("🚀 Configuration du Dashboard E-Commerce")
    print("=" * 60)
    
    # Step 1: Migrations
    print("\n[1/4] Application des migrations...")
    try:
        call_command('migrate')
        print("✅ Migrations appliquées avec succès")
    except Exception as e:
        print(f"❌ Erreur lors des migrations: {e}")
        return False
    
    # Step 2: Create Site Settings
    print("\n[2/4] Création des paramètres du site...")
    try:
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        if created:
            settings.site_name = "Django Shop"
            settings.site_email = "contact@djangoshop.com"
            settings.currency = "USD"
            settings.save()
            print("✅ Paramètres du site créés")
        else:
            print("ℹ️  Paramètres du site déjà existants")
    except Exception as e:
        print(f"⚠️  Impossible créer les paramètres: {e}")
    
    # Step 3: Create superuser if none exists
    print("\n[3/4] Vérification du compte administrateur...")
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        print("Aucun superutilisateur trouvé.")
        print("Vous devez créer un compte administrateur avec:")
        print("  python manage.py createsuperuser")
    else:
        print("✅ Compte administrateur trouvé")
    
    # Step 4: Collect static files
    print("\n[4/4] Collecte des fichiers statiques...")
    try:
        call_command('collectstatic', '--noinput')
        print("✅ Fichiers statiques collectés")
    except Exception as e:
        print(f"⚠️  Erreur lors de la collecte: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Installation complétée avec succès!")
    print("=" * 60)
    print("\n📝 Prochaines étapes:")
    print("  1. Apportez les modifisations à coremodels.py (si nécessaire)")
    print("  2. Exécutez: python manage.py makemigrations core")
    print("  3. Créez un compte admin: python manage.py createsuperuser")
    print("  4. Démarrez le serveur: python manage.py runserver")
    print("  5. Accédez au dashboard: http://localhost:8000/dashboard/")
    print("\n💡 Console Admin: http://localhost:8000/admin/")
    return True

def check_installation():
    """Vérifie que tout est correctement installé"""
    
    print("\n🔍 Vérification de l'installation...\n")
    
    checks = {
        "Dashboard App": lambda: 'dashboard' in __import__('django.conf').conf.settings.INSTALLED_APPS,
        "Core App": lambda: 'core' in __import__('django.conf').conf.settings.INSTALLED_APPS,
        "Database": lambda: User.objects.count() >= 0,
        "SiteSettings": lambda: SiteSettings.objects.exists(),
    }
    
    all_ok = True
    for check_name, check_func in checks.items():
        try:
            result = check_func()
            status = "✅" if result else "⚠️"
            print(f"{status} {check_name}")
        except Exception as e:
            print(f"❌ {check_name}: {e}")
            all_ok = False
    
    return all_ok

if __name__ == "__main__":
    User = get_user_model()
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_installation()
    else:
        success = install_dashboard()
        if success:
            check_installation()
