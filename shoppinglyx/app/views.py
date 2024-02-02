from django.shortcuts import render,redirect
from .models import Customer,Product,Cart,OrderPlaced
from django.db.models import Q
from django.views import View
from .forms import UserRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
 def get(self,request):
  topwear = Product.objects.filter(category="TW")
  mobile = Product.objects.filter(category="M")
  bottomwear = Product.objects.filter(category="BW")
  laptop = Product.objects.filter(category="L")
  current_items = 0
  if request.user.is_authenticated:
   current_items = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/home.html',{'topwear':topwear,'bottomwear':bottomwear,"mobile":mobile,'laptop':laptop,'current_items':current_items})
# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  item_already_exist = False
  if request.user.is_authenticated:
   item_already_exist = Cart.objects.filter(Q(product=product.id) & Q(user= request.user)).exists()
  current_items = 0
  if request.user.is_authenticated:
   current_items = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/productdetail.html',{"product":product,'item_already_exist':item_already_exist,'current_items':current_items})

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 cart_item, created = Cart.objects.get_or_create(user=user,product=product)
 if created:
  cart_item.quantity = 1
 else:
  cart_item.quantity += 1
 cart_item.save()
 current_items = 0
 if request.user.is_authenticated:
  current_items = len(Cart.objects.filter(user=request.user))
 return redirect('/show_cart',{'current_items':current_items})

@login_required
def show_cart(request):
 if request.user.is_authenticated:
  current_items = 0
  current_items = len(Cart.objects.filter(user=request.user))
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_cost = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user==user]
  if cart_product:
   for p in cart_product:
    temp_amount = (p.quantity * p.product.discounted_price)
    amount += temp_amount
    total = amount + shipping_cost
   return render(request,'app/addtocart.html',{'carts':cart,'amount':amount,'total':total,'current_items':current_items})
  else:
   return render(request,'app/emptycart.html',{'current_items':current_items})

@login_required  
def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q (product=prod_id) & Q(user=request.user))
  c.quantity += 1
  c.save()
  amount = 0.0
  shipping_cost = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user==request.user]
  if cart_product:
   for p in cart_product:
    temp_amount = (p.quantity * p.product.discounted_price)
    amount += temp_amount

  data = {
   'quantity' : c.quantity,
   'amount' : amount,
   'total' : amount + shipping_cost
    }
  return JsonResponse(data)
 
#minus cart func
@login_required
def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q (product=prod_id) & Q(user=request.user))
  c.quantity -= 1
  c.save()
  amount = 0.0
  shipping_cost = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user==request.user]
  if cart_product:
   for p in cart_product:
    temp_amount = (p.quantity * p.product.discounted_price)
    amount += temp_amount

  data = {
   'quantity' : c.quantity,
   'amount' : amount,
   'total' : amount + shipping_cost
    }
  return JsonResponse(data)
#Remove cart product func
@login_required
def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q (product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_cost = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user==request.user]
  if cart_product:
   for p in cart_product:
    temp_amount = (p.quantity * p.product.discounted_price)
    amount += temp_amount

  data = {
   'amount' : amount,
   'total' : amount + shipping_cost
    }
  return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self,request):
  form = CustomerProfileForm()
  current_items = 0
  if request.user.is_authenticated:
   current_items = len(Cart.objects.filter(user=request.user))
  return render(request,'app/profile.html',{'form':form,'current_items':current_items,'active':'btn-primary'})
 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   zipcode = form.cleaned_data['zipcode']
   state = form.cleaned_data['state']
   store = Customer(user=usr,name=name,locality=locality,city=city,zipcode=zipcode,state=state)
   store.save()
   current_items = 0
  if request.user.is_authenticated:
   current_items = len(Cart.objects.filter(user=request.user))
   messages.success(request,"Congratulation profile updated successfully!!")
  form = CustomerProfileForm()
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary','current_items':current_items})
 
@login_required
def address(request):
 address = Customer.objects.filter(user=request.user)
 current_items = 0
 if request.user.is_authenticated:
  current_items = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/address.html',{'address':address,'active':
 'btn-primary','current_items':current_items})

@login_required
def orders(request):
 order_placed = OrderPlaced.objects.filter(user=request.user)
 current_items = 0
 if request.user.is_authenticated:
  current_items = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/orders.html',{'order_placed':order_placed,'current_items':current_items})



def mobile(request, data=None):
 if data == None:
  mobiles = Product.objects.filter(category="M")
 elif data == "Oppo" or data == "Samsung":
  mobiles = Product.objects.filter(category="M").filter(brand=data)
 elif data == "Below":
  mobiles = Product.objects.filter(category="M").filter(discounted_price__lt=50000)
 elif data == "Above":
  mobiles = Product.objects.filter(category="M").filter(discounted_price__gt=50000)
 current_items = 0
 if request.user.is_authenticated:
  current_items = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/mobile.html',{"mobiles":mobiles,'current_items':current_items})

def laptop(request, data=None):
 if data == None:
  laptop = Product.objects.filter(category="L")
 elif data == "Dell" or data == "HP":
  laptop = Product.objects.filter(category="L").filter(brand=data)
 elif data == "Below":
  laptop = Product.objects.filter(category="L").filter(discounted_price__lt=150000)
 elif data == "Above":
  laptop = Product.objects.filter(category="L").filter(discounted_price__gt=50000)
 current_items = 0
 if request.user.is_authenticated:
  current_items = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/laptop.html',{"laptop":laptop,'current_items':current_items})

def topwear(request, data=None):
 if data == None:
  topwear = Product.objects.filter(category="TW")
 elif data == "Below":
  topwear = Product.objects.filter(category="TW").filter(discounted_price__lt=600)
 elif data == "Above":
  topwear = Product.objects.filter(category="TW").filter(discounted_price__gt=1000)
 current_items = 0
 if request.user.is_authenticated:
  current_items = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/topwear.html',{"topwear":topwear,'current_items':current_items})

def bottomwear(request, data=None):
 if data == None:
  bottomwear = Product.objects.filter(category="BW")
 elif data == "Below":
  bottomwear = Product.objects.filter(category="BW").filter(discounted_price__lt=600)
 elif data == "Above":
  bottomwear = Product.objects.filter(category="BW").filter(discounted_price__gt=1000)
 current_items = 0
 if request.user.is_authenticated:
  current_items = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/bottomwear.html',{"bottomwear":bottomwear,'current_items':current_items})

def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
  def get(self, request):
    form = UserRegistrationForm()
    return render(request, 'app/customerregistration.html',{"form":form})
  def post(self, request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
     messages.success(request, "Congratulation Registered Successfully")
     form.save()
     form = UserRegistrationForm()
    return render(request, 'app/customerregistration.html',{"form":form})
@login_required
def checkout(request):
 usr = request.user
 address = Customer.objects.filter(user=usr)
 cart_items = Cart.objects.filter(user=usr)
 if request.user.is_authenticated:
   current_items = len(Cart.objects.filter(user=request.user))
 amount = 0.0
 shipping_cost = 70.0
 cart_product = [p for p in Cart.objects.all() if p.user==request.user]
 if cart_product:
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
   total = amount + shipping_cost
 return render(request, 'app/checkout.html',{'address':address,'cart_items':cart_items,'total':total,'current_items':current_items})

@login_required
def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
  c.delete()
 return redirect('orders')