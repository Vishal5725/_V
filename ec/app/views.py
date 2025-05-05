from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist
from .forms import  CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q
from django.conf import settings
import razorpay
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
#from django.core.mail import send_mail
# Create your views here.

def home(request):
    '''  send_mail(
    'Testing mail',
    'Here is the message.',
    'djangoapp05@gmail.com',
    ['vg016600@gmail.com'],
    fail_silently=False,
   )'''
    totalitem = 0
    totalitem_wl = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalitem_wl = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/home.html',locals())

def about(request):
    totalitem = 0
    totalitem_wl = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalitem_wl = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/about.html',locals())


def Contact(request):
    totalitem = 0
    totalitem_wl = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalitem_wl = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/contact.html',locals())

@login_required
def feedback(request):
    totalitem = 0
    totalitem_wl = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalitem_wl = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/feedback.html',locals())

class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        totalitem_wl = 0
        if request.user.is_authenticated:
             totalitem = len(Cart.objects.filter(user=request.user))
             totalitem_wl = len(Wishlist.objects.filter(user=request.user))
        product=Product.objects.filter(category=val)
        title =Product.objects.filter(category=val).values('title')
        return render(request,'category.html',locals())
    
class Categorytitle(View):
    def get(self,request,val):
        totalitem = 0
        totalitem_wl = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            totalitem_wl = len(Wishlist.objects.filter(user=request.user))             
        product=Product.objects.filter(title=val)
        title =Product.objects.filter(category=product[0].category).values('title')
        return render(request,'category.html',locals())

#@method_decorator(login_required,name='dispatch')
class ProductDetails(View):
    def get(self,request,pk):
        totalitem = 0
        totalitem_wl = 0
        if request.user.is_authenticated:
            product=Product.objects.get(pk=pk)
            wishlist=Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
            totalitem = len(Cart.objects.filter(user=request.user))
            totalitem_wl = len(Wishlist.objects.filter(user=request.user))
        else :
            return redirect("login")
        return render(request,'app/product_details.html',locals())

class  CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()   
        return render(request, 'app/customerregistration.html', locals())
    def post(self,request):
         form = CustomerRegistrationForm(request.POST)
         if form.is_valid():
             form.save()
             messages.success(request,"Hurrey! You Have Successfully Registered")
             return redirect('login')
         else:
             messages.warning(request,"Invalid Input ")
         return render(request, 'app/customerregistration.html', locals())
            
  
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        Form = CustomerProfileForm()
        totalitem = 0
        totalitem_wl = 0
        if request.user.is_authenticated:
             if Customer.objects.filter(user=request.user).exists():
              totalitem = len(Cart.objects.filter(user=request.user))
              totalitem_wl = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())
        
    def post(self,request):
        Form = CustomerProfileForm(request.POST)
        if Form.is_valid():
            user = request.user
            name = Form.cleaned_data['name']
            locality = Form.cleaned_data['locality']
            city = Form.cleaned_data['city']
            mobile = Form.cleaned_data['mobile']
            state = Form.cleaned_data['state']
            zipcode = Form.cleaned_data['zipcode']
            reg = Customer( user = user, name=name, locality = locality, mobile = mobile, city = city, state = state, zipcode = zipcode )
            reg.save()
            messages.success(request,"Profille Saved")
            return redirect('address')
        else :
            messages.warning(request," Invalid Input")
        return render(request, 'app/profile.html', locals())
    
@login_required
def address(request):
    totalitem = 0
    totalitem_wl = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalitem_wl = len(Wishlist.objects.filter(user=request.user))

    add = Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateaddress(View):
    def get(self,request,pk):
         totalitem = 0
         totalitem_wl = 0
         if request.user.is_authenticated:
              totalitem = len(Cart.objects.filter(user=request.user))
              totalitem_wl = len(Wishlist.objects.filter(user=request.user))
         add = Customer.objects.get(pk=pk)
         Form = CustomerProfileForm(instance=add)
         return render(request, 'app/updateadd.html', locals())
    def post(self,request,pk):
        Form = CustomerProfileForm(request.POST)
        if Form.is_valid():
           add = Customer.objects.get(pk=pk)
           add.name = Form.cleaned_data['name']
           add.locality = Form.cleaned_data['locality']
           add.city = Form.cleaned_data['city']
           add.mobile = Form.cleaned_data['mobile']
           add.state = Form.cleaned_data['state']
           add.zipcode = Form.cleaned_data['zipcode']
           add.save() 
           messages.success(request,"Profille Updated")
        else :
            messages.warning(request," Invalid Input")
        return redirect("address")
    
@login_required
def logout2(request):
    logout(request)
    return redirect('login')

@login_required
def add_to_cart(request):
    totalitem = 0
    totalitem_wl = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalitem_wl = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    totalitem_wl = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalitem_wl = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    cart =Cart.objects.filter(user=user) 
    amount=0
    for p in cart:
        value = p.quantity*p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request,'app/addtocart.html',locals())

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem = 0
        totalitem_wl = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            totalitem_wl = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount=0
        for p in cart_items:
            value = p.quantity*p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12",  'payment_capture': 1 }
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        print(order_id)
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request,'app/checkout.html',locals())
    
@login_required
def pqy_qr():
    return redirect('orders')

@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    print("pid=",payment_id,"oid=",order_id)
    #Payment.objects.create(razorpay_order_id=order_id, razorpay_payment_id=payment_id, cust_id=cust_id)
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    cart = Cart.objects.filter(user=user)
    payment.save()
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect('orders')
    
@login_required
def orders(request):
    totalitem = 0
    totalitem_wl = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalitem_wl = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/order.html',locals())


@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        cart_items = Cart.objects.filter(Q(product=prod_id) & Q(user=user))

        if not cart_items.exists():
            return JsonResponse({'error': 'Cart item not found'}, status=404)

        # In case of multiple cart items, we handle the first one and delete the rest
        c = cart_items.first()
        c.quantity += 1
        c.save()

        if cart_items.count() > 1:
            # Deleting other duplicate cart items, if any
            cart_items.exclude(id=c.id).delete()

        # Recalculate the total amount
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40  # assuming 40 is the shipping cost or additional charge

        data = {
            "quantity": c.quantity,
            "amount": amount,
            "totalamount": totalamount,
        }
        return JsonResponse(data)



@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        cart_items = Cart.objects.filter(Q(product=prod_id) & Q(user=user))

        if not cart_items.exists():
            return JsonResponse({'error': 'Cart item not found'}, status=404)

        c = cart_items.first()
        if c.quantity > 1:
            c.quantity -= 1
            c.save()
        else:
            c.delete()

        # Recalculate the total amount
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40  # assuming 40 is the shipping cost or additional charge

        data = {
            "quantity": c.quantity if c.id else 0,
            "amount": amount,
            "totalamount": totalamount,
        }
        return JsonResponse(data)
    
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        cart_items = Cart.objects.filter(Q(product=prod_id) & Q(user=user))

        if not cart_items.exists():
            return JsonResponse({'error': 'Cart item not found'}, status=404)

        cart_items.delete()

        # Recalculate the total amount
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40  # assuming 40 is the shipping cost or additional charge

        data = {
            "amount": amount,
            "totalamount": totalamount,
        }
        return JsonResponse(data)


@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'Item Added to WishList',
        }
        return JsonResponse(data)

@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message':'Item Removed to WishList',
        }
        return JsonResponse(data)

@login_required    
def wishlist(request):
        user=request.user
        wish_prod=Wishlist.objects.filter(user=user)
        totalitem = 0
        totalitem_wl = 0
        if request.user.is_authenticated:
             totalitem = len(Cart.objects.filter(user=request.user))
             totalitem_wl = len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/wishlist.html',locals())
    
def search(request):
    query = request.GET['search']
    product = Product.objects.filter(Q(title__icontains=query))
    otalitem = 0
    totalitem_wl = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalitem_wl = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/search.html',locals())