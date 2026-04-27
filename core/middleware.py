from .models import PageView

# Paths à ignorer (assets statiques, dashboard, admin, API)
_SKIP_PREFIXES = (
    '/static/', '/media/', '/favicon', '/dashboard/', '/admin/',
    '/accounts/', '/__debug__/', '/api/',
)


class PageViewMiddleware:
    """
    Enregistre chaque requête GET sur les pages publiques dans PageView.
    Utilise un accès DB atomique (update-or-create + F()) pour éviter les race conditions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # On ne trace que les GET qui aboutissent à une page HTML réussie
        if (
            request.method == 'GET'
            and response.status_code == 200
            and not any(request.path.startswith(p) for p in _SKIP_PREFIXES)
        ):
            try:
                PageView.record(request.path)
            except Exception:
                pass  # Ne jamais crasher le site pour une stat

        return response
