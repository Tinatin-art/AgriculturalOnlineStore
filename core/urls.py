from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomeView, MyLoginView, RegisterView, Cart, OrderView
from .models.checkout import CheckOut

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', MyLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
    path('signup/', RegisterView.as_view(),name='signup'),
    path('cart/', Cart.as_view(), name='cart'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('check-out', CheckOut.as_view() , name='checkout'),
]