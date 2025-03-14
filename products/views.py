from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()  # Получить все товары из базы
    print(f"Number of products: {products.count()}")  # Для отладки
    return render(request, 'products/product_list.html', {'products': products})


from django.shortcuts import redirect, render, get_object_or_404
from .models import Product

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Получаем товар или 404, если его нет

    #Получаем корзину из сессии, если ее нет - создаем пустой словарь
    cart = request.session.get('cart', {})

    # Используем ID товара в качестве ключа
    product_key = str(product_id)
    
    # усли товар уже в корзине, увеличиваем количество. Если нет - добавляем.
    if product_key in cart:
        cart[product_key]['quantity'] += 1
    else:
        # Если товара еще нет, добавляем его 
        cart[product_key] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
        }


    # Сохраняем обновленную корзину в сессии
    request.session['cart'] = cart
    print('Корзина:', cart)  # Для тестирования можно посмотреть в консоли

    return redirect('product_list')  # возвращаем пользователя на страницу товара

def view_cart(request):
    cart = request.session.get('cart', {})  # Получаем корзину из сессии
    updated_cart = {}
    for product_id, item in cart.items():
        updated_cart[product_id] = {
            'name': item['name'],
            'price': float(item['price']),  # Преобразуем цены в Float
            'quantity': int(item['quantity']),  # Количество в  Int
            'total': float(item['price']) * int(item['quantity'])  #  Считаем итоговую сумму
        }
    
    total_price = sum(item['total'] for item in updated_cart.values())  # Общая сумма
    return render(request, 'products/cart.html', {
        'cart': updated_cart,
        'total_price': total_price
        })  # Передаем корзину и общ сумму в шаблон


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    # Удаляем товар из корзины, если он там есть
    product_key = str(product_id)
    if product_key in cart:
        del cart[product_key]

    # Обновляем корзину в сессии
    request.session['cart'] = cart
    return redirect('view_cart')


from django.shortcuts import render, redirect
from django.contrib import messages  # добав всплывающее сообщение
from .models import Order, OrderItem, Product
from .forms import OrderForm

def checkout(request):
    cart = request.session.get('cart', {})
    
    if not cart:  # Если корзина пуста, нельзя оформить заказ
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)

            # проверяем хватает ли товара для каждого продукта в корзине
            for product_id, item in cart.items():
                product = Product.objects.get(id=product_id)
                if item['quantity'] > product.stock:
                    messages.error(request, f"Товара '{product.name}' недостаточно в наличии!")
                    return redirect('view_cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Если все проверки пройдены, создаем заказ
            order = form.save(commit=False)
            order.total_price = sum(item['price'] * item['quantity'] for item in cart.values())  # Подсчет суммы
            order.save()

            # Сохранение товаров заказа
            for product_id, item in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    name=item['name'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Уменьшаем СТОКК только после проверки
                product.stock -= item['quantity']
                product.save()
        # Очистка корзины после оформления заказа
        request.session['cart'] = {}
        return render(request, 'products/thank_you.html', {'order': order})  # Спасибо за заказ!
    else:
        form = OrderForm()

    return render(request, 'products/checkout.html', {'form': form})
