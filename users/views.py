from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Wallet,Bid
from decimal import Decimal
from django.contrib.auth.decorators import user_passes_test
from auctions.models import Auction,Document

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

    bids = Bid.objects.filter(buyer=request.user).select_related('auction').order_by('-created_at')

    return render(request, 'pages/bids_history.html', {'bids': bids})

def is_admin(user):
    return user.is_authenticated and user.usertype == 'admin'

@user_passes_test(is_admin)
def manage_users_view(request):
    users = User.objects.all()
    return render(request, 'pages/manage_users.html', {'users': users})

@user_passes_test(is_admin)
def auctions_oversight_view(request):
    auctions = Auction.objects.select_related('seller', 'property')

    return render(request, 'pages/auctions_oversight.html', {'auctions': auctions})


@user_passes_test(lambda u: u.is_authenticated and u.usertype == 'admin')
def reporting_analytics_view(request):
    selected_category = request.GET.get('category', 'auctions')

    data = None
    headers = None

    if selected_category == 'auctions':
        data = Auction.objects.all()
        headers = ['ID', 'Property Type', 'Location', 'Starting Bid', 'Reserve Price', 'Start Date', 'End Date', 'Status']
    elif selected_category == 'bids':
        data = Bid.objects.select_related('auction', 'buyer').all()
        headers = ['ID', 'Auction', 'Buyer', 'Amount', 'Created At']
    elif selected_category == 'documents':
        data = Document.objects.select_related('auction').all()
        headers = ['ID', 'Auction', 'File Name', 'Uploaded At']
    elif selected_category == 'users':
        data = User.objects.all()
        headers = ['ID', 'Username', 'Email', 'User Type', 'Date Joined']

    return render(request, 'pages/reporting_analytics.html', {
        'selected_category': selected_category,
        'data': data,
        'headers': headers,
    })

@user_passes_test(is_admin)
def user_details_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Check if the current user is viewing their own details
    is_self = request.user.id == user_id

    # Handle delete action
    if request.method == 'POST' and 'delete' in request.POST:
        if not is_self:  # Prevent self-deletion
            user.delete()
            return redirect('manage_users')

    # Fetch role-specific details
    if user.usertype == 'buyer':
        bids = Bid.objects.filter(buyer=user).select_related('auction')
        return render(request, 'users/user_details.html', {
            'user': user,
            'bids': bids,
            'user_type': 'buyer',
            'is_self': is_self,
        })
    elif user.usertype == 'seller':
        auctions = Auction.objects.filter(seller=user)
        return render(request, 'users/user_details.html', {
            'user': user,
            'auctions': auctions,
            'user_type': 'seller',
            'is_self': is_self,
        })
    else:
        # Admin user
        return render(request, 'users/user_details.html', {'user': user, 'user_type': 'admin', 'is_self': is_self})
