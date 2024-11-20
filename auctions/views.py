# auctions/views.py

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Auction, Property,Document
from django.utils.timezone import now
from users.models import Wallet,Bid
from decimal import Decimal
from django.contrib import messages
from .forms import DocumentForm
from django.http import FileResponse, Http404
import os
@login_required
def create_auction(request):
    if request.method == 'POST':
        address = request.POST['address']
        size = request.POST['size']
        property_type = request.POST['property_type']
        starting_bid = request.POST['starting_bid']
        reserve_price = request.POST['reserve_price']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        # Create property
        property_instance = Property.objects.create(
            seller=request.user,
            address=address,
            size=size,
            property_type=property_type,
        )

        # Create auction
        Auction.objects.create(
            seller=request.user,
            property=property_instance,
            starting_bid=starting_bid,
            reserve_price=reserve_price,
            start_date=start_date,
            end_date=end_date,
        )

        return redirect('home')  # Redirect to home after auction creation

    return render(request, 'auctions/create_auction.html')


@login_required
def edit_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    if request.user != auction.seller:
        return redirect('home')

    if request.method == 'POST':
        # Handle auction updates
        if 'update' in request.POST:
            auction.starting_bid = request.POST.get('starting_bid')
            auction.reserve_price = request.POST.get('reserve_price')
            auction.start_date = request.POST.get('start_date')
            auction.end_date = request.POST.get('end_date')
            auction.save()
            messages.success(request, "Auction updated successfully!")
            return redirect('home')

        # Handle end auction
        if 'end' in request.POST:
            auction.status = 'ended'
            auction.save()
            messages.success(request, "Auction ended successfully!")
            return redirect('edit_auction', auction_id=auction.id)

        # Handle delete auction
        if 'delete' in request.POST:
            auction.delete()
            messages.success(request, "Auction deleted successfully!")
            return redirect('home')

        # Handle document upload
        if 'upload_document' in request.POST:
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                document, created = Document.objects.get_or_create(auction=auction)
                document.file = form.cleaned_data['file']
                document.save()
                messages.success(request, "Document uploaded successfully!")
                return redirect('edit_auction', auction_id=auction.id)
    else:
        form = DocumentForm()

    return render(request, 'auctions/edit_auction.html', {'auction': auction, 'form': form})


@login_required
def auction_details_view(request, auction_id):
    # Fetch the auction and associated details
    auction = get_object_or_404(Auction, id=auction_id)

    # Restrict access to buyers
    if request.user.usertype != 'buyer':
        return redirect('home')

    # Get the buyer's wallet
    wallet = Wallet.objects.get(buyer=request.user)

    # Check if the auction has a document
    document = auction.document.file.url if hasattr(auction, 'document') else None

    if request.method == 'POST':
        # Handle bid submission
        bid_amount = Decimal(request.POST.get('bid_amount', '0'))
        if bid_amount > 0:
            if wallet.balance >= bid_amount:
                # Create a new bid
                Bid.objects.create(auction=auction, buyer=request.user, amount=bid_amount)
                wallet.balance -= bid_amount  # Deduct the bid amount from wallet
                wallet.save()
                messages.success(request, "Bid placed successfully!")
                return redirect('bids_history')
            else:
                messages.error(request, "Insufficient balance in your wallet.")
        else:
            messages.error(request, "Invalid bid amount.")

    return render(request, 'auctions/auction_details.html', {'auction': auction, 'wallet': wallet, 'document': document})

def download_document(request, auction_id):
    # Fetch the document associated with the auction
    document = get_object_or_404(Document, auction__id=auction_id)
    print(document.file)
    path = f'{os.getcwd()}/{document.file}'
    document.file = path
    try:
        return FileResponse(document.file.open('rb'), as_attachment=True, filename=document.file.name.split('/')[-1])
    except FileNotFoundError:
        raise Http404("Document not found.")
