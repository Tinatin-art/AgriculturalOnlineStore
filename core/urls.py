from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', MyLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
    path('signup/', RegisterView.as_view(),name='signup'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),
]