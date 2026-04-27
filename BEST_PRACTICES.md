# 💡 GUIDE DE BONNES PRATIQUES - DASHBOARD DJANGO

## 🎯 BONNES PRATIQUES IMPLÉMENTÉES

### 1. Architecture Django ✅

#### Structure d'App
```
dashboard/
├── __init__.py                 # App config
├── apps.py                     # Classes app
├── admin.py                    # Enregistrement admin
├── models.py                   # Modèles (si nécessaire)
├── views.py                    # Logique métier
├── forms.py                    # Formulaires
├── urls.py                     # Routage
├── migrations/                 # Migrations BD
└── templates/                  # Templates HTML
    └── dashboard/              # Sous-dossier modulaire
        ├── base.html
        ├── home.html
        ├── products/
        ├── categories/
        └── ...
```

**Avantage:** Séparation claire des responsabilités (MVC/MVT)

#### Avantages:
- ✅ Maintenabilité
- ✅ Testabilité
- ✅ Réutilisabilité
- ✅ Scalabilité

---

### 2. Class-Based Views (CBV) ✅

#### Utilisation
```python
# ✅ BON - Utiliser CBV pour CRUD standard
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

class ProductListView(StaffRequiredMixin, ListView):
    queryset = Item.objects.all()
    template_name = 'dashboard/products/list.html'
    paginate_by = 20
    
    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(title__icontains=search)
        return qs
```

#### Avantages:
- ✅ Moins de code
- ✅ Mixins réutilisables
- ✅ Permissions intégrées
- ✅ Conventions standardisées

---

### 3. Mixins pour Authentification ✅

#### Implémentation
```python
# ✅ BON - Créer mixin réutilisable
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect

class StaffRequiredMixin(LoginRequiredMixin):
    """Requires staff/admin user"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('admin:login')
        return super().dispatch(request, *args, **kwargs)

# ✅ UTILISATION
class ProductListView(StaffRequiredMixin, ListView):
    # View code...
```

#### Avantages:
- ✅ DRY (Don't Repeat Yourself)
- ✅ Cohérence
- ✅ Facile à modifier globalement

---

### 4. Formulaires ModelForm ✅

#### Pattern Correct
```python
# ✅ BON - Utiliser ModelForm avec Meta widgets personnalisés
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'price', 'discount_price', 'category', 'image']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Titre du produit', 'class': 'form-control'}
            ),
            'price': forms.NumberInput(
                attrs={'step': '0.01', 'class': 'form-control'}
            ),
            'description1': forms.Textarea(
                attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Description...'}
            ),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }
    
    def save(self, commit=True):
        """Auto-generate slug from title"""
        instance = super().save(commit=False)
        if not instance.slug or self.cleaned_data['title'] != instance.title:
            from django.utils.text import slugify
            instance.slug = slugify(self.cleaned_data['title'])
        if commit:
            instance.save()
        return instance
```

#### Avantages:
- ✅ Validation automatique
- ✅ Protection CSRF
- ✅ Message validation personnalisé
- ✅ HTML render simple

---

### 5. Gestion des Erreurs ✅

#### Pattern Correct
```python
# ✅ BON - Gérer les cas edge
class OrderDetailView(StaffRequiredMixin, DetailView):
    model = Order
    template_name = 'dashboard/orders/detail.html'
    context_object_name = 'order'
    
    def get_object(self):
        try:
            return Order.objects.get(pk=self.kwargs['pk'])
        except Order.DoesNotExist:
            raise Http404("Commande non trouvée")
    
    def post(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.POST.get('status')
        
        # ✅ Validation
        if new_status not in dict(Order.ORDER_STATUS_CHOICES):
            messages.error(request, "Statut invalide")
            return redirect('dashboard:orders-detail', pk=order.pk)
        
        order.status = new_status
        order.save()
        messages.success(request, f"Statut mis à jour en: {new_status}")
        return redirect('dashboard:orders-detail', pk=order.pk)
```

#### Avantages:
- ✅ Pas de crash
- ✅ UX clair
- ✅ Logs traçables

---

### 6. Pagination ✅

#### Implémentation
```python
# ✅ BON - Paginer les listes
class ProductListView(StaffRequiredMixin, ListView):
    model = Item
    paginate_by = 20  # 20 par page
    template_name = 'dashboard/products/list.html'
    
    # Template:
    # {% for product in products %}
    #   <tr>...</tr>
    # {% endfor %}
    # 
    # {% if is_paginated %}
    #   <nav aria-label="Page navigation">
    #     <ul class="pagination">
    #       {% if page_obj.has_previous %}
    #         <li><a href="?page=1">Première</a></li>
    #         <li><a href="?page={{ page_obj.previous_page_number }}">Précédente</a></li>
    #       {% endif %}
    #       
    #       <li class="active">Page {{ page_obj.number }}</li>
    #       
    #       {% if page_obj.has_next %}
    #         <li><a href="?page={{ page_obj.next_page_number }}">Suivante</a></li>
    #         <li><a href="?page={{ page_obj.paginator.num_pages }}">Dernière</a></li>
    #       {% endif %}
    #     </ul>
    #   </nav>
    # {% endif %}
```

#### Avantages:
- ✅ Performance (pas tout charger)
- ✅ UX fluide
- ✅ Scalable avec BD grande

---

### 7. Recherche et Filtrage ✅

#### Pattern Correct
```python
# ✅ BON - Filtrer proprement
class ProductListView(StaffRequiredMixin, ListView):
    model = Item
    paginate_by = 20
    
    def get_queryset(self):
        qs = Item.objects.all()
        
        # Recherche
        search = self.request.GET.get('search', '')
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description1__icontains=search)
            )
        
        # Filtres
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category_id=category)
        
        status = self.request.GET.get('status')
        if status in ['active', 'draft']:
            qs = qs.filter(status=status)
        
        return qs.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        return context
```

#### Template
```html
<form method="get" class="form-inline">
    <input type="text" name="search" value="{{ search_query }}" 
           placeholder="Rechercher..." class="form-control mr-2">
    
    <select name="category" class="form-control mr-2">
        <option value="">Toutes les catégories</option>
        {% for cat in categories %}
            <option value="{{ cat.id }}">{{ cat.name }}</option>
        {% endfor %}
    </select>
    
    <button type="submit" class="btn btn-primary">Filtrer</button>
</form>
```

#### Avantages:
- ✅ Flexible
- ✅ Performant
- ✅ UX intuitif

---

### 8. Messages Django ✅

#### Utilisation Correcte
```python
# ✅ BON
from django.contrib import messages

def post(self, request, *args, **kwargs):
    try:
        object = self.form_valid(form)
        messages.success(
            request, 
            f"✅ {object} créé avec succès!"  # Emoji optionnel
        )
        return redirect('dashboard:products-list')
    except Exception as e:
        messages.error(request, f"❌ Erreur: {str(e)}")
        return self.form_invalid(form)
```

#### Template
```html
{% if messages %}
  <div class="alert-container mt-3">
      {% for message in messages %}
          <div class="alert alert-{{ message.tags }}" role="alert">
              {{ message }}
              <button type="button" class="close" data-dismiss="alert">
                  <span>&times;</span>
              </button>
          </div>
      {% endfor %}
  </div>
{% endif %}
```

#### Avantages:
- ✅ Feedback utilisateur
- ✅ Bootstrap intégré
- ✅ Auto-fermeture

---

### 9. Gestion d'Images ✅

#### Pattern Correct
```python
# ✅ BON - Gérer images proprement
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

class ProductCreateView(StaffRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    
    def form_valid(self, form):
        # Image optionnelle
        if 'image' in self.request.FILES:
            image = self.request.FILES['image']
            
            # Validation
            if image.size > 5 * 1024 * 1024:  # 5MB max
                form.add_error('image', 'Image trop grande (max 5MB)')
                return self.form_invalid(form)
            
            # Sauvegarde
            obj = form.save(commit=False)
            obj.image = image
            obj.save()
        else:
            obj = form.save()
        
        messages.success(self.request, "Produit créé!")
        return super().form_valid(form)
```

#### Template avec Preview
```html
<div class="form-group">
    <label for="image">Image</label>
    <input type="file" id="image" name="image" class="form-control" 
           accept="image/*" onchange="previewImage(this)">
    
    {% if form.instance.image %}
        <div class="mt-2">
            <img src="{{ form.instance.image.url }}" 
                 style="max-width: 200px; max-height: 200px;" 
                 alt="Aperçu">
        </div>
    {% endif %}
    
    <div id="preview" style="margin-top: 10px;"></div>
</div>

<script>
function previewImage(input) {
    const preview = document.getElementById('preview');
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.innerHTML = `<img src="${e.target.result}" 
                                      style="max-width: 200px; max-height: 200px;">`;
        };
        reader.readAsDataURL(input.files[0]);
    }
}
</script>
```

#### Avantages:
- ✅ Validation fichier
- ✅ Preview avant upload
- ✅ Pas de surcharge

---

### 10. Slugs Auto-Générés ✅

#### Pattern Correct
```python
# ✅ BON - Slug auto-généré
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            
            # Éviter les doublons
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']  # slug NOT inclus
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('slug', None)  # Retirer slug du formulaire
```

#### Avantages:
- ✅ SEO-friendly
- ✅ Évite doublons
- ✅ URLs lisibles

---

### 11. Dates et Heures ✅

#### Pattern Correct
```python
from django.utils import timezone
from django.db import models

class Contact(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Once on create
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    def mark_as_read(self):
        """Mark message as read"""
        self.is_read = True
        self.read_at = timezone.now()  # ✅ Utiliser timezone.now()
        self.save()

# View
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.mark_as_read()  # Auto marquer lu
    
    context = {
        'contact': contact,
        'time_since': timezone.now() - contact.created_at  # timesince
    }
    return render(request, 'dashboard/contacts/detail.html', context)
```

#### Template
```html
<p>Reçu il y a: {{ contact.created_at|timesince }}</p>

{% if contact.is_read %}
    <span class="badge badge-info">Lue le {{ contact.read_at|date:"d/m/Y H:i" }}</span>
{% endif %}
```

#### Avantages:
- ✅ Timezone correct
- ✅ Format flexible
- ✅ Audit trail

---

### 12. QuerySet Optimization ✅

#### Anti-Pattern ❌
```python
# ❌ MAUVAIS - N+1 queries
def bad_view(request):
    orders = Order.objects.all()
    context = {
        'orders': orders
    }
    return render(request, 'orders.html', context)

# Template: Pour chaque order, requête SELECT User/Item
# {% for order in orders %}
#     {{ order.user.email }}  # SELECT * FROM users WHERE id=...
# {% endfor %}
```

#### Pattern Correct ✅
```python
# ✅ BON - Prefetch/Select related
from django.db.models import Prefetch, Q

class OrderListView(StaffRequiredMixin, ListView):
    def get_queryset(self):
        qs = Order.objects.select_related('user').prefetch_related('items')
        
        # Plus rapide - 1 requête au lieu de N+1
        return qs.order_by('-created_at')

# Aggregate si besoin stats
from django.db.models import Sum, Count

context = {
    'total_orders': Order.objects.count(),
    'total_revenue': Order.objects.aggregate(Sum('total'))['total__sum'] or 0,
    'orders_by_status': Order.objects.values('status').annotate(count=Count('id'))
}
```

#### Avantages:
- ✅ Performance 100x mieux
- ✅ Moins de charge BD
- ✅ Scalable

---

### 13. Permissions Granulaires ✅

#### Pattern Correct
```python
# ✅ BON - Permissions détaillées
class ProductDeleteView(StaffRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    
    def test_func(self):
        """Only allow super-staff to delete"""
        return self.request.user.is_superuser or \
               self.request.user.groups.filter(name='Product Manager').exists()
    
    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas la permission de supprimer")
        return redirect('dashboard:products-list')
```

#### Avec Groups
```python
# settings.py
PERMISSION_GROUPS = {
    'Product Manager': [
        'core.add_item',
        'core.change_item',
        'core.delete_item',
    ],
    'Category Manager': [
        'core.add_category',
        'core.change_category',
    ],
}

# models.py
def setup_permissions():
    from django.contrib.auth.models import Group, Permission
    for group_name, permissions in PERMISSION_GROUPS.items():
        group, created = Group.objects.get_or_create(name=group_name)
        for perm in permissions:
            app, codename = perm.split('.')
            try:
                p = Permission.objects.get(
                    content_type__app_label=app,
                    codename=codename
                )
                group.permissions.add(p)
            except Permission.DoesNotExist:
                pass
```

#### Avantages:
- ✅ Contrôle fin
- ✅ Flexible
- ✅ Audit possible

---

### 14. Testabilité ✅

#### Pattern Correct
```python
# tests.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_staff_user(
            username='admin',
            email='admin@test.com',
            password='testpass'
        )
        self.client.login(username='admin', password='testpass')
    
    def test_product_list_view(self):
        response = self.client.get('/dashboard/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/products/list.html')
    
    def test_product_create_requires_staff(self):
        self.client.logout()
        response = self.client.get('/dashboard/products/create/')
        self.assertNotEqual(response.status_code, 200)
```

#### Avantages:
- ✅ Confiance code
- ✅ Refactoring safe
- ✅ Regression prevention

---

### 15. Logging et Debugging ✅

#### Configuration
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/dashboard.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'dashboard': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# views.py
import logging
logger = logging.getLogger('dashboard')

def product_create(request):
    try:
        # Code...
        logger.info(f"Product created by {request.user}")
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}", exc_info=True)
        messages.error(request, "Erreur lors de la création")
```

#### Avantages:
- ✅ Audit trail
- ✅ Debugging facile
- ✅ Production safe

---

## 🎓 RÉSUMÉ CHECKLIST

- [x] Django app structure correcte
- [x] CBV pour CRUD
- [x] Mixins réutilisables
- [x] ModelForms validés
- [x] Gestion erreurs
- [x] Pagination
- [x] Recherche/Filtre
- [x] Messages utilisateur
- [x] Upload images safe
- [x] Slugs auto-générés
- [x] Dates timezone.now()
- [x] QuerySet optimisé (select/prefetch)
- [x] Permissions granulaires
- [x] Tests unitaires
- [x] Logging/debugging

---

**Dernière MAJ**: 2024  
**Django Version**: 3.x+  
**Status**: Production-ready
