from .models import SiteSettings, Order, Contact, Review, Category, SiteImage, Slide, UserProfile


def site_settings(request):
    """Inject SiteSettings into all templates"""
    try:
        settings = SiteSettings.objects.first()
    except Exception:
        settings = None
    return {'site_settings': settings}


def cart_count(request):
    """Inject cart item count into all templates"""
    count = 0
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            count = order.items.count()
        except Order.DoesNotExist:
            count = 0
    return {'cart_count': count}


def dashboard_notifications(request):
    """Inject dashboard notification counts for sidebar badges"""
    data = {'unread_messages': 0, 'unapproved_reviews': 0}
    if request.user.is_authenticated and request.user.is_staff:
        try:
            data['unread_messages'] = Contact.objects.filter(is_read=False).count()
            data['unapproved_reviews'] = Review.objects.filter(is_approved=False).count()
        except Exception:
            pass
        try:
            data['user_profile'] = UserProfile.get_or_create_for_user(request.user)
        except Exception:
            data['user_profile'] = None
    return data


def global_store_content(request):
    """Inject dynamic content managed via dashboard for all storefront templates"""
    try:
        top_categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by('order', 'title')
    except Exception:
        top_categories = []

    try:
        top_carousel_images = SiteImage.objects.filter(image_type='top_carousel', is_active=True).order_by('order')
    except Exception:
        top_carousel_images = []

    try:
        hero_images = SiteImage.objects.filter(image_type='hero', is_active=True).order_by('order')
    except Exception:
        hero_images = []

    try:
        marketing_images = SiteImage.objects.filter(image_type='marketing', is_active=True).order_by('order')
    except Exception:
        marketing_images = []

    try:
        banner_images = SiteImage.objects.filter(image_type='banner', is_active=True).order_by('order')
    except Exception:
        banner_images = []

    try:
        footer_images = SiteImage.objects.filter(image_type='footer', is_active=True).order_by('order')
    except Exception:
        footer_images = []

    try:
        active_slides = Slide.objects.filter(is_active=True).order_by('-id')
    except Exception:
        active_slides = []

    return {
        'top_categories': top_categories,
        'top_carousel_images': top_carousel_images,
        'hero_images': hero_images,
        'marketing_images': marketing_images,
        'banner_images': banner_images,
        'footer_images': footer_images,
        'active_slides': active_slides,
    }
