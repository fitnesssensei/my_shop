from django.contrib import admin
from .models import Product, Order, OrderItem

# Inline-модель для отображения товаров внутри заказа
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Не добавлять пустые дополнительные поля
    readonly_fields = ('name', 'price', 'quantity')  # Сделаем поля только для чтения

# Основная модель заказа
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'total_price', 'created_at', 'get_order_items')

    def get_order_items(self, obj):
        return ", ".join([f"{item.name} (x{item.quantity})" for item in obj.items.all()])
    
    get_order_items.short_description = "Товары"


# Регистрация остальных моделей
admin.site.register(Product)
admin.site.register(OrderItem)