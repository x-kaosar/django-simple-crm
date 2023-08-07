from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Product,Order,Customer
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from .forms import OrderForm, CreateUserForm



def base(request):
    h2 = 'This is home page'
    context = {'h2':h2}
    return render(request, 'base.html',context)

def dashboard(request):
    orders        = Order.objects.all()
    customers     = Customer.objects.all()

    total_orders  = orders.count()
    pending       = Order.objects.filter(status='Pending').count()
    delivered     = Order.objects.filter(status='Delivered').count()

    context       = {
        'orders': orders,
        'customers': customers,
        'total_orders':total_orders,
        'pending':pending,
        'delivered':delivered,


    }
    return render(request, 'accounts/dashboard.html',context)

def product(request):
    product = Product.objects.all()
    context = {'products':product}
    return render(request, 'accounts/products.html',context)

def customer(request,id):
    customer = Customer.objects.get(id=id)

    orders = customer.order_set.all()

    orderFilter = OrderFilter(request.GET, queryset=orders)

    orders = orderFilter.qs

    context = {'customer':customer,'orders':orders,'orderFilter':orderFilter,}
    return render(request, 'accounts/customer.html',context)


def createOrder(request):
    form = OrderForm()

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form':form}
    return render(request, 'accounts/order_create.html',context)


def updateOrder(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form':form}

    return render(request, 'accounts/order_create.html',context)


def deleteOrder(request,id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.delete()
        return redirect('dashboard')
    context = {'item':order}
    return render(request, 'accounts/delete.html',context)


def loginPage(request):
    context = {}
    return render(request, 'auth/login.html', context)


def signUpPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request, 'auth/signup.html', context)





