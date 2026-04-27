from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.db.models import Q
from django.db.models import F
from django.utils import timezone
from urllib.parse import quote
from .forms import CheckoutForm, CouponForm, RefundForm
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon, Refund, Category, SiteSettings

import random
import string


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def build_order_email_message(order, email, city, notes=''):
    products = []
    for order_item in order.items.all():
        products.append(
            f"- {order_item.item.title} | Ref: {order_item.item.stock_no} | Quantite: {order_item.quantity} | Total: {order_item.get_final_price()}"
        )

    delivery_address = order.billing_address
    address_lines = []
    if delivery_address:
        address_lines.extend([
            delivery_address.street_address,
            delivery_address.apartment_address,
            city,
            delivery_address.country,
            delivery_address.zip,
        ])

    return (
        f"Une nouvelle demande de commande a ete effectuee sur le site.\n\n"
        f"Client: {order.user.get_username()}\n"
        f"Email confirme: {email}\n"
        f"Reference commande: {order.ref_code or 'a generer'}\n"
        f"Montant total: {order.get_total()}\n"
        f"Adresse de livraison: {', '.join([line for line in address_lines if line])}\n"
        f"Notes: {notes or 'Aucune'}\n\n"
        f"Produits demandes:\n" + "\n".join(products)
    )


class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            return render(request, "payment.html", context)
        else:
            messages.warning(request, "Vous n'avez pas ajouté une adresse de facturation")
            return redirect("core:checkout")

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        # Simulate payment
        payment = Payment()
        payment.stripe_charge_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        payment.user = request.user
        payment.amount = order.get_total()
        payment.save()

        order.ordered = True
        order.payment = payment
        order.ref_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        order.save()

        messages.success(request, "Commande passée avec succès!")
        return redirect("/")


class HomeView(ListView):
    template_name = "index.html"
    queryset = Item.objects.filter(is_active=True, is_featured=True)
    context_object_name = 'items'

    def get_queryset(self):
        featured = Item.objects.filter(is_active=True, is_featured=True)[:8]
        if featured.exists():
            return featured
        return Item.objects.filter(is_active=True).order_by('-created_at')[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_items'] = Item.objects.filter(is_active=True).order_by('-created_at')[:8]
        return context


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'object': order
            }
            return render(request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(request, "Vous n'avez pas de commande active")
            return redirect("/")


class ShopView(ListView):
    model = Item
    paginate_by = 6
    template_name = "shop.html"

    def get_queryset(self):
        queryset = Item.objects.filter(is_active=True).select_related('category').order_by('-created_at')

        category_slug = self.request.GET.get('category')
        search = self.request.GET.get('q')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description_short__icontains=search) |
                Q(description_long__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category'] = self.request.GET.get('category', '')
        context['query'] = self.request.GET.get('q', '')
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-detail.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Incrémenter le compteur de vues de manière atomique
        Item.objects.filter(pk=self.object.pk).update(view_count=F('view_count') + 1)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_items'] = Item.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(pk=self.object.pk)[:4]

        settings = SiteSettings.objects.first()
        wa_number = ''
        if settings:
            wa_number = settings.whatsapp_number or settings.phone_number or ''
        wa_number = wa_number.replace('+', '').replace(' ', '')

        if wa_number:
            product_url = self.request.build_absolute_uri(self.object.get_absolute_url())
            message = (
                f"Bonjour, je suis interesse par ce produit: {self.object.title}. "
                f"Reference: {self.object.stock_no}. "
                f"Lien: {product_url}"
            )
            context['product_whatsapp_link'] = f"https://wa.me/{wa_number}?text={quote(message)}"
        else:
            context['product_whatsapp_link'] = ''

        return context


# class CategoryView(DetailView):
#     model = Category
#     template_name = "category.html"

class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        item = Item.objects.filter(category=category, is_active=True).order_by('-created_at')
        context = {
            'object_list': item,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image,
            'selected_category': category.slug,
            'query': '',
        }
        return render(self.request, "category.html", context)


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            initial = {'email': request.user.email}
            form = CheckoutForm(initial=initial)
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(request, "checkout.html", context)

        except ObjectDoesNotExist:
            messages.info(request, "Vous n'avez pas de commande active")
            return redirect("core:checkout")

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST or None)
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                city = form.cleaned_data.get('city')
                zip = form.cleaned_data.get('zip')
                notes = form.cleaned_data.get('notes')

                request.user.email = email
                request.user.save(update_fields=['email'])

                billing_address = BillingAddress(
                    user=request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    city=city,
                    country=country,
                    zip=zip,
                    address_type='B'
                )
                billing_address.save()
                order.billing_address = billing_address
                order.ref_code = order.ref_code or create_ref_code()
                order.ordered = True
                order.ordered_date = timezone.now()
                order.save()

                subject = f"Nouvelle commande a livrer - {order.user.get_username()}"
                message = build_order_email_message(order, email, city, notes)

                # Lire l'email admin depuis SiteSettings (configurable depuis le dashboard)
                site_cfg = SiteSettings.objects.first()
                admin_recipient = (
                    (site_cfg.notification_email if site_cfg and site_cfg.notification_email else None)
                    or getattr(settings, 'ORDER_NOTIFICATION_EMAIL', None)
                    or settings.DEFAULT_FROM_EMAIL
                )

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_recipient],
                    fail_silently=False,
                )

                send_mail(
                    f"Confirmation de votre demande - {order.ref_code}",
                    (
                        f"Bonjour {order.user.get_username()},\n\n"
                        f"Votre demande de commande a bien ete transmise a notre equipe.\n"
                        f"Reference: {order.ref_code}\n"
                        f"Montant estime: {order.get_total()}\n\n"
                        f"Nous vous contacterons tres bientot pour organiser la livraison."
                    ),
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True,
                )

                messages.success(
                    request,
                    "Votre commande a bien été enregistrée. Notre équipe vous contactera sous peu pour organiser la livraison."
                )
                return redirect('core:home')
        except ObjectDoesNotExist:
            messages.error(request, "Vous n'avez pas de commande active")
            return redirect("core:order-summary")


# def home(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "index.html", context)
#
#
# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "product-detail.html", context)
#
#
# def shop(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "shop.html", context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "La quantite du produit a ete mise a jour.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Produit ajoute au panier.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Produit ajoute au panier.")
    return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Produit retire du panier.")
            return redirect("core:order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Ce produit n'est pas dans votre panier.")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "Vous n'avez pas de commande active.")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "La quantite du produit a ete mise a jour.")
            return redirect("core:order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Ce produit n'est pas dans votre panier.")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "Vous n'avez pas de commande active.")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "Ce coupon n'existe pas")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Coupon ajoute avec succes")
                return redirect("core:checkout")

            except ObjectDoesNotExist:
                messages.info(self.request, "Vous n'avez pas de commande active")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist")
                return redirect("core:request-refund")
