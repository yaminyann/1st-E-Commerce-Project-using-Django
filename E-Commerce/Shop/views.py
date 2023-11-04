from django.shortcuts import render, HttpResponseRedirect,redirect
from django.views import View
from . models import Product,Customar,Cart,OrderPlaced
from . forms import CustomarRegistration,CustomarProfile
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

# Customar Profile View
@method_decorator(login_required, name=('dispatch'))
class CustomarProfileView(View):
     def get(self,request):
          form = CustomarProfile()
          total_item_in_cart = 0
          if request.user.is_authenticated:
               total_item_in_cart = len(Cart.objects.filter(user=request.user))
          context ={
               'form':form,
               'active':'btn-success',
               'total_item_in_cart':total_item_in_cart,
          }
          return render(request, 'Shop/profile.html', context)
     
     def post(self,request):
          form = CustomarProfile(request.POST)
          if form.is_valid():
               user_d = request.user
               name_d = form.cleaned_data['name']
               division_d = form.cleaned_data['division']
               district_d = form.cleaned_data['district']
               thana_d = form.cleaned_data['thana']
               villageORroad_d = form.cleaned_data['villageORroad']
               zipcode_d = form.cleaned_data['zipcode']
               data = Customar(user=user_d,name=name_d, division=division_d, district=district_d, thana=thana_d, villageORroad=villageORroad_d, zipcode=zipcode_d)
               data.save()
               messages.success(request, 'Profile Update Successfully !')
               return HttpResponseRedirect('/profile/')
          
          total_item_in_cart = 0
          if request.user.is_authenticated:
               total_item_in_cart = len(Cart.objects.filter(user=request.user))
               data = {
                    'form':form,
                    'active':'btn-success',
                    'total_item_in_cart':total_item_in_cart
               }
          return render(request, 'Shop/profile.html',data)
     
     
# Product View
class ProductView(View):
     def get(self, request):
          gents = Product.objects.filter(category = 'GP')
          baby_fasion = Product.objects.filter(category = 'BF')
          borkha = Product.objects.filter(category = 'BK')
          saree = Product.objects.filter(category = 'S')
          lehenga = Product.objects.filter(category = 'L')
          total_item_in_cart = 0
          if request.user.is_authenticated:
               total_item_in_cart = len(Cart.objects.filter(user=request.user))
          shop_item = {
               'gents':gents,
               'baby_fasion':baby_fasion,
               'borkha':borkha,
               'saree':saree,
               'lehenga':lehenga,
               'total_item_in_cart':total_item_in_cart,
          }
          return render(request,'Shop/home.html',shop_item)


# Prodcut Details
class ProductDetails(View):
     def get(self, request, pk):
          product = Product.objects.get(pk=pk)
          item_already_in_cart = False
          if request.user.is_authenticated:
               item_already_in_cart = Cart.objects.filter(Q(prodcut=product.id) & Q(user=request.user)).exists()
               
               context ={
                    'product':product,
                    'item_already_in_cart':item_already_in_cart,
               }
          return render(request, 'Shop/productdetail.html',context)
          
          
          
# Add To Cart
@login_required
def add_to_cart(request):
     user =request.user
     product_id = request.GET.get('product_id')
     product = Product.objects.get(id=product_id)
     Cart(user=user,prodcut=product).save()
     return redirect('/mycart')



# show my Cart
@login_required
def Show_my_cart(request):
     if request.user.is_authenticated:
          user = request.user 
          cart = Cart.objects.filter(user=user)
          sub_total = 0.0
          shipping_charge = 120
          total_ammount = 0.0
          cart_product = [ product for product in Cart.objects.all() if product.user==user]
          if cart_product:
               for product in cart_product:
                    temp_ammount = (product.quantity * product.prodcut.discount_price)
                    sub_total += temp_ammount
                    total_ammount = shipping_charge + sub_total
                    
               total_item_in_cart = 0
               if request.user.is_authenticated:
                    total_item_in_cart = len(Cart.objects.filter(user=request.user))
               context = {
                    'user_cart':cart,
                    'shpping_charge':shipping_charge,
                    'sub_total':sub_total,
                    'total_ammount':total_ammount,
                    'total_item_in_cart':total_item_in_cart,
               }          
               return render(request, 'Shop/addtocart.html', context)
          else:
               return render(request, 'shop/empty_cart.html')
          
     
# Cart product Quantity Incrase
def incrase_quantity(request):
     if request.method == 'GET':
          product_id = request.GET['product_id']
          cart = Cart.objects.get(Q(prodcut=product_id) & Q(user=request.user))
          cart.quantity += 1
          cart.save()
          sub_total = 0.0
          shipping_charge = 120
          total_ammount = 0.0
          cart_product = [ product for product in Cart.objects.all() if product.user==request.user]
          for product in cart_product:
               temp_ammount = (product.quantity * product.prodcut.discount_price)
               sub_total += temp_ammount
               total_ammount = shipping_charge + sub_total
          context = {
               'quantity':cart.quantity,
               'shpping_charge':shipping_charge,
               'sub_total':sub_total,
               'total_ammount':total_ammount,
          }   
          return JsonResponse(context)    
      
# Cart product Quantity decrase
def decrase_quantity(request):
     if request.method == 'GET':
          product_id = request.GET['product_id']
          cart = Cart.objects.get(Q(prodcut=product_id) & Q(user=request.user))
          cart.quantity -=1
          cart.save()
          sub_total = 0.0
          shipping_charge = 120
          total_ammount = 0.0
          cart_product = [ product for product in Cart.objects.all() if product.user==request.user]
          for product in cart_product:
               temp_ammount = (product.quantity * product.prodcut.discount_price)
               sub_total += temp_ammount
               total_ammount = shipping_charge + sub_total
          context = {
               'quantity':cart.quantity,
               'shpping_charge':shipping_charge,
               'sub_total':sub_total,
               'total_ammount':total_ammount,
          }   
          return JsonResponse(context) 
     
     
# Cart Product Remove Item
def Remove_cart(request):
     if request.method == 'GET':
          product_id = request.GET['product_id']
          cart = Cart.objects.get(Q(prodcut=product_id) & Q(user=request.user))
          cart.delete()
          sub_total = 0.0
          shipping_charge = 120
          total_ammount = 0.0
          cart_product = [ product for product in Cart.objects.all() if product.user==request.user]
          for product in cart_product:
               temp_ammount = (product.quantity * product.prodcut.discount_price)
               sub_total += temp_ammount
               total_ammount = shipping_charge + sub_total
          context = {
               'sub_total':sub_total,
               'total_ammount':total_ammount,
          }   
          return JsonResponse(context) 
     

# Address Page
@login_required
def address(request):
     add_address = Customar.objects.filter(user=request.user)
     total_item_in_cart = 0
     if request.user.is_authenticated:
          total_item_in_cart = len(Cart.objects.filter(user=request.user))
     context = {
          'address':add_address,
          'active':'btn-success',
          'total_item_in_cart':total_item_in_cart,
     }
     return render(request, 'Shop/address.html',context)


# Change Password 
def change_password(request):
 return render(request, 'Shop/changepassword.html')

# product details page
@login_required
def buy_now(request):
     return render(request, 'Shop/buynow.html')

# Lehenta Item
def lehenga(request, data=None):
     if data == None:
          lehengas = Product.objects.filter(category='L')
     elif data == 'lubnan' or data == 'infinity':
          lehengas = Product.objects.filter(category='L').filter(brand=data)
     elif data == 'above':
          lehengas = Product.objects.filter(category='L').filter(discount_price__gt=20000)          
     elif data == 'below':
          lehengas = Product.objects.filter(category='L').filter(discount_price__lt=20000)          
     
     total_item_in_cart = 0
     if request.user.is_authenticated:
          total_item_in_cart = len(Cart.objects.filter(user=request.user))
     context = {
          'lehengas':lehengas,
          'total_item_in_cart':total_item_in_cart,
     }
     return render(request, 'Shop/lehenga.html',context)

# Saree Item
def Saree(request, data=None):
     if data == None:
          all_saree = Product.objects.filter(category='S')
     elif data == 'Shareez' or data == 'Rajshahi_Silk':
          all_saree = Product.objects.filter(category='S').filter(brand=data)
     elif data == 'above':
          all_saree = Product.objects.filter(category='S').filter(discount_price__gte=20000)         
     elif data == 'below':
          all_saree = Product.objects.filter(category='S').filter(discount_price__lte=20000)          
     
     total_item_in_cart = 0
     if request.user.is_authenticated:
          total_item_in_cart = len(Cart.objects.filter(user=request.user))
     context = {
          'all_saree':all_saree,
          'total_item_in_cart':total_item_in_cart,
     }
     return render(request, 'Shop/saree.html',context)




# Customar/User registration Form
class CustomarRegistrationView(View):
     def get(self, request):
          form = CustomarRegistration()
          context = {
               'form':form
          }
          return render(request, 'Shop/customerregistration.html',context)
     
     def post(self, request):
          form = CustomarRegistration(request.POST)
          if form.is_valid():
               messages.success(request, 'Congratulations registration successfully')
               form.save()
          context = {
               'form':form
          }
          return render(request, 'Shop/customerregistration.html',context)


# checkout prodcut page
@login_required
def checkout(request):
     user = request.user 
     address = Customar.objects.filter(user=user)
     cart_itmem = Cart.objects.filter(user=user)
     sub_total = 0.0
     shipping_charge = 120
     total_ammount = 0.0
     cart_product = [ product for product in Cart.objects.all() if product.user==request.user]
     for product in cart_product:
          temp_ammount = (product.quantity * product.prodcut.discount_price)
          sub_total += temp_ammount
          total_ammount = sub_total + shipping_charge
     
     data = {
          'address':address,
          'cart_itmem':cart_itmem,
          'sub_total':sub_total,
          'total_ammount':total_ammount,
     }
     
     return render(request, 'Shop/checkout.html',data)

# orders
@login_required
def Order_status(request):
     user = request.user 
     customar_id = request.GET.get('customarID')
     customar = Customar.objects.get(id=customar_id)
     cart = Cart.objects.filter(user=user)
     for c in cart:
          OrderPlaced(
               user= user,
               customar= customar,
               product= c.prodcut,
               quantity=c.quantity
          ).save()
          c.delete()
          
     return redirect('/orders')

# Orders status 
@login_required
def orders(request):
     order_placed = OrderPlaced.objects.filter(user=request.user)
     data ={
          'order_placed':order_placed,
     }
     return render(request, 'Shop/orders.html',data)



# Search button
def Search(request):
     if request.method == 'GET':
          quary = request.GET.get('quary')
          if quary:
               product = Product.objects.filter(title__icontains=quary)
               # cart item show
               total_item_in_cart = 0
               if request.user.is_authenticated:
                    total_item_in_cart = len(Cart.objects.filter(user=request.user))
               
               data ={
                    'product':product,
                    'total_item_in_cart':total_item_in_cart,
               }
               return render(request, 'shop/search.html', data)
          else:
               return render(request, 'shop/search.html', data)
          
     
     