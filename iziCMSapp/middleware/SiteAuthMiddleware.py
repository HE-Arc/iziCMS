from django.shortcuts import redirect

class SiteAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'website_id' in view_kwargs:
            website_id = view_kwargs.get('website_id', None)
            if 'site' not in request.session or request.session['site'] != int(website_id):
                return redirect('home')
        return None
