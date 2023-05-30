from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .models.product import Product
from .models.category import Category
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView, DetailView, ListView
from django.contrib.auth import login 
from .forms import *
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from urllib.parse import urlencode


class HomeView(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        return redirect('home')
    

    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/{request.get_full_path()[1:]}')
    

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = Product.get_all_products()
        categories = Category.get_all_categories()
        categoryID = 'category'
        if 'category' in request.GET:
            categoryID = request.GET['category']
        else:
            categoryID = False
        if categoryID:
            products = Product.get_all_products_by_categoryId(categoryID)
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
        return render(request, 'core/products.html', data)
    


class RegisterView(FormView):
    template_name = 'users/signup.html'
    form_class = RegisterForm

    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
            
        return super(RegisterView, self).form_valid(form)
    
    
class MyLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))