from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .basket import Basket
from store.models import Product



class BasketSummary(View):

    def get(self, request):
        basket = Basket(request)
        return render(request, 'basket/summary.html', {'basket': basket})


class BasketAdd(View):

    def post(self, request):
        basket = Basket(request)
        productid = int(request.POST.get('productid'))
        productqty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=productid)
        basket.add(product, productqty)
        return JsonResponse({'qty': basket.__len__()})

class BasketDelete(View):

    def post(self, request):
        basket = Basket(request)
        productid = int(request.POST.get('productid'))
        basket.delete(productid)
        response = JsonResponse({
            'subtotal': basket.get_total_price(),
            'qty': basket.__len__()
            
        })
        return response

        

class BasketUpdate(View):

    def post(self, request):
        basket = Basket(request)
        productid = int(request.POST.get('productid'))
        productqty = int(request.POST.get('productqty'))
        basket.update(productid, productqty)
        qty = basket.__len__()
        total_price = basket.get_total_price()
        response = JsonResponse({
            'qty': qty,
            'subtotal': total_price
        })
        return response