from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import Category, Product

def categories(request):
    return {
        'categories': Category.objects.all()
    }

class CategoryList(View):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
        return render(request, 'store/products/category.html', {
            'category': category,
            'products': products
        })

class ProductDetail(View):

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug, in_stock=True)
        return render(request, 'store/products/detail.html', {'product': product})


class AllProducts(View):
    def get(self, request):
        products = Product.products.all()
        return render(request, 'store/home.html', {'products': products})