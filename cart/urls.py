from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='view_cart'),  # contoh view keranjang
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('get-alamat/<int:alamat_id>/', views.get_alamat, name='get_alamat'),
    path('get-data-hitungan/<int:alamat_id>/<int:ekspedisi_detail_id>/', views.get_data_hitungan, name='get_data_hitungan'),
    path('get-ekspedisi-details/<int:ekspedisi_id>/', views.get_ekspedisi_details, name='get_ekspedisi_details'),  # contoh ekspedisi
    path('get-ongkir/<int:ekspedisi_detail_id>/', views.get_ongkir, name='get_ongkir'),  # contoh ongkos kirim
    path('checkout/', views.checkout, name='checkout'),  # contoh checkout
    path('order-success/', views.order_success, name='order_success'),  # contoh sukses checkout
    path('payment/<str:snap_token>/<int:order_id>/', views.payment_midtrans, name='payment'),
]
