import json
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.db import transaction, models
from .models import URLMapping
from .forms import URLForm

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["POST"])
def shorten_url(request):
    """Shortens a URL.

    Takes a POST request with a JSON body containing the URL to shorten.
    Returns a JSON response with the short code and the shortened URL.
    """
    try:
        data = json.loads(request.body)
        form = URLForm(data)
        if form.is_valid():
            original_url = form.cleaned_data['url']
            
            # Use transaction.atomic to ensure that the short code is unique
            with transaction.atomic():
                mapping = URLMapping.objects.create(original_url=original_url)
            
            short_url = request.build_absolute_uri(f'/{mapping.short_code}')
            return JsonResponse({'short_code': mapping.short_code, 'short_url': short_url}, status=201)
        else:
            return JsonResponse({'error': form.errors.as_json()}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@require_http_methods(["GET"])
def redirect_url(request, short_code):
    """Redirects to the original URL.

    Takes a short code and redirects to the original URL.
    Increments the click count for the short code.
    """
    mapping = get_object_or_404(URLMapping, short_code=short_code)
    
    # Use F() expression to avoid race conditions
    with transaction.atomic():
        mapping.clicks = models.F('clicks') + 1
        mapping.save()
        
    return HttpResponseRedirect(mapping.original_url)

@require_http_methods(["GET"])
def get_stats(request, short_code):
    """Returns analytics for a short code.

    Takes a short code and returns the original URL, click count, and creation timestamp.
    """
    mapping = get_object_or_404(URLMapping, short_code=short_code)
    return JsonResponse({
        'url': mapping.original_url,
        'clicks': mapping.clicks,
        'created_at': mapping.created_at.isoformat(),
    })