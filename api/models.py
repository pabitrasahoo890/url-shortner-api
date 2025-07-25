from django.db import models
import string
import random

def generate_short_code():
    """Generate a unique short code."""
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not URLMapping.objects.filter(short_code=code).exists():
            return code

class URLMapping(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=6, unique=True, default=generate_short_code)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.short_code} -> {self.original_url}'