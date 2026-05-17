from django.db import models


class Coffee(models.Model):
    CATEGORY_CHOICES = [
        ('espresso', 'Espresso'),
        ('latte', 'Latte'),
        ('cappuccino', 'Cappuccino'),
        ('cold_brew', 'Cold Brew'),
        ('pour_over', 'Pour Over'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='coffees/', blank=True, null=True,
                              help_text="Upload a photo of this coffee")
    image_url = models.URLField(max_length=500, blank=True,
                                help_text="Or paste an image URL (used if no upload)")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_image(self):
        """Return uploaded image URL first, fallback to external URL."""
        if self.image:
            return self.image.url
        return self.image_url or ''

    class Meta:
        ordering = ['name']
        verbose_name = 'Coffee'
        verbose_name_plural = 'Coffees'

    def __str__(self):
        return f"{self.name} (${self.price})"
