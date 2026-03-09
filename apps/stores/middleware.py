# apps/stores/middleware.py

from apps.stores.models import Store


class StoreMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.store = None

        host = request.get_host().split(":")[0]
        print("Host:", host)

        parts = host.split(".")

        if len(parts) > 1:
            slug = parts[0]

            try:
                print("Looking for store with slug:", slug)
                request.store = Store.objects.get(slug=slug)
                print("Store found:", request.store.name)
            except Store.DoesNotExist:
                request.store = None

        return self.get_response(request)