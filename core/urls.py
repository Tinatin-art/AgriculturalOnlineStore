from django.urls import path
from .views import HomeView, login_view, register_view, logout_view

urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),
    path('signin/', login_view, name="signin"),
    path('signup/', register_view, name="signup"),
    path('logout/', logout_view, name="logout")
]