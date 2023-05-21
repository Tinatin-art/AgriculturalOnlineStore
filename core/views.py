from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .models.product import Product
from .models.category import Category
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.edit import FormMixin
from django.contrib.auth import login 
from .models.auth import RegisterForm
from django.views.generic import FormView, DetailView
from django.views import  View
from .models.orders import Order, OrderItem
from .models.comment import CommentForm


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
    

class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request , 'core/cart.html',{ 'products' : products})
    
    
    
@login_required
def checkout(request):
    ids = list(request.session.get('cart').keys())
    products = Product.get_products_by_id(ids)
    return render(request, 'core/checkout.html', {'products' : products})

@login_required
def myaccount(request):
    return render(request, 'core/myaccount.html')

def start_order(request):
    cart = request.session.get('cart')
    products = Product.get_products_by_id(list(cart.keys()))

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        place = request.POST.get('place')
        phone = request.POST.get('phone')

        order = Order.objects.create(user=request.user, first_name=first_name, last_name=last_name, email=email, phone=phone, address=address, zipcode=zipcode, place=place)
        
        for item in products:
            product = item
            quantity= cart.get(str(product.id))
            price = product.price * quantity

            

            item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
 
        request.session['cart'] = {}

        return redirect('myaccount')
    return redirect('cart')


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
