from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView, DetailView, View, CreateView, UpdateView
from django.views.generic.edit import FormMixin, DeleteView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import CustomUser, Product, Category, Comment, Order, OrderItem
from .forms import RegisterForm, CommentForm, CustomUserCreationForm, CustomUserChangeForm, UserLoginForm


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
    
# class SignUpView(CreateView):
#     template_name = 'users/signup.html'
#     form_class = UserCreationForm
#     success_url = reverse_lazy('home')
#     redirect_authenticated_user = True

#     def post(self, request, *args, **kwargs):
#         form = UserCreationForm(request.POST)

#         def form_valid(self, form):
#             user = form.save()
#             if user:
#                 login(self.request, user)
                
#             return super(RegisterView, self).form_valid(form)

class SignUpView(CreateView):
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()

        if user:
            login(self.request, user)
        return response




class RegisterView(FormView):
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
            
        return super(CustomUserCreationForm, self).form_valid(form)
    
    
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

# class ProfileView(DetailView):
#     model = CustomUser
#     template_name = 'users/profile.html'
#     context_object_name = 'user'

#     def get_success_url(self, **kwargs):
#         return reverse_lazy('profile', kwargs = {'pk': self.get_object().id })

class ProfileView(DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    form_class = CustomUserCreationForm
    context_object_name = 'user'

    # def get_object(self, queryset=None):
    #     return self.request.user

    # def get_success_url(self):
    #     return reverse_lazy('profile',  kwargs = {'pk': self.get_object().id })


class ProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/profile_update.html'
    context_object_name = 'user'

    def get_success_url(self):
         return reverse_lazy('profile_update',  kwargs = {'pk': self.get_object().id })


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

        return redirect('profile')
    return redirect('cart')
