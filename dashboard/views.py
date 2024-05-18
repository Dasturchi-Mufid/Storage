from django.shortcuts import render,redirect
from django.utils.dateparse import parse_datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from . import models

from decimal import Decimal
from itertools import chain
from datetime import timedelta


@login_required(login_url='login')
def home(request):
    products = models.Product.objects.order_by('-id')[:10]
    returns = models.Returned.objects.order_by('-id')[:10]
    enters = models.Enter.objects.order_by('-id')[:10]
    outlays = models.Outlay.objects.filter(returned=False).order_by('-id')[:10]
    context = {
        'products': products,
        'returns': returns,
        'enters': enters,
        'outlays': outlays,
    }
    return render(request, 'index.html', context)


@login_required(login_url='login')
def search(request):
    query = request.GET.get('q')
    products = models.Product.objects.filter(name__icontains=query)
    context = {'products': products}
    return render(request, 'search.html',context)

@login_required(login_url='login')
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        models.Category.objects.create(name=name)
        return redirect('category_list')
    return render(request, 'category/create.html')


@login_required(login_url='login')
def category_list(request):
    categories = models.Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'category/list.html', context)


@login_required(login_url='login')
def update_category(request,code):
    category = models.Category.objects.get(code=code)
    if request.method == 'POST':
        name = request.POST.get('name')
        category.name = name
        category.save()
        return redirect('category_list')


@login_required(login_url='login')
def category_delete(request,code):
    category = models.Category.objects.get(code=code)
    category.delete()
    return redirect('category_list')

@login_required(login_url='login')
def create_product(request):
    categories = models.Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        category = models.Category.objects.get(code=request.POST.get('category_code'))
        price = request.POST.get('price')
        description = request.POST.get('description')
        product = models.Product.objects.create(
            name=name, 
            category=category, 
            price=price, 
            description=description
        )
        if request.FILES.getlist('images'):
            for img in request.FILES.getlist('images'):
                models.ProductImage.objects.create(
                    product = product,
                    image = img
            )
        
    return render(request, 'product/create.html',{'categories': categories})


@login_required(login_url='login')
def product_detail(request,code):
    product = models.Product.objects.get(code=code)
    images = models.ProductImage.objects.filter(product=product)
    context = {
        'product': product,
        'images': images,
    }
    return render(request, 'product/detail.html', context)


@login_required(login_url='login')
def product_list(request,code=None):
    products = models.Product.objects.all()
    if code:
        products = models.Product.objects.filter(category__code=code)
    context = {
        'products': products,
    }
    return render(request, 'product/list.html', context)


@login_required(login_url='login')
def update_product(request,code):

    product = models.Product.objects.get(code=code)
    categories = models.Category.objects.all()
    images = models.ProductImage.objects.filter(product=product)

    if request.method == 'POST':
        name = request.POST.get('name')
        category = models.Category.objects.get(code=request.POST.get('category_code'))
        price = request.POST.get('price')
        description = request.POST.get('description')
        product.name = name
        product.category = category
        product.price = price
        product.description = description
        product.save()

        if request.FILES.getlist('images'):
            for img in request.FILES.getlist('images'):
                models.ProductImage.objects.create(
                    product = product,
                    image = img
            )
    context = {
        'product': product,
        'categories': categories,
        'images': images,
        }
    return render(request, 'product/update.html',context)


@login_required(login_url='login')
def product_delete(request,code):
    product = models.Product.objects.get(code=code)
    product.delete()
    return redirect('product_list')


@login_required(login_url='login')
def delete_product_image(request,code):
    image = models.ProductImage.objects.get(code=code)
    image.delete()
    return redirect('update_product',code=image.product.code)


@login_required(login_url='login')
def create_enter(request):
    products = models.Product.objects.all()
    if request.method == 'POST':
        product = models.Product.objects.get(code=request.POST.get('product_code'))
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        models.Enter.objects.create(
            product = product,
            quantity = quantity,
            price = price,
        )
        return redirect('enter_list')
    context = {
        'products': products,
    }
    return render(request, 'enter/create.html', context)


@login_required(login_url='login')
def enter_list(request,code=None):
    enters = models.Enter.objects.all()
    if code:
        enters = models.Enter.objects.filter(product__code=code)
    context = {
        'enters': enters,
    }
    return render(request, 'enter/list.html', context)


@login_required(login_url='login')
def update_enter(request,code):
    enter = models.Enter.objects.get(code=code)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        enter.quantity = quantity
        enter.price = Decimal(price)
        enter.save()
        return redirect('enter_list')


@login_required(login_url='login')
def create_out(request):
    products = models.Product.objects.all()
    if request.method == 'POST':
        product = models.Product.objects.get(code=request.POST.get('product_code'))
        quantity = request.POST.get('quantity')
        models.Outlay.objects.create(
            product = product,
            quantity = quantity,
        )
        return redirect('out_list')
    context = {
        'products': products,
    }
    return render(request, 'out/create.html', context)


@login_required(login_url='login')
def out_list(request,code=None):
    outlays = models.Outlay.objects.all().order_by('-id')
    if code:
        outlays = models.Outlay.objects.filter(product__code=code)
    context = {
        'outlays': outlays,
    }
    return render(request, 'out/list.html', context)
    

@login_required(login_url='login')
def update_out(request,code):
    outlay = models.Outlay.objects.get(code=code)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        outlay.quantity = quantity
        outlay.save()
        return redirect('out_list')
    

@login_required(login_url='login')
def create_return(request):
    outlays = models.Outlay.objects.filter(returned=False)
    if request.method == 'POST' and request.POST.get('return'):
        outlay = models.Outlay.objects.get(code=request.POST.get('out_code'))
        models.Returned.objects.create(
            out = outlay,
        )
        return redirect('return_list')
    return render(request, 'return/create.html', {'outlays': outlays})


@login_required(login_url='login')
def return_list(request,code=None):
    outlays = models.Outlay.objects.filter(returned=True)
    return render(request, 'return/list.html',{'outlays': outlays})


@login_required(login_url='login')
def report(request):
    outs = models.Outlay.objects.filter(returned=False)
    enters = models.Enter.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        start_datetime = parse_datetime(start_date)
        end_datetime = parse_datetime(end_date)
        end_datetime += timedelta(days=1)
        outs = models.Outlay.objects.filter(returned=False, date__range=[start_datetime, end_datetime])
        enters = models.Enter.objects.filter(date__range=[start_datetime, end_datetime])
    reports = list(chain(outs, enters))
    reports = sorted(reports, key=lambda x: x.date)

    out_total = 0
    enter_total = 0
    for out in outs:
        out_total += out.total
    
    for enter in enters:
        enter_total += enter.total
    context = {
        'reports': reports,
        'out_total': out_total,
        'enter_total': enter_total
    }
    return render(request, 'report/report.html',context)


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'auth/login.html')


def log_out(request):
    logout(request)
    return redirect('login')