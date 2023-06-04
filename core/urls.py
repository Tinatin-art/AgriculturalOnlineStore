from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', MyLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
    path('signup/', register,name='signup'),
    path('cart/', Cart.as_view(), name='cart'),
    path('checkout/', checkout , name='checkout'),
    path('start_order/', start_order, name='start_order'),
    path('myaccount/', myaccount, name='myaccount'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('token/' , token_send , name="token_send"),
    path('verify/<auth_token>/' , verify , name="verify"),
    path('error/' , error_page , name="error"),
    path('search_list/', search_list, name='search_list'),
    path('detail/<int:pk>/rate/', RatingCreateView.as_view(), name='rate_product'),
]