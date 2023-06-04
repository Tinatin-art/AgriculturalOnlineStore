from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView, DetailView, View, CreateView, UpdateView
from django.views.generic.edit import FormMixin, DeleteView
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Avg


from .models import CustomUser, Product, Category, Comment, Order, OrderItem, Rating
from .forms import  CommentForm, CustomUserCreationForm, CustomUserChangeForm, RatingForm


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


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    form_class = CustomUserCreationForm
    context_object_name = 'user'


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

class RatingCreateView(CreateView):
    form_class = RatingForm
    context_object_name = 'user'

    def form_valid(self, form):
        pk = self.kwargs['pk']
        product = get_object_or_404(Product, id=pk)
        rating = form.save(commit=False)
        rating.user = self.request.user
        rating.product = product
        rating.save()
        product.update_average_rating()  
        return redirect('detail', pk=pk)
    
    def get_rating(self, product):
        average_rating = Rating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
        product.average_rating = average_rating
        product.save()

def search_list(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(name__icontains=query) | Q(description__icontains=query)

            results= Product.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'core/search_list.html', context)

        else:
            return render(request, 'core/search.html')

    else:
        return render(request, 'core/search.html')