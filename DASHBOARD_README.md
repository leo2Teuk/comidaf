# Dashboard E-Commerce Django - Guide d'Installation et Utilisation

## 📋 Vue d'ensemble

Ce dashboard est un système complet de gestion d'e-commerce construit avec Django. Il offre une interface moderne pour gérer tous les aspects de votre boutique en ligne.

## ✨ Fonctionnalités Implémentées

### 1. **Tableau de Bord (Dashboard Home)**
- Statistiques en temps réel (produits, catégories, commandes, revenus)
- Alertes pour les ruptures de stock
- Commandes récentes
- Produits populaires
- Actions rapides

### 2. **Gestion des Produits**
- CRUD complet (Créer, Lire, Mettre à jour, Supprimer)
- Liste avec pagination et filtrage
- Recherche par nom et numéro de stock
- Informations complètes (prix, stock, images, SEO)
- Statut actif/inactif
- Prix réduit supporté

### 3. **Gestion des Catégories**
- CRUD complet
- Support des sous-catégories (hiérarchie parent/enfant)
- Images de catégorie
- Gestion de l'ordre

### 4. **Gestion des Images Site**
- Upload d'images pour différents types (bannière, hero, logo, etc.)
- Galerie avec filtrage par type
- Alt text pour SEO
- Activation/désactivation des images

### 5. **Paramètres du Site**
- Configuration complète du site
- Réseaux sociaux
-Logo et favicon
- Paramètres SEO
- Configuration des fonctionnalités

### 6. **Gestion des Utilisateurs**
- Liste des utilisateurs
- Détails par utilisateur
- Historique des commandes
- Gestion des rôles (admin/client)
- Activation/désactivation de comptes

### 7. **Gestion des Commandes**
- Liste des commandes avec recherche
- Détails complets de chaque commande
- Mise à jour du statut (en attente, en livraison, reçue)
- Détails client et adresses
- Récapitulatif du total

### 8. **Gestion des Messages/Contact**
- Affichage des messages de contact
- Marquage comme lu/non lu
- Réponse aux messages
- Suppression de messages

### 9. **Gestion des Avis**
- Liste des avis avec filtrage (approuvé/en attente)
- Approbation des avis
- Réponses admin aux avis
- Suppression d'avis
- Statistiques des avis

### 10. **Gestion des Promotions**
- Création de codes promo
- Types de réductions (pourcentage ou montant fixe)
- Limitation du nombre d'utilisations
- Montant minimum pour appliquer
- Produits spécifiques ou tous les produits
- Périodes de validité

### 11. **Analytics**
- Graphiques des commandes par jour
- Graphiques des revenus par jour
- Produits populaires
- Données sur 30 jours

### 12. **Authentification & Sécurité**
- LoginRequired sur tous les dashboards
- StaffRequired pour accès complet
- Middleware d'authentification
- Messages de confirmation

## 🔧 Installation

### Étape 1: Installation des dépendances

```bash
pip install -r requirements.txt
```

### Étape 2: Appliquer les migrations

```bash
python manage.py makemigrations core
python manage.py makemigrations dashboard
python manage.py migrate
```

### Étape 3: Créer un super-utilisateur

```bash
python manage.py createsuperuser
```

### Étape 4: Démarrer le serveur

```bash
python manage.py runserver
```

## 🌐 Accès au Dashboard

1. **Pour accéder au dashboard:**
   - URL: `http://localhost:8000/dashboard/`
   - Vous devez être connecté et être staff

2. **Pour accéder à l'administrateur Django:**
   - URL: `http://localhost:8000/admin/`

## 📱 URLs du Dashboard

| Module | URL |
|--------|-----|
| Accueil | `/dashboard/` |
| Produits | `/dashboard/products/` |
| Créer Produit | `/dashboard/products/create/` |
| Modifier Produit | `/dashboard/products/<id>/edit/` |
| Supprimer Produit | `/dashboard/products/<id>/delete/` |
| Catégories | `/dashboard/categories/` |
| Créer Catégorie | `/dashboard/categories/create/` |
| Images | `/dashboard/images/` |
| Paramètres | `/dashboard/settings/` |
| Utilisateurs | `/dashboard/users/` |
| Commandes | `/dashboard/orders/` |
| Messages | `/dashboard/contacts/` |
| Avis | `/dashboard/reviews/` |
| Promotions | `/dashboard/promotions/` |
| Analytics | `/dashboard/analytics/` |

## 👥 Rôles et Permissions

### Admin/Staff
- Accès complet au dashboard
- Gestion complète des ressources
- Gestion des utilisateurs
- Visualisation des analytics

### Client
- Pas d'accès au dashboard
- Accès à leur compte personnel
- Historique des commandes
- Possibilité de laisser des avis

## 🗄️ Modèles de Données

### Models Créés/Étendus:

1. **SiteSettings**
   - Paramètres globaux du site
   - Informations contact
   - Réseaux sociaux
   - SEO

2. **SiteImage**
   - Images du site dynamiques
   - Types: banner, hero, logo, favicon, marketing

3. **Contact**
   - Messages de contact des visiteurs
   - Statut lu/non lu
   - Réponses admin

4. **Review**
   - Avis sur les produits
   - Notations 1-5 étoiles
   - Approbation admin
   - Réponses admin

5. **Promotion**
   - Codes promo
   - Types de réductions
   - Limites d'utilisation
   - Périodes valides

## 🎨 Design UI/UX

- **Sidebar fixe** avec menu de navigation
- **Navbar** pour informations utilisateur
- **Cards modernes** avec ombres et transitions
- **Responsive design** (works on mobile)
- **Bootstrap 4** pour la structure
- **Font Awesome 6** pour les icônes
- **Couleurs gradient** (violet/bleu)

## ⚠️ Notes Importantes

1. **Permissions**: Seuls les utilisateurs avec `is_staff=True` peuvent accéder

2. **Migrations**: Si vous modifiez les modèles, exécutez:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Static Files**: Assurez-vous que les static files sont collectés:
   ```bash
   python manage.py collectstatic
   ```

4. **Images**: Les images doivent être dans les répertoires MEDIA_ROOT:
   - Produits: `media_root/products/`
   - Catégories: `media_root/categories/`
   - Site: `media_root/site/`
   - Images: `media_root/site-images/`

## 🐛 Dépannage

### Problème: "Page not found" au dashboard
- Vérifiez que l'app 'dashboard' est dans INSTALLED_APPS
- Vérifiez que les URLs sont incluses dans demo/urls.py
- Vérifiez votre authentification

### Problème: Permission denied
- Vérifiez que your account a is_staff=True
- Naviguer vers /admin/ et cocher "Staff status"

### Problème: Images ne s'affichent pas
- Vérifiez que DEBUG=True en développement
- Vérifiez les chemins MEDIA_URL et MEDIA_ROOT

## 📊 Structure de Fichiers

```
dashboard/
├── migrations/        # Migrations Django
├── templates/
│   └── dashboard/
│       ├── base.html                # Template de base
│       ├── home.html                # Dashboard home
│       ├── products/                # Templates produits
│       ├── categories/              # Templates catégories
│       ├── images/                  # Templates images
│       ├── users/                   # Templates utilisateurs
│       ├── orders/                  # Templates commandes
│       ├── contacts/                # Templates messages
│       ├── reviews/                 # Templates avis
│       ├── promotions/              # Templates promotions
│       └── analytics.html           # Analytics
├── admin.py         # Configuration admin
├── apps.py          # Config application
├── forms.py         # Formulaires Django
├── models.py        # Modèles (vides, dans core)
├── tests.py         # Tests
├── urls.py          # URL configuration
└── views.py         # Vues du dashboard
```

## 🚀 Prochaines Étapes

1. **Personnalisation**:
   - Modifiez les couleurs dans base.html
   - Adaptez les templates à votre brand
   - Ajoutez vos logos

2. **Fonctionnalités Additionnelles**:
   - Email notifications
   - Export des données (CSV, PDF)
   - API REST pour mobile app
   - Webhooks pour livraison

3. **Sécurité**:
   - HTTPS en production
   - CSRF protection
   - Rate limiting
   - Two-factor authentication

4. **Performance**:
   - Caching
   - Pagination optimisée
   - Indexes sur les queries
   - Lazy loading pour images

## 📝 Licence

Ce dashboard est fourni tel quel pour le projet Django E-Commerce.

## ❓ Support

Pour des questions ou des problèmes, consultez:
- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/
- Font Awesome: https://fontawesome.com/

---

**Dernière mise à jour**: April 2026
**Version**: 1.0.0
