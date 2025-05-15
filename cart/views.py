from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import CartItem
from designs.models import Design
from products.models import ProductColor, ProductColorDetail
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from users.models import Alamat
from orders.models import Order, OrderItem, Ekspedisi, EkspedisiDetail, OrderPayment
from django.db import transaction   
from midtransclient import Snap
from django.conf import settings
import json
import json
from django.http import HttpResponse
import hashlib
import hmac
import base64


snap = Snap(
    is_production=settings.MIDTRANS_IS_PRODUCTION,
    server_key=settings.MIDTRANS_SERVER_KEY,
    client_key=settings.MIDTRANS_CLIENT_KEY
)


@csrf_exempt
def payment_notification(request):
    if request.method == 'POST':
        raw_body = request.body.decode('utf-8')
        data = json.loads(raw_body)

        # Verifikasi signature
        order_id = data.get('order_id')
        status_code = data.get('status_code')

        gross_amount_str = data.get('gross_amount', '0')
        gross_amount = int(float(gross_amount_str))

        signature_key = data.get('signature_key')

        my_signature = hashlib.sha512(
            (order_id + status_code + gross_amount_str + settings.MIDTRANS_SERVER_KEY).encode('utf-8')
        ).hexdigest()

        if my_signature != signature_key:
            return HttpResponse('Invalid signature', status=403)

        # Proses status pembayaran

        transaction_status = data.get('transaction_status')

        order = get_object_or_404(Order, id=order_id)
        order_payment = OrderPayment.objects.filter(order=order).first()

        with transaction.atomic():
            if order_payment:
                order_payment.transaction_status = data.get('transaction_status')
                order_payment.status_message = data.get('status_message')
                
                

                if transaction_status == 'settlement':
                    order_payment.settlement_time = data.get('settlement_time')

                    order.status = 'paid'
                    order.save()

                order_payment.save()
            else:
            # Jika tidak ada OrderPayment, buat yang baru
                OrderPayment.objects.create(
                    order=order,
                    transaction_time=data.get('transaction_time'),
                    transaction_status=data.get('transaction_status'),
                    transaction_id=data.get('transaction_id'),
                    status_message=data.get('status_message'),
                    status_code=status_code,
                    signature_key=signature_key,
                    settlement_time=data.get('settlement_time'),
                    payment_type=data.get('payment_type'),
                    merchant_id=data.get('merchant_id'),
                    gross_amount=gross_amount,
                    fraud_status=data.get('fraud_status'),
                    expiry_time=data.get('expiry_time'),
                    currency=data.get('currency'),
                    biller_code=data.get('biller_code'),
                    bill_key=data.get('bill_key')
                )

        
        # Lakukan update status pesanan di database sesuai order_id

        return HttpResponse('OK', status=200)

    return HttpResponse('Only POST allowed', status=405)

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        design_id = request.POST.get('design_id')
        color_id = request.POST.get('product_color_id')
        size_id = request.POST.get('product_detail_id')
        quantity = int(request.POST.get('quantity', 1))

        design = Design.objects.get(id=design_id)
        color = ProductColor.objects.get(id=color_id)
        detail = ProductColorDetail.objects.get(id=size_id)

        print(f"Design ID: {design_id}, Color ID: {color_id}, Size ID: {size_id}, Quantity: {quantity}")
        print(f"Design: {design}, Color: {color}, Detail: {detail}")

        # Hitung harga dari ProductColorDetail
        price = detail.price * 1
        print(f"Price: {price}")

        # Cek apakah item dengan kombinasi ini sudah ada
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            design=design,
            product_color=color,
            product_detail=detail,
            is_ordered=False,
            defaults={'quantity': quantity, 'price': price}
        )

        print(f"Cart Item: {cart_item}, Created: {created}")
        if not created:
            cart_item.quantity += quantity
            # cart_item.price += price
            cart_item.save()

        return JsonResponse({'success': True, 'message': 'Berhasil ditambahkan ke keranjang.'})

    return JsonResponse({'success': False, 'message': 'Metode tidak valid.'})

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user, is_ordered=False)
    total_price = sum(item.price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/view_cart.html', context)

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user, is_ordered=False)
    item.delete()
    return redirect('view_cart')  # atau redirect ke nama url keranjang kamu

@login_required
def get_data_hitungan(request, alamat_id, ekspedisi_detail_id):      

    cart_items = CartItem.objects.filter(user=request.user, is_ordered=False)
    sub_total = sum(item.quantity * item.price for item in cart_items)

    # return JsonResponse({'error': 'Alamat not found'}, status=404)

    if not alamat_id or not ekspedisi_detail_id:
        return {'error': 'Missing alamat_id or ekspedisi_detail_id'}

    try:
        ekspedisi_detail = EkspedisiDetail.objects.get(id=ekspedisi_detail_id, is_active=True)
        data = {
            'sub_total': sub_total,
            'ongkir': ekspedisi_detail.default_price,
            'total': sub_total + ekspedisi_detail.default_price,
        }

        return JsonResponse(data)
    except EkspedisiDetail.DoesNotExist:
        return JsonResponse({'error': 'Ekspedisi detail not found'})


@login_required
def get_alamat(request, alamat_id):    
    if alamat_id:
        try:
            alamat = Alamat.objects.get(id=alamat_id, user=request.user)
            data = {
                'id': alamat.id,
                'provinsi': alamat.provinsi.name,
                'kabupaten': alamat.kabupaten.name,
                'kecamatan': alamat.kecamatan.name,
                'kelurahan': alamat.kelurahan.name,
                'detail_alamat': alamat.detail_alamat,
                'kode_pos': alamat.kode_pos,
                'alamat_lengkap': f"{alamat.detail_alamat}, {alamat.kelurahan.name}, {alamat.kecamatan.name}, {alamat.kabupaten.name}, {alamat.provinsi.name}, Kode Pos : {alamat.kode_pos}",
                # 'hitungan': hitungan,
            }
            return JsonResponse(data)
        except Alamat.DoesNotExist:
            return JsonResponse({'error': 'Alamat not found'}, status=404)  
                
    return JsonResponse({'error': 'Missing product_color_id'}, status=400)

@login_required
def get_ongkir(request, ekspedisi_detail_id):    
    if ekspedisi_detail_id:
        try:
            ekspedisi_detail = EkspedisiDetail.objects.get(id=ekspedisi_detail_id, is_active=True)
            data = {
                'id': ekspedisi_detail.id,
                'name': ekspedisi_detail.name,
                'default_price': ekspedisi_detail.default_price,
            }
            return JsonResponse(data)
        except Ekspedisi.DoesNotExist:
            return JsonResponse({'error': 'Ekspedisi not found'}, status=404)  
        except EkspedisiDetail.DoesNotExist:
            return JsonResponse({'error': 'Ekspedisi detail not found'}, status=404)  
                
    return JsonResponse({'error': 'Missing ekspedisi_id or ekspedisi_detail_id'}, status=400)

@login_required
def get_ekspedisi_details(request, ekspedisi_id):   
    if ekspedisi_id:
        try:
            ekspedisi = Ekspedisi.objects.get(id=ekspedisi_id, is_active=True)
            ekspedisi_details = EkspedisiDetail.objects.filter(ekspedisi=ekspedisi)
            data = {
                'details': [
                    {
                        'id': detail.id,
                        'name': detail.name,                        
                    } for detail in ekspedisi_details
                ]
            }
            return JsonResponse(data)
        except Ekspedisi.DoesNotExist:
            return JsonResponse({'error': 'Ekspedisi not found'}, status=404)  
                
    return JsonResponse({'error': 'Missing ekspedisi_id'}, status=400)
    

@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user, is_ordered=False)
    alamats = Alamat.objects.filter(user=user)
    ekspedisis = Ekspedisi.objects.filter(is_active=True)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Ambil data dari request
                alamat_id = request.POST.get('alamat_id')
                alamat = Alamat.objects.get(id=alamat_id, user=user)

                service_id = request.POST.get('service_id')
                ekspedisi_detail = EkspedisiDetail.objects.get(id=service_id, is_active=True)   
                
                total_barang = sum(item.quantity * item.price for item in cart_items)
                diskon_persen = int(request.POST.get('diskon_persen', 0))
                diskon_rupiah = int(request.POST.get('diskon_rupiah', 0))
                ongkir = ekspedisi_detail.default_price
                
                total_diskon = int(total_barang * diskon_persen / 100) + diskon_rupiah
                total = total_barang - total_diskon + ongkir
                
                order = Order.objects.create(
                    user=user,
                    alamat=alamat,
                    total_harga_barang=total_barang,
                    diskon_persen=diskon_persen,
                    diskon_rupiah=diskon_rupiah,
                    ongkos_kirim=ongkir,
                    total=total,
                    ekspedisi_detail=ekspedisi_detail,
                    ekspedisi=ekspedisi_detail.ekspedisi,
                )
                
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        design=item.design,
                        product_color=item.product_color,
                        product_detail=item.product_detail,
                        quantity=item.quantity,
                        price=item.price
                    )
                    # item.is_ordered = True
                    item.save()

                snap_params = {
                    "transaction_details": {
                        "order_id": order.id,
                        "gross_amount": order.total,
                    },
                    "customer_details": {
                        "first_name": request.user.first_name or request.user.username,
                        "email": request.user.email,
                    },
                }

                # Dapatkan snap_token
                snap_token = snap.create_transaction(snap_params)['token']
                data = {
                    'order_id': order.id,
                    'snap_token': snap_token,
                    'client_key': settings.MIDTRANS_CLIENT_KEY
                }

                return JsonResponse(data)
                # return JsonResponse({'order_id': order.id, 'snap_token': snap_token, 'client_key': settings.MIDTRANS_CLIENT_KEY}, status=200)
                

        except Exception as e:
            # Opsional: log error atau tampilkan pesan kesalahan
            return render(request, 'cart/checkout.html', {
                'cart_items': cart_items,
                'alamats': alamats,
                'ekspedisis': ekspedisis,
                'error': 'Checkout gagal. Silakan coba lagi.'
            })

        
    
    # print(f"Ekspedisi: {ekspedisis}")
    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'alamats': alamats,
        'ekspedisis': ekspedisis,
    })

@login_required
def order_success(request):
    return render(request, 'cart/order_success.html', {
        'message': 'Order berhasil! Silakan cek email Anda untuk detail pesanan.',
    })

@login_required
def payment_midtrans(request, snap_token, order_id):
    # Ambil order berdasarkan order_id
    order = get_object_or_404(Order, id=order_id, user=request.user)
    data = {
        'snap_token': snap_token,
        'client_key': settings.MIDTRANS_CLIENT_KEY,
        'order': order,
    }
    return render(request, 'cart/checkout_payment.html', data)