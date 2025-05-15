from django.db import models
from users.models import User
from django.utils.text import slugify
from django.urls import reverse
import uuid
import os


def design_color_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{slugify(instance.name)}-{uuid.uuid4().hex}.{ext}"
    return os.path.join('designs', filename)

class Design(models.Model):
    designer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_designer': True})
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=design_color_image_path)
    slug = models.SlugField(max_length=200, unique=True, default="-")
    design_aktif = models.BooleanField(default=True)
    description = models.TextField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # if not self.slug:
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_url(self):
        return reverse('design_detail',args=[self.slug])

