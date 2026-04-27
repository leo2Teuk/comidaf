from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta

from core.models import (
    Item, Category, Order, OrderItem, SiteSettings, SiteImage,
    Contact, Review, Promotion, User
)
from .forms import (
    ItemForm, CategoryForm, SiteSettingsForm, SiteImageForm,
    ReviewResponseForm, PromotionForm
)


# ==========================================
# Mixins pour l'authentification et droits
# ==========================================

def is_staff(user):
    """Vérifier si l'utilisateur est staff"""
    return user.is_staff


class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin pour vérifier si l'utilisateur est staff"""
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, "Vous n'avez pas accès au dashboard")
        return redirect('core:home')


# ==========================================
# TABLEAU DE BORD (Dashboard Home)
# ==========================================

class DashboardHomeView(LoginRequiredMixin, StaffRequiredMixin, View):
    """Page d'accueil du dashboard avec statistiques"""
    
    def get(self, request):
        # Statistiques générales
        total_products = Item.objects.count()
        total_categories = Category.objects.count()
        total_orders = Order.objects.filter(ordered=True).count()
        total_revenue = sum([
            order.get_total() for order in Order.objects.filter(ordered=True)
        ])
        
        # Produits en rupture de stock
        out_of_stock = Item.objects.filter(stock_quantity=0).count()
        
        # Commandes récentes
        recent_orders = Order.objects.filter(ordered=True).order_by('-start_date')[:5]
        
        # Produits les plus vendus
        popular_items = []
        for order in Order.objects.filter(ordered=True):
            for item in order.items.all():
                popular_items.append(item.item)
        
        from collections import Counter
        item_counts = Counter(popular_items)
        popular_items = [
            (item, count) for item, count in item_counts.most_common(5)
        ]
        
        # Messages non lus
        unread_messages = Contact.objects.filter(is_read=False).count()
        
        # Avis sans approbation
        unapproved_reviews = Review.objects.filter(is_approved=False).count()
        
        context = {
            'total_products': total_products,
            'total_categories': total_categories,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'out_of_stock': out_of_stock,
            'recent_orders': recent_orders,
            'popular_items': popular_items,
            'unread_messages': unread_messages,
            'unapproved_reviews': unapproved_reviews,
        }
        
        return render(request, 'dashboard/home.html', context)


dashboard_home = login_required(user_passes_test(is_staff)(DashboardHomeView.as_view()))


# ==========================================
# GESTION DES PRODUITS
# ==========================================

class ProductListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Liste des produits avec pagination"""
    model = Item
    template_name = 'dashboard/products/list.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        queryset = Item.objects.all()
        
        # Recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(stock_no__icontains=search)
            )
        
        # Filtre par catégorie
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Filtre par statut
        status = self.request.GET.get('status')
        if status:
            if status == 'active':
                queryset = queryset.filter(is_active=True)
            elif status == 'inactive':
                queryset = queryset.filter(is_active=False)
            elif status == 'stock':
                queryset = queryset.filter(stock_quantity=0)
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search'] = self.request.GET.get('search', '')
        return context


class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """Créer un nouveau produit"""
    model = Item
    form_class = ItemForm
    template_name = 'dashboard/products/form.html'
    success_url = reverse_lazy('dashboard:products-list')

    def form_valid(self, form):
        messages.success(self.request, "Produit créé avec succès")
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """Modifier un produit"""
    model = Item
    form_class = ItemForm
    template_name = 'dashboard/products/form.html'
    
    def get_success_url(self):
        messages.success(self.request, "Produit modifié avec succès")
        return reverse_lazy('dashboard:products-list')


class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """Supprimer un produit"""
    model = Item
    template_name = 'dashboard/products/confirm_delete.html'
    success_url = reverse_lazy('dashboard:products-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Produit supprimé avec succès")
        return super().delete(request, *args, **kwargs)


# ==========================================
# GESTION DES CATÉGORIES
# ==========================================

class CategoryListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Liste des catégories"""
    model = Category
    template_name = 'dashboard/categories/list.html'
    context_object_name = 'categories'
    paginate_by = 15

    def get_queryset(self):
        return Category.objects.all().order_by('order', 'title')


class CategoryCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """Créer une nouvelle catégorie"""
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/categories/form.html'
    success_url = reverse_lazy('dashboard:categories-list')

    def form_valid(self, form):
        messages.success(self.request, "Catégorie créée avec succès")
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """Modifier une catégorie"""
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/categories/form.html'
    
    def get_success_url(self):
        messages.success(self.request, "Catégorie modifiée avec succès")
        return reverse_lazy('dashboard:categories-list')


class CategoryDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """Supprimer une catégorie"""
    model = Category
    template_name = 'dashboard/categories/confirm_delete.html'
    success_url = reverse_lazy('dashboard:categories-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Catégorie supprimée avec succès")
        return super().delete(request, *args, **kwargs)


# ==========================================
# GESTION DES IMAGES DU SITE
# ==========================================

class SiteImageListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Liste des images du site"""
    model = SiteImage
    template_name = 'dashboard/images/list.html'
    context_object_name = 'images'
    paginate_by = 12

    def get_queryset(self):
        image_type = self.request.GET.get('type')
        queryset = SiteImage.objects.all()
        if image_type:
            queryset = queryset.filter(image_type=image_type)
        return queryset.order_by('image_type', 'order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_types'] = dict(SiteImage.IMAGE_TYPES)
        return context


class SiteImageCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """Ajouter une image au site"""
    model = SiteImage
    form_class = SiteImageForm
    template_name = 'dashboard/images/form.html'
    success_url = reverse_lazy('dashboard:images-list')

    def form_valid(self, form):
        messages.success(self.request, "Image ajoutée avec succès")
        return super().form_valid(form)


class SiteImageUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """Modifier une image du site"""
    model = SiteImage
    form_class = SiteImageForm
    template_name = 'dashboard/images/form.html'
    
    def get_success_url(self):
        messages.success(self.request, "Image modifiée avec succès")
        return reverse_lazy('dashboard:images-list')


class SiteImageDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """Supprimer une image du site"""
    model = SiteImage
    template_name = 'dashboard/images/confirm_delete.html'
    success_url = reverse_lazy('dashboard:images-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Image supprimée avec succès")
        return super().delete(request, *args, **kwargs)


# ==========================================
# PARAMÈTRES DU SITE
# ==========================================

class SiteSettingsView(LoginRequiredMixin, StaffRequiredMixin, View):
    """Modifier les paramètres du site"""
    
    def get(self, request):
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        form = SiteSettingsForm(instance=settings)
        return render(request, 'dashboard/settings.html', {'form': form, 'settings': settings})
    
    def post(self, request):
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Paramètres du site mis à jour")
            return redirect('dashboard:settings')
        return render(request, 'dashboard/settings.html', {'form': form, 'settings': settings})


# ==========================================
# GESTION DES UTILISATEURS
# ==========================================

class UserListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Liste des utilisateurs"""
    model = User
    template_name = 'dashboard/users/list.html'
    context_object_name = 'users'
    paginate_by = 15

    def get_queryset(self):
        search = self.request.GET.get('search')
        queryset = User.objects.all()
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search)
            )
        return queryset.order_by('-date_joined')


class UserDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    """Détails d'un utilisateur"""
    model = User
    template_name = 'dashboard/users/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculer le montant total dépensé
        total_spent = sum([
            order.get_total() for order in self.object.order_set.filter(ordered=True)
        ])
        context['total_spent'] = total_spent
        return context


@login_required(redirect_field_name=None)
@user_passes_test(is_staff)
def toggle_user_staff(request, pk):
    """Activer/désactiver le rôle staff"""
    user = get_object_or_404(User, pk=pk)
    user.is_staff = not user.is_staff
    user.save()
    status = "staff" if user.is_staff else "client"
    messages.success(request, f"{user.username} est maintenant {status}")
    return redirect('dashboard:users-detail', pk=pk)


@login_required(redirect_field_name=None)
@user_passes_test(is_staff)
def toggle_user_active(request, pk):
    """Activer/désactiver un compte"""
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    status = "activé" if user.is_active else "désactivé"
    messages.success(request, f"Compte {user.username} {status}")
    return redirect('dashboard:users-detail', pk=pk)


# ==========================================
# GESTION DES COMMANDES
# ==========================================

class OrderListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Liste des commandes"""
    model = Order
    template_name = 'dashboard/orders/list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get('search')
        queryset = Order.objects.filter(ordered=True)
        if search:
            queryset = queryset.filter(
                Q(ref_code__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__email__icontains=search)
            )
        return queryset.order_by('-ordered_date')


class OrderDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    """Détails d'une commande"""
    model = Order
    template_name = 'dashboard/orders/detail.html'


@login_required(redirect_field_name=None)
@user_passes_test(is_staff)
def update_order_status(request, pk):
    """Mettre à jour le statut d'une commande"""
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        being_delivered = request.POST.get('being_delivered') == 'on'
        received = request.POST.get('received') == 'on'
        
        order.being_delivered = being_delivered
        order.received = received
        order.save()
        
        messages.success(request, "Statut de la commande mis à jour")
    
    return redirect('dashboard:orders-detail', pk=pk)


# ==========================================
# GESTION DES MESSAGES/CONTACT
# ==========================================

class ContactListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Liste des messages de contact"""
    model = Contact
    template_name = 'dashboard/contacts/list.html'
    context_object_name = 'contacts'
    paginate_by = 15

    def get_queryset(self):
        return Contact.objects.all().order_by('-created_at')


class ContactDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    """Détails d'un message"""
    model = Contact
    template_name = 'dashboard/contacts/detail.html'
    
    def get(self, request, *args, **kwargs):
        contact = self.get_object()
        if not contact.is_read:
            contact.is_read = True
            contact.save()
        return super().get(request, *args, **kwargs)


@login_required(redirect_field_name=None)
@user_passes_test(is_staff)
def delete_contact(request, pk):
    """Supprimer un message"""
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    messages.success(request, "Message supprimé")
    return redirect('dashboard:contacts-list')


@login_required(redirect_field_name=None)
@user_passes_test(is_staff)
def reply_contact(request, pk):
    """Répondre à un message"""
    contact = get_object_or_404(Contact, pk=pk)
    
    if request.method == 'POST':
        reply_message = request.POST.get('reply_message')
        contact.reply_message = reply_message
        contact.replied_at = timezone.now()
        contact.save()
        messages.success(request, "Réponse envoyée")
        return redirect('dashboard:contacts-detail', pk=pk)
    
    return render(request, 'dashboard/contacts/reply.html', {'contact': contact})


# ==========================================
# GESTION DES AVIS
# ==========================================

class ReviewListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Liste des avis"""
    model = Review
    template_name = 'dashboard/reviews/list.html'
    context_object_name = 'reviews'
    paginate_by = 15

    def get_queryset(self):
        status = self.request.GET.get('status')
        queryset = Review.objects.all()
        if status:
            if status == 'approved':
                queryset = queryset.filter(is_approved=True)
            elif status == 'pending':
                queryset = queryset.filter(is_approved=False)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_reviews'] = Review.objects.count()
        context['approved_reviews'] = Review.objects.filter(is_approved=True).count()
        context['pending_reviews'] = Review.objects.filter(is_approved=False).count()
        return context


@login_required(redirect_field_name=None)
@user_passes_test(is_staff)
def approve_review(request, pk):
    """Approuver un avis"""
    review = get_object_or_404(Review, pk=pk)
    review.is_approved = True
    review.save()
    messages.success(request, "Avis approuvé")
    return redirect('dashboard:reviews-list')


@login_required(redirect_field_name=None)
@user_passes_test(is_staff)
def delete_review(request, pk):
    """Supprimer un avis"""
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    messages.success(request, "Avis supprimé")
    return redirect('dashboard:reviews-list')


@login_required(redirect_field_name=None)
@user_passes_test(is_staff)
def respond_review(request, pk):
    """Répondre à un avis"""
    review = get_object_or_404(Review, pk=pk)
    
    if request.method == 'POST':
        form = ReviewResponseForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Réponse ajoutée")
            return redirect('dashboard:reviews-list')
    else:
        form = ReviewResponseForm(instance=review)
    
    return render(request, 'dashboard/reviews/respond.html', {'form': form, 'review': review})


# ==========================================
# GESTION DES PROMOTIONS
# ==========================================

class PromotionListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Liste des promotions"""
    model = Promotion
    template_name = 'dashboard/promotions/list.html'
    context_object_name = 'promotions'
    paginate_by = 15

    def get_queryset(self):
        return Promotion.objects.all().order_by('-created_at')


class PromotionCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """Créer une promotion"""
    model = Promotion
    form_class = PromotionForm
    template_name = 'dashboard/promotions/form.html'
    success_url = reverse_lazy('dashboard:promotions-list')

    def form_valid(self, form):
        messages.success(self.request, "Promotion créée avec succès")
        return super().form_valid(form)


class PromotionUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """Modifier une promotion"""
    model = Promotion
    form_class = PromotionForm
    template_name = 'dashboard/promotions/form.html'
    
    def get_success_url(self):
        messages.success(self.request, "Promotion modifiée avec succès")
        return reverse_lazy('dashboard:promotions-list')


class PromotionDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """Supprimer une promotion"""
    model = Promotion
    template_name = 'dashboard/promotions/confirm_delete.html'
    success_url = reverse_lazy('dashboard:promotions-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Promotion supprimée avec succès")
        return super().delete(request, *args, **kwargs)


# ==========================================
# ANALYTICS (Optionnel)
# ==========================================

class AnalyticsView(LoginRequiredMixin, StaffRequiredMixin, View):
    """Page d'analytics"""
    
    def get(self, request):
        # Données pour les 30 derniers jours
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # Commandes par jour
        daily_orders = {}
        for order in Order.objects.filter(ordered=True, ordered_date__gte=thirty_days_ago):
            date = order.ordered_date.date()
            daily_orders[date] = daily_orders.get(date, 0) + 1
        
        # Revenu par jour
        daily_revenue = {}
        for order in Order.objects.filter(ordered=True, ordered_date__gte=thirty_days_ago):
            date = order.ordered_date.date()
            daily_revenue[date] = daily_revenue.get(date, 0) + order.get_total()
        
        # Produits populaires
        popular_products = Item.objects.annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:10]
        
        context = {
            'daily_orders': daily_orders,
            'daily_revenue': daily_revenue,
            'popular_products': popular_products,
        }
        
        return render(request, 'dashboard/analytics.html', context)
