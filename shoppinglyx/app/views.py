from django.shortcuts import render
from .models import Customer,Product,Cart,OrderPlaced
from django.views import View
from .forms import UserRegistrationForm
from django.contrib import messages
# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
 def get(self,request):
  topwear = Product.objects.filter(category="TW")
  mobile = Product.objects.filter(category="M")
  bottomwear = Product.objects.filter(category="BW")
  return render(request, 'app/home.html',{'topwear':topwear,
                                          'bottomwear':bottomwear,"mobile":mobile})
# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/productdetail.html',{"product":product})


def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')



def mobile(request, data=None):
 if data == None:
  mobiles = Product.objects.filter(category="M")
 elif data == "Oppo" or data == "Samsung":
  mobiles = Product.objects.filter(category="M").filter(brand=data)
 elif data == "Below":
  mobiles = Product.objects.filter(category="M").filter(discounted_price__lt=50000)
 elif data == "Above":
  mobiles = Product.objects.filter(category="M").filter(discounted_price__gt=50000)
 return render(request, 'app/mobile.html',{"mobiles":mobiles})

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
def checkout(request):
 return render(request, 'app/checkout.html')
