from django.db import models
import os
import uuid
from django.utils.text import slugify

def product_color_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{slugify(instance.product.name)}-{uuid.uuid4().hex}.{ext}"
    return os.path.join('product_colors', filename)


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)  # T-shirt, Hoodie, Mug

    def __str__(self):
        return self.name

class Color(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.code} - {self.name}"

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    # default_color = models.ForeignKey('ProductColor', on_delete=models.SET_NULL, null=True, blank=True, related_name='default_for_product')

    def __str__(self):
        return f"{self.name}"

class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color = models.ForeignKey(Color, on_delete=models.RESTRICT, null=True, blank=True)
    image = models.ImageField(upload_to=product_color_image_path)
    is_default = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return f"{self.product.name} - {self.color}"

class ProductColorDetail(models.Model):
    productcolor = models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name='details')
    size = models.CharField(max_length=10)  # S, M, L, XL, etc
    price = models.DecimalField(max_digits=10, decimal_places=2)
