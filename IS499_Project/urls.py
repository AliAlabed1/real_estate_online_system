from django.contrib import admin
from django.urls import path, include
from . import views  # Import home and other root-level views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),  # Home view in the root project
    path('logout/', views.logout_view, name='logout'),  # Logout view in root project
    path('users/', include('users.urls')),  # Users app URLs
    path('auctions/', include('auctions.urls')),  # Auctions app URLs
    path('admin/', admin.site.urls),  # Admin site
]
