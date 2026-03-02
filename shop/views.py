from django.shortcuts import render, get_object_or_404
from .models import Product, ShopProductType


def product_list(request):
    product_type = request.GET.get("type")
    types = ShopProductType.objects.all()
    products = Product.objects.filter(show=True).select_related("currency", "product_type")
    if product_type:
        products = products.filter(product_type__label=product_type)
    return render(request, "shop/product_list.html", {
        "products": products,
        "types": types,
        "active_type": product_type,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, show=True)
    return render(request, "shop/product_detail.html", {"product": product})

