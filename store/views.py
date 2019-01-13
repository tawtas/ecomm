from django.shortcuts import render,redirect
from .models import Product, Order
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.
def cartItem(cart):#takes cart object id's that we have in our sessions and turn them into actual objects
    items=[]#we took an empty array
    for item in cart: # we loop through
        items.append(Product.objects.get(id=int(item)))# this will basically get
    return items
def genItemsList(cart):
    cart_items = cartItem(cart)
    items_list = ""
    for item in cart_items:
        items_list += ","
        items_list += item.name
    return items_list
def priceCart(cart): # add the value of each cost of product
    cart_items = cartItem(cart)
    price=0
    for item in cart_items:
        price +=item.price
    return price

def catalog (request):
    if 'cart' not in request.session:
        request.session['cart']=[]      #array sort of stuff with keys, creating new session
    cart = request.session['cart']       # accessing a session
    request.session.set_expiry(0)         # session doesnt close until user closes the browser
    store_items= Product.objects.all()      # gives all the product present in the database
    ctx={'store_items': store_items, 'cart_size':len(cart)}#creating a dictionary with appropriate keys
    if request.method == "POST":
        cart.append(int(request.POST['obj_id']))
        return redirect('catalog')#when user hits the add to cart button whole page gets updated so that nomber of items presnt in thne cart gets updated in real time !
    return render (request,"catalog.html",ctx)

def cart (request): # will give us the content of cart
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx={'cart': cart,'cart_size':len(cart),'cart_items':cartItem(cart),'total_price':priceCart(cart)}
    return render(request,"cart.html",ctx)

def removefromcart(request):
    request.session.set_expiry(0)
    obj_to_remove = int(request.POST['obj_id'])#figures out which object is being removed based on post request
    obj_index = request.session['cart'].index(int(obj_to_remove))
    request.session['cart'].pop(obj_index)#remove it from the cart
    return redirect('cart')#redirect user to the cart page

def checkout(request):
    request.session.set_expiry(0)
    cart = request.session['cart']
    ctx={'cart':cart, 'cart_size':len(cart), 'total_price': priceCart(cart)}
    return render(request, "checkout.html", ctx)

def completeOrder(request):
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {'cart':cart, 'cart_size':len(cart), 'cart_items':cartItem(cart), 'total_price': priceCart(cart)}
    order= Order()
    order.items = genItemsList(cart)
    order.first_name = request.POST['first_name']
    order.last_name = request.POST['last_name']
    order.address = request.POST['address']
    order.city = request.POST['city']
    order.payment_data = request.POST['payment_data']
    order.fulfilled = False
    order.payment_method = request.POST['payment']
    order.save()
    request.session['cart']=[]
    return render(request, "complete_order.html", ctx)

def adminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect ("admin")
        else:
            return render(request, "admin_login",{'login':False})
    return render(request, "admin_login.html",None)
@login_required
def adminDashboard (request):
    orders = Order.objects.all()
    ctx = {'orders': orders}
    return render (request, "admin_panel.html",ctx)
