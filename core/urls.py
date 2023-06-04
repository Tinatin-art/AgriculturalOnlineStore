from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    #path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', MyLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
    path('signup/', RegisterView.as_view(),name='signup'),
    path('cart/', Cart.as_view(), name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('start_order/', start_order, name='start_order'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('detail/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('detail/<int:pk>/rate/', RatingCreateView.as_view(), name='rate_product'),
    path('search_list/', search_list, name='search_list'),
]