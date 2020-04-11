from django.shortcuts import render,redirect
from .models import Product, Order
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

# Create your views here.


def cartItems(cart):
    items=[]
    for item in cart:
        items.append(Product.objects.get(id=item))
    return items

def genItemsList(cart):
    cart_items = cartItems(cart)
    items_list=""
    for item in cart_items:
        items_list += str(item.name)
        items_list +=","
    return items_list


def priceCart(cart):
    cart_items=cartItems(cart)
    price=0
    for item in cart_items:
        price+=item.price
    return price

def catalog(request):
    if 'cart' not in request.session:
        request.session['cart']=[]
    cart=request.session['cart']
    request.session.set_expiry(0)
    store_items=Product.objects.all()
    ctx = {'store_items':store_items,'cart_size':len(cart)}
    if request.method == "POST":
        cart.append(int(request.POST.get('obj_id',False)))
        return redirect('catalog')

    return render(request,"catalog.html",ctx)

def cart(request):
    if 'cart' not in request.session:
        request.session['cart']=[]
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx={'cart':cart , 'cart_size':len(cart) , 'cart_items': cartItems(cart) , 'total_price': priceCart(cart)}
    return render(request,"cart.html",ctx)

def removefromcart(request):
    request.session.set_expiry(0)
    s = request.POST['obj_id']
    s1=s[:-1]
    obj_to_remove=int(s1)
    obj_index=request.session['cart'].index(obj_to_remove)
    request.session['cart'].pop(obj_index)
    return redirect('cart')

def checkout(request):
    request.session.set_expiry(0)
    cart = request.session['cart']
    ctx={'cart':cart, 'cart_size':len(cart),'total_price': priceCart(cart) }
    return render(request,"checkout.html",ctx)

def completeOrder(request):
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {'cart':cart, 'cart_size':len(cart), 'cart_items':cartItems(cart), 'total_price': priceCart(cart)}
    order = Order()
    order.items = genItemsList(cart)
    order.first_name = request.POST['first_name']
    order.last_name = request.POST['last_name']
    order.address = request.POST['address']
    order.city = request.POST['city']
    order.payment_data = request.POST['payment_data']
    order.fulfilled = False
    order.payment_method = request.POST['payment']
    order.save()
    request.session['cart'] = []
    return render(request, "complete_order.html", ctx)


                            



def adminLogin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("admin")
        else:
            return render(request,"admin_login.html", {'login':False})
    return render(request,"admin_login.html",None)

@login_required
def adminDashboard(request):
    orders = Order.objects.all()
    ctx={'orders': orders}
    return render(request,"admin_panel.html",ctx)