from django import forms


class CheckoutForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Confirmez votre adresse email',
        'class': 'w-full rounded-2xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-zinc-100 outline-none focus:border-yellow-400'
    }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Quartier, rue, repere',
        'class': 'w-full rounded-2xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-zinc-100 outline-none focus:border-yellow-400'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Appartement, immeuble, complement',
        'class': 'w-full rounded-2xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-zinc-100 outline-none focus:border-yellow-400'
    }))
    country = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full rounded-2xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-zinc-100 outline-none focus:border-yellow-400',
        'placeholder': 'Pays'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full rounded-2xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-zinc-100 outline-none focus:border-yellow-400',
        'placeholder': 'Ville'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full rounded-2xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-zinc-100 outline-none focus:border-yellow-400',
        'placeholder': 'Code postal'
    }))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'w-full rounded-2xl border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-zinc-100 outline-none focus:border-yellow-400',
        'rows': 3,
        'placeholder': 'Instructions de livraison ou precision complementaire'
    }))


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-2 text-sm text-zinc-100 outline-none focus:border-yellow-400',
        'placeholder': 'Code promo'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()
