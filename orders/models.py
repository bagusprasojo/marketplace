from django.db import models
from users.models import User, Alamat
from designs.models import Design
from products.models import ProductColorDetail, ProductColor

class Ekspedisi(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.name
    
class EkspedisiDetail(models.Model):   
    ekspedisi = models.ForeignKey(Ekspedisi, related_name='details', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    default_price = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ekspedisi.name} - {self.name}"

class OrderPayment(models.Model):
    order = models.ForeignKey('Order', related_name='payments', on_delete=models.CASCADE)
    transaction_time = models.DateTimeField()
    transaction_status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    status_message = models.CharField(max_length=255)
    status_code = models.CharField(max_length=50)
    signature_key = models.CharField(max_length=1024)
    settlement_time = models.DateTimeField(null=True, blank=True)
    payment_type = models.CharField(max_length=50)
    merchant_id = models.CharField(max_length=20)
    gross_amount = models.PositiveIntegerField(default=0)
    fraud_status = models.CharField(max_length=50)
    expiry_time = models.DateTimeField(null=True, blank=True)
    currency = models.CharField(max_length=10)
    biller_code = models.CharField(max_length=50, null=True, blank=True)
    bill_key = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.transaction_status}"

    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alamat = models.ForeignKey(Alamat, on_delete=models.CASCADE, default=1)
    total_harga_barang = models.PositiveIntegerField(default=0)  # Total harga barang tanpa diskon dan ongkos kirim
    diskon_persen = models.PositiveIntegerField(default=0)  # Diskon dalam persen
    diskon_rupiah = models.PositiveIntegerField(default=0)  # Diskon dalam rupiah    
    ongkos_kirim = models.PositiveIntegerField(default=0)  # Ongkos kirim
    total = models.PositiveIntegerField(default=0)  # Total setelah diskon dan ongkos kirim
    status = models.CharField(max_length=50, default='pending')  # Bisa: pending, paid, shipped, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    ekspedisi_detail = models.ForeignKey(EkspedisiDetail, on_delete=models.CASCADE, default=1)
    ekspedisi = models.ForeignKey(Ekspedisi, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, default=1)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    product_detail = models.ForeignKey(ProductColorDetail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    def subtotal(self):
        return self.quantity * self.price