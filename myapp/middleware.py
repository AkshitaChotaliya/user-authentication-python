from django.http import JsonResponse

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith('/api/sales/'):
            return self.get_response(request)

        open_paths = [
            '/signup/', '/login/', '/logout/', '/password-reset/',
            '/password-reset/confirm/', '/webhook/', '/register/'
        ]

        if request.path.startswith('/api/auth') in open_paths:
            print(f"[API LOG] {request.method} {request.path}")
        else:
            if not request.user.is_authenticated:
                return JsonResponse({'detail': 'Authentication required.'}, status=401)

        response = self.get_response(request)
        return response
