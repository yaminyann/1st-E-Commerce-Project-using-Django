from django.contrib import admin
from . models import (
    Customar,
    Product,
    Cart,
    OrderPlaced
)

# Register your models here.
@admin.register(Customar)
class CustomarModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','division','district','thana','villageORroad','zipcode']
    
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_rice','discount_price','discription','brand','category','product_img']
    
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','prodcut','quantity']
    

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customar','product','quantity','ordered_date','status']