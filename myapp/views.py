from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Product,Order,Customer
from .filters import OrderFilter
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import OrderForm, CreateUserForm,CustomerForm
from .decorators import unauthenticate_user,allowerd_users,admin_only



def base(request):
    h2 = 'This is home page'
    context = {'h2':h2}
    return render(request, 'base.html',context)


@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@allowerd_users(allowed_roles=['admin'])
def product(request):
    product = Product.objects.all()
    context = {'products':product}
    return render(request, 'accounts/products.html',context)


@login_required(login_url='login')
@allowerd_users(allowed_roles=['admin'])
def customer(request,id):
    customer = Customer.objects.get(id=id)

    orders = customer.order_set.all()

    orderFilter = OrderFilter(request.GET, queryset=orders)

    orders = orderFilter.qs

    context = {'customer':customer,'orders':orders,'orderFilter':orderFilter,}
    return render(request, 'accounts/customer.html',context)


@login_required(login_url='login')
@allowerd_users(allowed_roles=['admin'])
def createOrder(request):
    form = OrderForm()

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form':form}
    return render(request, 'accounts/order_create.html',context)

@login_required(login_url='login')
@allowerd_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowerd_users(allowed_roles=['admin'])
def deleteOrder(request,id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.delete()
        return redirect('dashboard')
    context = {'item':order}
    return render(request, 'accounts/delete.html',context)

@unauthenticate_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect!')
        
    context = {}
    return render(request, 'auth/login.html', context)

@unauthenticate_user
def signUpPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            # Customer.objects.create(user=user,name=username,email=email)

            messages.success(request, 'User is created for '+username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'auth/signup.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@allowerd_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending   = orders.filter(status='Pending').count()
    context = {
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,

        }
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowerd_users(allowed_roles=['customer'])
def userSetting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST,request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated!')
            

    context ={'form':form}
    return render(request,'accounts/account_setting.html', context)

