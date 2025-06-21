from django.http import JsonResponse
class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/auth') or request.path in [
            '/signup/', '/login/', '/logout/', '/password-reset/',
            '/password-reset/confirm/', '/webhook/', '/register/'
        ]:
            print(f"[API LOG] {request.method} {request.path}")

        response = self.get_response(request)
        return response