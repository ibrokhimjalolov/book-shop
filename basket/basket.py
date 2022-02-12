

from decimal import Decimal
from store.models import Product


class Basket():
    def __init__(self, request) -> None:
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket
    
    def add(self, product, productqty):
        product_id = str(product.id)
        self.basket[product_id] = {
                'price': str(product.price),
                'qty': int(productqty)
            }
        self.save()

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def __iter__(self):
        products = Product.objects.filter(id__in=self.basket.keys())
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def update(self, product_id, product_qty):
        product_id = str(product_id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_qty
        self.save()

    def save(self):
        self.session.modified = True
