# Instructions d'installation et d'exécution du Dashboard

## 1️⃣ INSTALLATION INITIALE

### Étape 1: Appliquer les migrations

```bash
python manage.py makemigrations core
python manage.py migrate
```

### Étape 2: Créer un compte administrateur (si vous n'en avez pas)

```bash
python manage.py createsuperuser
```

Entrez:
- Username: admin
- Email: admin@example.com
- Password: votreMotDePasse

### Étape 3: Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### Étape 4: Démarrer le serveur

```bash
python manage.py runserver
```

---

## 2️⃣ ACCÈS AU DASHBOARD

### Pour le premier accès:

1. Allez sur http://localhost:8000/admin/
2. Connectez-vous avec vos identifiants d'administrateur
3. Allez à http://localhost:8000/dashboard/

### ⚠️ Important

Vous DEVEZ être un utilisateur staff pour accéder au dashboard.

Si votre compte n'a pas accès:
1. Allez à http://localhost:8000/admin/auth/user/
2. Cliquez sur votre nom d'utilisateur
3. Cochez "Staff status"
4. Cliquez sur "Enregistrer"

---

## 3️⃣ STRUCTURE DES MODULES

### Dashboard Module URLs:

| Fonction | URL |
|----------|-----|
| Accueil du Dashboard | `/dashboard/` |
| **Produits** | 
| - Liste | `/dashboard/products/` |
| - Créer | `/dashboard/products/create/` |
| - Modifier | `/dashboard/products/<id>/edit/` |
| - Supprimer | `/dashboard/products/<id>/delete/` |
| **Catégories** | 
| - Liste | `/dashboard/categories/` |
| - Créer | `/dashboard/categories/create/` |
| - Modifier | `/dashboard/categories/<id>/edit/` |
| - Supprimer | `/dashboard/categories/<id>/delete/` |
| **Images Site** | 
| - Liste | `/dashboard/images/` |
| - Ajouter | `/dashboard/images/create/` |
| - Modifier | `/dashboard/images/<id>/edit/` |
| - Supprimer | `/dashboard/images/<id>/delete/` |
| **Paramètres Globaux** | `/dashboard/settings/` |
| **Utilisateurs** | 
| - Liste | `/dashboard/users/` |
| - Détails | `/dashboard/users/<id>/` |
| - Toggle Admin | `/dashboard/users/<id>/toggle-staff/` |
| - Toggle Actif | `/dashboard/users/<id>/toggle-active/` |
| **Commandes** | 
| - Liste | `/dashboard/orders/` |
| - Détails | `/dashboard/orders/<id>/` |
| - Mettre à jour | `/dashboard/orders/<id>/update/` |
| **Messages Contact** | 
| - Liste | `/dashboard/contacts/` |
| - Détails | `/dashboard/contacts/<id>/` |
| - Répondre | `/dashboard/contacts/<id>/reply/` |
| - Supprimer | `/dashboard/contacts/<id>/delete/` |
| **Avis Produits** | 
| - Liste | `/dashboard/reviews/` |
| - Approuver | `/dashboard/reviews/<id>/approve/` |
| - Répondre | `/dashboard/reviews/<id>/respond/` |
| - Supprimer | `/dashboard/reviews/<id>/delete/` |
| **Promotions/Codes Promo** | 
| - Liste | `/dashboard/promotions/` |
| - Créer | `/dashboard/promotions/create/` |
| - Modifier | `/dashboard/promotions/<id>/edit/` |
| - Supprimer | `/dashboard/promotions/<id>/delete/` |
| **Analytics** | `/dashboard/analytics/` |

---

## 4️⃣ FEATURES PAR MODULE

### 🏠 Dashboard Home
- ✅ Statistiques globales
- ✅ Alertes rupture de stock
- ✅ Commandes récentes
- ✅ Produits populaires
- ✅ Actions rapides

### 📦 Gestion Produits
- ✅ Ajouter/Modifier/Supprimer produits
- ✅ Gestion stock
- ✅ Tarification (prix + prix réduit)
- ✅ Catégories
- ✅ Images
- ✅ Métadonnées SEO
- ✅ Filtrage et recherche
- ✅ Pagination

### 📁 Gestion Catégories
- ✅ CRUD complet
- ✅ Support sous-catégories
- ✅ Images de catégorie
- ✅ Gestion de l'ordre
- ✅ Statut actif/inactif

### 🖼️ Gestion Images Site
- ✅ Upload images
- ✅ Types variés (bannière, hero, logo, etc.)
- ✅ Filtrage par type
- ✅ Alt text SEO
- ✅ Ordre personnalisé

### ⚙️ Paramètres Site
- ✅ Informations générales
- ✅ Emails et numéros
- ✅ Réseaux sociaux
- ✅ Logo/Favicon
- ✅ SEO meta tags
- ✅ Configuration fonctionnalités

### 👥 Gestion Utilisateurs
- ✅ Liste complète
- ✅ Détails utilisateur
- ✅ Rôles (admin/client)
- ✅ Activation/Désactivation
- ✅ Historique commandes

### 🛒 Gestion Commandes
- ✅ Liste des commandes
- ✅ Détails complets
- ✅ Images produits
- ✅ Client info
- ✅ Adresses
- ✅ Status update (en attente/livraison/reçue)
- ✅ Totaux

### 💬 Gestion Messages
- ✅ Affichage messages
- ✅ Statut lecture
- ✅ Système de réponse
- ✅ Suppression

### ⭐ Gestion Avis
- ✅ Liste avis
- ✅ Filtrage (approuvé/attente)
- ✅ Approbation
- ✅ Réponses admin
- ✅ Statistiques

### 🏷️ Gestion Promotions
- ✅ Codes promo
- ✅ Types réductions
- ✅ Limites utilisation
- ✅ Péri dates
- ✅ Produits spécifiques

### 📊 Analytics
- ✅ Graphiques commandes
- ✅ Graphiques revenus
- ✅ Produits populaires
- ✅ Données 30 jours

---

## 5️⃣ STRUCTURE DES FICHIERS

```
dashboard/
├── migrations/
│   └── __init__.py
├── templates/dashboard/
│   ├── base.html
│   ├── home.html
│   ├── settings.html
│   ├── analytics.html
│   ├── products/
│   │   ├── list.html
│   │   ├── form.html
│   │   └── confirm_delete.html
│   ├── categories/
│   │   ├── list.html
│   │   ├── form.html
│   │   └── confirm_delete.html
│   ├── images/
│   │   ├── list.html
│   │   ├── form.html
│   │   └── confirm_delete.html
│   ├── users/
│   │   ├── list.html
│   │   └── detail.html
│   ├── orders/
│   │   ├── list.html
│   │   └── detail.html
│   ├── contacts/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── reply.html
│   ├── reviews/
│   │   ├── list.html
│   │   └── respond.html
│   └── promotions/
│       ├── list.html
│       ├── form.html
│       └── confirm_delete.html
├── forms.py
├── urls.py
├── views.py
├── apps.py
└── admin.py

core/
├── models.py (Extended with SiteSettings, SiteImage, Contact, Review, Promotion)
├── admin.py
├── forms.py
└── migrations/
    └── 0011_add_dashboard_models.py
```

---

## 6️⃣ COMMANDES UTILES

```bash
# Créer migrations
python manage.py makemigrations

# Appliquer migrations
python manage.py migrate

# Superutilisateur
python manage.py createsuperuser

# Démarrer serveur
python manage.py runserver

# Accès shell Django
python manage.py shell

# Collect static
python manage.py collectstatic

# Flush data
python manage.py flush

# Tests
python manage.py test
```

---

## 7️⃣ DÉPANNAGE

### ❌ "Module not found: dashboard"
**Solution**: Assurez-vous que `dashboard` est dans INSTALLED_APPS dans settings.py

### ❌ "Permission denied" au dashboard
**Solution**: 
1. Allez à /admin/
2. Éditez votre utilisateur
3. Cochez "Staff status"

### ❌ Images ne s'affichent pas
**Solution**:
- Vérifiez DEBUG = True en développement
- Vérifiez les chemins MEDIA_URL et MEDIA_ROOT
- Exécutez: `python manage.py collectstatic`

### ❌ "No such table" errors
**Solution**: Exécutez `python manage.py migrate`

### ❌ Port 8000 déjà utilisé
**Solution**: `python manage.py runserver 8001`

---

## 8️⃣ CONSEIL & BONNES PRATIQUES

✅ Créez un compte admin dédié
✅ Utilisez des mots de passe forts
✅ Sauvegardez votre base de données régulièrement
✅ Testez sur une copie avant la production
✅ Utilisez HTTPS en production
✅ Configurez EMAIL_BACKEND pour les notifications
✅ Optimisez les images avant upload
✅ Monitorez les performances

---

**C'est prêt! Commencez par étape 1️⃣ pour une installation complète.**
