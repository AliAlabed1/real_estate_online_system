from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from auctions.models import Auction
from django.utils.timezone import now
from django.db.models import Q
def home(request):
    current_time = now()
    search_query = request.GET.get('search', '').strip()
    search_results = None

    # Categorize auctions
    ended_auctions = Auction.objects.filter(end_date__lt=current_time)
    ongoing_auctions = Auction.objects.filter(start_date__lte=current_time, end_date__gte=current_time)
    upcoming_auctions = Auction.objects.filter(start_date__gt=current_time)

    if search_query:
        # Filter auctions based on search query
        search_results = Auction.objects.filter(
            Q(property__property_type__icontains=search_query) |
            Q(property__address__icontains=search_query)
        )
        # If the user is authenticated and a seller, limit search results to their auctions
        if request.user.is_authenticated and request.user.usertype == 'seller':
            search_results = search_results.filter(seller=request.user)

    if request.user.is_authenticated:
        if request.user.usertype == 'seller':
            # For sellers, show only their auctions
            ended_auctions = ended_auctions.filter(seller=request.user)
            ongoing_auctions = ongoing_auctions.filter(seller=request.user)
            upcoming_auctions = upcoming_auctions.filter(seller=request.user)

    # Render the template with categorized auctions and search results
    context = {
        'ended_auctions': ended_auctions,
        'ongoing_auctions': ongoing_auctions,
        'upcoming_auctions': upcoming_auctions,
        'search_results': search_results,
        'search_query': search_query,
    }
    return render(request, 'pages/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the home page or another page after logout