# 🗺️ RÉFÉRENCE RAPIDE DES URLS DASHBOARD

## Format URL
```
/dashboard/<section>/<action>/[<pk>/]
```

---

## 📍 ROUTES PRINCIPALES

### 🏠 HOME
| Nom URL | URL | Méthode | Description |
|---------|-----|---------|-------------|
| `dashboard:home` | `/dashboard/` | GET | Dashboard d'accueil avec stats |

---

### 📦 PRODUITS
| Nom URL | URL | Méthode | Description |
|---------|-----|---------|-------------|
| `dashboard:products-list` | `/dashboard/products/` | GET | Liste tous les produits |
| `dashboard:products-create` | `/dashboard/products/create/` | GET/POST | Créer nouveau produit |
| `dashboard:products-update` | `/dashboard/products/<pk>/edit/` | GET/POST | Modifier produit |
| `dashboard:products-delete` | `/dashboard/products/<pk>/delete/` | GET/POST | Supprimer produit |

**Filtres disponibles:**
- Recherche par titre
- Catégorie
- Statut (active/draft)

---

### 🏷️ CATÉGORIES
| Nom URL | URL | Méthode | Description |
|---------|-----|---------|-------------|
| `dashboard:categories-list` | `/dashboard/categories/` | GET | Liste catégories |
| `dashboard:categories-create` | `/dashboard/categories/create/` | GET/POST | Créer catégorie |
| `dashboard:categories-update` | `/dashboard/categories/<pk>/edit/` | GET/POST | Modifier catégorie |
| `dashboard:categories-delete` | `/dashboard/categories/<pk>/delete/` | GET/POST | Supprimer catégorie |

**Spécificités:**
- Hiérarchie parent/enfant
- Slug auto-généré
- Image par catégorie

---

### 🖼️ IMAGES DU SITE
| Nom URL | URL | Méthode | Description |
|---------|-----|---------|-------------|
| `dashboard:images-list` | `/dashboard/images/` | GET | Galerie d'images |
| `dashboard:images-create` | `/dashboard/images/create/` | GET/POST | Ajouter image |
| `dashboard:images-update` | `/dashboard/images/<pk>/edit/` | GET/POST | Modifier image |
| `dashboard:images-delete` | `/dashboard/images/<pk>/delete/` | GET/POST | Supprimer image |

**Types disponibles:**
- banner (bannière)
- hero (hero section)
- logo (logo site)
- favicon
- marketing
- other

---

### ⚙️ PARAMÈTRES DU SITE
| Nom URL | URL | Méthode | Description |
|---------|-----|---------|-------------|
| `dashboard:settings` | `/dashboard/settings/` | GET/POST | Configuration du site |

**Champs configurables:**
- Nom du site
- Email
- Téléphone
- WhatsApp
- Adresse
- Liens réseaux sociaux
- SEO (meta title, description)
- Logo, favicon
- Branding (couleurs, polices)

---

### 👥 UTILISATEURS
| Nom URL | URL | Méthode | Description |
|---------|-----|---------|-------------|
| `dashboard:users-list` | `/dashboard/users/` | GET | Liste des utilisateurs |
| `dashboard:users-detail` | `/dashboard/users/<pk>/` | GET | Détail utilisateur |

**Informations affichées:**
- Nom, email
- Date d'inscription
- Nombre de commandes
- Total dépensé
- Historique commandes
- Statut staff

---

### 📋 COMMANDES
| Nom URL | URL | Méthode | Description |
|---------|-----|---------|-------------|
| `dashboard:orders-list` | `/dashboard/orders/` | GET | Liste commandes |
| `dashboard:orders-detail` | `/dashboard/orders/<pk>/` | GET/POST | Détail commande |

**Fonctionnalités:**
- Recherche par ref_code
- Articles détail
- Statuts (building, ordered, shipped, received, refund_requested, refund_granted, refund_denied)
- Historique paiement
- Mise à jour statut

---

### 💬 MESSAGES DE CONTACT
| Nom URL | URL | Méthode | Description |
|---------|-----|---------|-------------|
| `dashboard:contacts-list` | `/dashboard/contacts/` | GET | Messages reçus |
| `dashboard:contacts-detail` | `/dashboard/contacts/<pk>/` | GET | Voir message |
| `dashboard:contacts-delete` | `/dashboard/contacts/<pk>/delete/` | POST | Supprimer message |
| `dashboard:contacts-reply` | `/dashboard/contacts/<pk>/reply/` | GET/POST | Répondre au message |

**Actions:**
- Marque automatique comme lu
- Stockage des réponses
- Historique messagerie

---

### ⭐ AVIS PRODUITS
| Nom URL | URL | Méthode | Description |
|---------|-----|---------|-------------|
| `dashboard:reviews-list` | `/dashboard/reviews/` | GET | Tous les avis |
| `dashboard:reviews-approve` | `/dashboard/reviews/<pk>/approve/` | POST | Approuver avis |
| `dashboard:reviews-respond` | `/dashboard/reviews/<pk>/respond/` | GET/POST | Répondre avis |

**Filtres:**
- Approbation (approuvé/en attente)
- Note (1-5 étoiles)

**Validation:**
- Réponse administrateur
- Comptage votes utiles

---

### 🎁 CODES PROMOTIONNELS
| Nom URL | URL | Méthode | Description |
|---------|-----|---------|-------------|
| `dashboard:promotions-list` | `/dashboard/promotions/` | GET | Codes promos |
| `dashboard:promotions-create` | `/dashboard/promotions/create/` | GET/POST | Créer promo |
| `dashboard:promotions-update` | `/dashboard/promotions/<pk>/edit/` | GET/POST | Modifier promo |
| `dashboard:promotions-delete` | `/dashboard/promotions/<pk>/delete/` | GET/POST | Supprimer promo |

**Types de réduction:**
- Pourcentage (%)
- Montant fixe (€)

**Contraintes:**
- Limite d'utilisation max_uses
- Montant minimum commande
- Dates de validité (start_date - end_date)
- Produits spécifiques (ManyToMany)

---

### 📊 ANALYTIQUE
| Nom URL | URL | Méthode | Description |
|---------|-----|---------|-------------|
| `dashboard:analytics` | `/dashboard/analytics/` | GET | Graphiques & stats |

**Visualisations:**
- Commandes quotidiennes (graphique ligne)
- Revenu quotidien (graphique colonne)
- Statistiques agrégées
- Données exportables

---

## 🔗 ACCÈS COMPLET

### URL Namespaces
```python
reverse('dashboard:home')                    # /dashboard/
reverse('dashboard:products-list')           # /dashboard/products/
reverse('dashboard:products-create')         # /dashboard/products/create/
reverse('dashboard:products-update', args=[1])  # /dashboard/products/1/edit/
reverse('dashboard:categories-list')         # /dashboard/categories/
# ... et tous les autres
```

### Inclusion dans Templates
```html
<a href="{% url 'dashboard:products-list' %}">Produits</a>
<a href="{% url 'dashboard:products-create' %}">+ Ajouter</a>
<a href="{% url 'dashboard:products-update' product.pk %}">Modifier</a>
```

---

## 🔐 AUTHENTIFICATION REQUISE

Toutes les routes du dashboard nécessitent:
- ✅ Utilisateur authentifié (`is_authenticated`)
- ✅ Statut staff (`is_staff=True`)

### Redirection
- Utilisateur non-authentifié → Page de login Django
- User non-staff → Erreur 403 (Forbidden)

---

## 🛠️ COMMANDES UTILES

```bash
# Afficher toutes les URLs dashboard
python manage.py show_urls | grep dashboard

# Tester une URL
python manage.py shell
from django.urls import reverse
print(reverse('dashboard:home'))

# Vérifier les migrations
python manage.py showmigrations dashboard

# Collecter les fichiers statiques
python manage.py collectstatic
```

---

## 📱 ACCÈS DEPUIS TEMPLATES

### Naviguer vers dashboard
```html
{# Depuis n'importe quel template #}
<a href="{% url 'dashboard:home' %}" class="btn btn-primary">
  Aller au Dashboard
</a>
```

### Boucler sur éléments avec URL
```html
{% for product in products %}
  <a href="{% url 'dashboard:products-update' product.pk %}">
    {{ product.title }}
  </a>
{% endfor %}
```

---

## 🎯 FAQ URLS

**Q: Comment aller à la liste des produits?**  
A: `GET /dashboard/products/` ou `reverse('dashboard:products-list')`

**Q: Comment créer un nouveau produit?**  
A: `POST /dashboard/products/create/` avec formulaire

**Q: Comment modifier le produit #5?**  
A: `GET/POST /dashboard/products/5/edit/` ou `reverse('dashboard:products-update', args=[5])`

**Q: Comment supprimer une catégorie?**  
A: `GET /dashboard/categories/3/delete/` (confirmation page) puis `POST` pour confirmer

**Q: Comment afficher le détail d'une commande?**  
A: `GET /dashboard/orders/123/`

**Q: Comment répondre à une avis produit?**  
A: `GET/POST /dashboard/reviews/45/respond/`

---

## ✨ PATTERNS AVANCÉS

### Redirect après creation
```python
# Dans views.py
def get_success_url(self):
    return reverse('dashboard:products-detail', args=[self.object.pk])
```

### URL avec paramètres query
```html
{# Passé par Vue/Vue #}
/dashboard/products/?search=apple&category=5
```

### Combinaison avec Django auth
```html
{% if user.is_staff %}
  <a href="{% url 'dashboard:home' %}">Dashboard</a>
{% endif %}
```

---

## 📌 NOTES IMPORTANTES

1. **Toutes les URLs nécessitent `is_staff=True`**
   - Administrateur requis dans admin Django

2. **Namespacing 'dashboard'**
   - Impératif d'utiliser le namespace complet
   - `reverse('dashboard:products-list')`

3. **PK obligatoire pour Detail/Edit/Delete**
   - `reverse('dashboard:products-update', args=[product_id])`

4. **POST requis pour actions destructrices**
   - Suppression: POST avec confirmation
   - Approval: POST request

5. **Messages de feedback**
   - Succès/Erreur affichés au top de page
   - Utilisez Django messages framework

---

**Dernière mise à jour**: 2024  
**Dashboard Version**: 1.0  
**Django**: 3.x+
