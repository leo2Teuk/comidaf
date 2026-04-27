from django import forms
from django.utils.text import slugify
from core.models import (
    Item, Category, SiteSettings, SiteImage, Contact, 
    Review, Promotion
)


class ItemForm(forms.ModelForm):
    """Form pour créer/modifier les produits"""
    class Meta:
        model = Item
        fields = [
            'title', 'description_short', 'description_long', 
            'price', 'discount_price', 'category', 'image',
            'stock_quantity', 'stock_no', 'sku', 'label',
            'weight', 'dimensions', 'is_active', 'is_featured',
            'seo_title', 'seo_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du produit'
            }),
            'description_short': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Description courte'
            }),
            'description_long': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description détaillée'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'discount_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'stock_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de stock'
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SKU (optionnel)'
            }),
            'label': forms.Select(attrs={
                'class': 'form-control'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'dimensions': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'L x W x H en cm'
            }),
            'seo_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre SEO'
            }),
            'seo_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Description SEO'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance


class CategoryForm(forms.ModelForm):
    """Form pour créer/modifier les catégories"""
    class Meta:
        model = Category
        fields = ['title', 'description', 'image', 'parent', 'is_active', 'order']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la catégorie'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'parent': forms.Select(attrs={
                'class': 'form-control'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance


class SiteSettingsForm(forms.ModelForm):
    """Form pour modifier les paramètres du site"""
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'site_email', 'whatsapp_number', 'phone_number',
            'address', 'facebook_url', 'instagram_url', 'twitter_url',
            'youtube_url', 'linkedin_url', 'logo', 'favicon',
            'meta_description', 'meta_keywords', 'currency',
            'items_per_page', 'enable_reviews', 'enable_wishlist'
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du site'
            }),
            'site_email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+229...'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+229...'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control'
            }),
            'youtube_url': forms.URLInput(attrs={
                'class': 'form-control'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'favicon': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'currency': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'items_per_page': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'enable_reviews': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'enable_wishlist': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class SiteImageForm(forms.ModelForm):
    """Form pour ajouter/modifier les images du site"""
    class Meta:
        model = SiteImage
        fields = ['image_type', 'title', 'image', 'description', 'alt_text', 'order', 'is_active']
        widgets = {
            'image_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l\'image'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Texte alternatif'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ReviewResponseForm(forms.ModelForm):
    """Form pour répondre aux avis"""
    class Meta:
        model = Review
        fields = ['is_approved', 'admin_response']
        widgets = {
            'admin_response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Votre réponse'
            }),
            'is_approved': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class PromotionForm(forms.ModelForm):
    """Form pour créer/modifier les promotions"""
    class Meta:
        model = Promotion
        fields = [
            'code', 'title', 'description', 'discount_type', 'discount_value',
            'max_uses', 'min_order_amount', 'items', 'is_active',
            'start_date', 'end_date'
        ]
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CODE2024'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de la promotion'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'discount_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'discount_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'max_uses': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'min_order_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'items': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
