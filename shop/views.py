from django.shortcuts import render
from designs.models import Design
from products.models import Product, ProductColor, ProductColorDetail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse



def home(request):
    best_sellers = Design.objects.all().filter(design_aktif=True)
    paginator_bs = Paginator(best_sellers,8)
    page_bs = request.GET.get('page_bs')
    paged_bs = paginator_bs.get_page(page_bs)
    bs_count = best_sellers.count()

    newests = Design.objects.all().filter(design_aktif=True).order_by('-created_at')
    paginator_newest = Paginator(newests,8)
    page_newest = request.GET.get('page_newest')
    paged_newest = paginator_newest.get_page(page_newest)
    newest_count = newests.count()

    
    context = {
        'best_sellers' : paged_bs,
        'bs_count' : bs_count,
        'newests' : paged_newest,
        'newest_count': newest_count,

    }
    return render(request, 'home.html', context)


def design_detail(request, design_slug):
    products = Product.objects.all()
    product_colors = ProductColor.objects.filter(product = products[0])
    product_color_details = ProductColorDetail.objects.filter(productcolor = product_colors[0])

    print(product_colors)
    design = Design.objects.get(slug = design_slug )


    context = {
        'design' : design,
        'products': products,
        'product_colors' : product_colors,
        'product_color_details' : product_color_details
    }
    return render(request, 'shop/design_detail.html', context)

# views.py

def get_colors(request):
    product_id = request.GET.get('product_id')
    if not product_id:
        return JsonResponse({'error': 'Product ID not provided'}, status=400)

    # Ambil data
    color_data = ProductColor.objects.filter(product_id=product_id)\
        .select_related('color')\
        .distinct()

    result = []
    for item in color_data:
        # Buat full URL untuk image kalau ada
        image_url = request.build_absolute_uri(item.image.url) if item.image else None

        result.append({
            'id': item.id,
            'image': image_url,
            'is_default': item.is_default,
            'code': item.color.code,
            'name': item.color.name
        })

    return JsonResponse(result, safe=False)

def get_sizes(request):
    product_color_id = request.GET.get('product_color_id')
    if product_color_id:
        try:
            product_color = ProductColor.objects.get(id=product_color_id)
            size_data = ProductColorDetail.objects.filter(productcolor=product_color).values('id', 'size','price')
            return JsonResponse(list(size_data), safe=False)
        except ProductColor.DoesNotExist:
            return JsonResponse({'error': 'ProductColor not found'}, status=404)
    return JsonResponse({'error': 'Missing product_color_id'}, status=400)

def register(request):
    if request.method == 'POST':
        # Handle registration logic here
        pass
    return render(request, 'shop/register.html')