from django.db import models
from users.models import User
from designs.models import Design
from products.models import ProductColorDetail, ProductColor
from users.models import Alamat


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    product_detail = models.ForeignKey(ProductColorDetail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

class Meta:
        unique_together = ('user', 'design', 'product_color', 'product_detail', 'is_ordered')
        ordering = ['-updated_at']  


