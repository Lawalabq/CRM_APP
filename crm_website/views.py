from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from crm_website.forms import SignUpForm, CustomerUpdateForm, CreateCustomer
from .models import Customer


# Create your views here.


def home(request):
    records = Customer.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'home.html', {'records': records})


def signout(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        form.save()
        messages.success(request, 'User created successfully')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        authenticate(request, username=username, password=password)
        return redirect('home')
    else:
        form = SignUpForm()
        print(form)
        return render(request, 'register.html', {'form': form})


@login_required
def individual_record(request, pk):
    customer = Customer.objects.get(id=pk)

    form = CustomerUpdateForm(instance=customer)
    if request.method == "POST":
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomerUpdateForm(instance=customer)

    return render(request, 'customer.html', {'customer': customer, 'form': form})


@login_required
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    customer.delete()
    messages.success(request, 'Successfully deleted')
    return redirect('home')


def create_customer(request):
    if request.method == 'POST':
        form = CreateCustomer(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreateCustomer(request.POST)
    return render(request, 'new_customer.html', {'form': form})
