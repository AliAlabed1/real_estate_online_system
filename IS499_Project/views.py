from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from auctions.models import Auction
from django.utils.timezone import now
def home(request):
    current_time = now()

    # Categorize auctions
    ended_auctions = Auction.objects.filter(end_date__lt=current_time)
    ongoing_auctions = Auction.objects.filter(start_date__lte=current_time, end_date__gte=current_time)
    upcoming_auctions = Auction.objects.filter(start_date__gt=current_time)

    if request.user.is_authenticated:
        if request.user.usertype == 'seller':
            # For sellers, show only their auctions
            ended_auctions = ended_auctions.filter(seller=request.user)
            ongoing_auctions = ongoing_auctions.filter(seller=request.user)
            upcoming_auctions = upcoming_auctions.filter(seller=request.user)

    # Render the template with categorized auctions
    context = {
        'ended_auctions': ended_auctions,
        'ongoing_auctions': ongoing_auctions,
        'upcoming_auctions': upcoming_auctions,
    }
    print(context)
    return render(request, 'pages/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the home page or another page after logout