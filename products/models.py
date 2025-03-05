from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)  # Название товара
    description = models.TextField(blank=True)  # Описание (опционально)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена
    image = models.ImageField(upload_to='product_images/', blank=True)  # Фото
    stock = models.PositiveIntegerField(default=0)  # Количество оставшегося товара в наличии

    def __str__(self):
        return f"{self.name} ({self.stock} в наличии)"  # теперь название + кол-во


class Order(models.Model):
    name = models.CharField(max_length=255)  # Имя покупателя
    email = models.EmailField()  # Email
    address = models.TextField()  # Адрес доставки
    created_at = models.DateTimeField(auto_now_add=True)  # Дата заказа
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Общая сумма

    def __str__(self):
        return f"Заказ от {self.name} на сумму {self.total_price} руб."


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')  # Связь с заказом
    name = models.CharField(max_length=255)  # Название товара
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена товара
    quantity = models.PositiveIntegerField()  # Количество товара

    def __str__(self):
        return f"{self.name} x {self.quantity}"