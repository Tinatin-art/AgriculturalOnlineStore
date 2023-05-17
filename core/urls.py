from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomeView, MyLoginView, RegisterView, Cart, checkout, myaccount, start_order

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', MyLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
    path('signup/', RegisterView.as_view(),name='signup'),
    path('cart/', Cart.as_view(), name='cart'),
    path('checkout/', checkout , name='checkout'),
    path('start_order/', start_order, name='start_order'),
    path('myaccount/', myaccount, name='myaccount'),
]