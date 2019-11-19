from django.contrib import admin
from shop_app.models import Product,Category,Subject,ProductIMG, Cart, CartItem, Order
# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ['image_thumb',]

class ProductIMGInline(admin.StackedInline):
    model = ProductIMG
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductIMGInline,
    ]


def make_payd(modeladmin, request, queryset):
    queryset.update(status='Оплачено')

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_payd]



make_payd.short_description = "Сделать оплачеными"

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Subject)
admin.site.register(ProductIMG, PersonAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin, )


