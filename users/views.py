from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Wallet,Bid
from decimal import Decimal
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        usertype = request.POST['usertype']
        errors = []

        # Check if passwords match
        if password1 != password2:
            errors.append("Passwords do not match.")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists. Please choose another.")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors.append("Email is already registered. Use a different email.")

        # If there are errors, re-render the form with error messages
        if errors:
            return render(request, 'users/register.html', {'errors': errors})

        # Create user if no errors
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.usertype = usertype
        user.save()
        return redirect('login')  # Redirect to login page after successful registration

    return render(request, 'users/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        errors = []

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page on successful login
        else:
            errors.append("Invalid username or password.")

        # Re-render the login form with error messages
        return render(request, 'users/login.html', {'errors': errors})

    return render(request, 'users/login.html')

@login_required
def wallet_view(request):
    if request.user.usertype != 'buyer':
        return redirect('home')  # Restrict access to buyers only

    wallet, created = Wallet.objects.get_or_create(buyer=request.user)

    if request.method == 'POST':
        charge_amount = Decimal(request.POST.get('charge_amount', 0))
        if charge_amount > 0:
            wallet.balance += charge_amount
            wallet.save()
            return redirect('wallet')

    return render(request, 'pages/wallet.html', {'wallet': wallet})

@login_required
def bids_history_view(request):
    if request.user.usertype != 'buyer':
        return redirect('home')  # Restrict access to buyers only

    bids = Bid.objects.filter(buyer=request.user).select_related('auction')

    return render(request, 'pages/bids_history.html', {'bids': bids})
