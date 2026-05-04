from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils import timezone

# Create your models here.
CATEGORY_CHOICES = (
    ('SB', 'Shirts And Blouses'),
    ('TS', 'T-Shirts'),
    ('SK', 'Skirts'),
    ('HS', 'Hoodies&Sweatshirts')
)

LABEL_CHOICES = (
    ('S', 'sale'),
    ('N', 'new'),
    ('P', 'promotion')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Slide(models.Model):
    caption1 = models.CharField(max_length=100)
    caption2 = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    image = models.ImageField(help_text="Size: 1920x570")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.caption1, self.caption2)

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })

    @property
    def is_parent(self):
        return self.parent is None

    def get_children(self):
        return self.children.filter(is_active=True)

    def get_all_children(self):
        """Get all descendants"""
        children = list(self.get_children())
        for child in children:
            children.extend(child.get_all_children())
        return children


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, blank=True, null=True)
    slug = models.SlugField(unique=True)
    stock_no = models.CharField(max_length=10, unique=True)
    description_short = models.CharField(max_length=200, blank=True, null=True)
    description_long = models.TextField()
    image = models.ImageField(upload_to='products/')
    stock_quantity = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Weight in kg")
    dimensions = models.CharField(max_length=50, blank=True, null=True, help_text="L x W x H in cm")
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    seo_title = models.CharField(max_length=60, blank=True, null=True)
    seo_description = models.CharField(max_length=160, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_display_price(self):
        """Prix principal affiche: toujours le plus bas."""
        if self.discount_price is None:
            return self.price
        return min(self.price, self.discount_price)

    def get_original_price(self):
        """Prix barre affiche: le plus eleve si deux prix differents existent."""
        if self.discount_price is None:
            return None
        if self.discount_price == self.price:
            return None
        return max(self.price, self.discount_price)

    def has_price_difference(self):
        return self.get_original_price() is not None


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.get_display_price()

    def get_amount_saved(self):
        original_price = self.item.get_original_price()
        if original_price is None:
            return 0
        return (self.quantity * original_price) - self.get_total_discount_item_price()

    def get_final_price(self):
        return self.quantity * self.item.get_display_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'BillingAddress', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'BillingAddress', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a BillingAddress
    (Failed Checkout)
    3. Payment
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, default='')
    country = models.CharField(max_length=100, default='')
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'BillingAddresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


# ================================
# Dashboard Models
# ================================

class SiteSettings(models.Model):
    """Configuration globale du site"""
    site_name = models.CharField(max_length=100, default='Django Shop')
    site_email = models.EmailField(default='contact@djangoshop.com')
    notification_email = models.EmailField(
        blank=True,
        help_text="Email de l'administrateur qui reçoit les notifications de commande"
    )
    whatsapp_number = models.CharField(max_length=20, blank=True)
    whatsapp_default_message = models.CharField(
        max_length=255,
        blank=True,
        default='Bonjour, je souhaite obtenir un devis pour des gaines electriques.'
    )
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    # Hero / contenu accueil
    hero_title = models.CharField(max_length=120, default='Solutions de gaines electriques professionnelles')
    hero_subtitle = models.TextField(blank=True, default='Des references fiables pour vos chantiers residentiels et industriels.')
    hero_cta_text = models.CharField(max_length=60, default='Decouvrir les produits')
    hero_cta_link = models.CharField(max_length=255, default='/shop/')
    hero_badge_text = models.CharField(max_length=80, default='Materiel electrique professionnel')
    hero_secondary_cta_text = models.CharField(max_length=60, default='Gerer le contenu')
    hero_secondary_cta_link = models.CharField(max_length=255, default='/dashboard/')

    # Couleurs globales (pilotables depuis dashboard)
    primary_color = models.CharField(max_length=7, default='#facc15')
    primary_hover_color = models.CharField(max_length=7, default='#eab308')
    secondary_color = models.CharField(max_length=7, default='#0a0a0a')
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # Logo and Branding
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Settings
    currency = models.CharField(max_length=10, default='FCFA')
    items_per_page = models.IntegerField(default=12)
    enable_reviews = models.BooleanField(default=True)
    enable_wishlist = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name


class SiteImage(models.Model):
    """Images statiques du site (bannières, logos, etc.)"""
    IMAGE_TYPES = (
        ('top_carousel', 'Carousel pleine largeur'),
        ('banner', 'Bannière'),
        ('footer', 'Footer'),
        ('hero', 'Hero Section'),
        ('logo', 'Logo'),
        ('favicon', 'Favicon'),
        ('marketing', 'Marketing'),
        ('other', 'Autre'),
    )
    
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='site-images/')
    description = models.TextField(blank=True)
    alt_text = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['image_type', 'order']

    def __str__(self):
        return f"{self.title} ({self.image_type})"


class Contact(models.Model):
    """Messages de contact des visiteurs"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    replied_at = models.DateTimeField(blank=True, null=True)
    reply_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Review(models.Model):
    """Avis produits"""
    RATING_CHOICES = (
        (1, '1 étoile'),
        (2, '2 étoiles'),
        (3, '3 étoiles'),
        (4, '4 étoiles'),
        (5, '5 étoiles'),
    )
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    admin_response = models.TextField(blank=True)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('item', 'user')

    def __str__(self):
        return f"{self.title} - {self.item.title}"


class Promotion(models.Model):
    """Promotions et codes promo"""
    DISCOUNT_TYPES = (
        ('percentage', 'Pourcentage'),
        ('fixed', 'Montant fixe'),
    )
    
    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_uses = models.IntegerField(blank=True, null=True)
    used_count = models.IntegerField(default=0)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    items = models.ManyToManyField(Item, blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        if self.max_uses and self.used_count >= self.max_uses:
            return False
        if now < self.start_date or now > self.end_date:
            return False
        return self.is_active


class PageView(models.Model):
    """Suivi des visites quotidiennes par page"""
    path = models.CharField(max_length=500)
    date = models.DateField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('path', 'date')
        ordering = ['-date', '-count']

    def __str__(self):
        return f"{self.date} | {self.path} ({self.count})"

    @classmethod
    def record(cls, path):
        today = timezone.now().date()
        obj, created = cls.objects.get_or_create(path=path, date=today)
        cls.objects.filter(pk=obj.pk).update(count=models.F('count') + 1)


class UserProfile(models.Model):
    """Profil étendu de l'utilisateur (photo de profil, etc.)"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

    @classmethod
    def get_or_create_for_user(cls, user):
        profile, _ = cls.objects.get_or_create(user=user)
        return profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
