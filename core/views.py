from typing import Any, Dict
from django.shortcuts import render, redirect
from django.views import View
from .models.product import Product
from .models.category import Category
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView, DetailView, ListView
from django.views.generic.edit import FormMixin, DeleteView
from django.contrib.auth import login 
from .forms import *
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from urllib.parse import urlencode


class HomeView(View):
    def get(self, request, *args, **kwargs):

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
    
class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = 'core/detail.html'
    context_object_name = 'product'
    form_class = CommentForm
    object = None

    def get_success_url(self, **kwargs):
        return reverse_lazy('detail', kwargs = {'pk': self.get_object().id })
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        self.object = form.save(commit='False')
        self.object.product = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)    

class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        product_id = self.object.product_id 
        return reverse_lazy('detail', kwargs={'pk': product_id})

class Search(ListView):
    template_name = 'core/search.html'
    paginate_by = 3
    
    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query_param = self.request.GET.get("q")
        context["q"] = urlencode({'q': query_param}) + '&'
        return context