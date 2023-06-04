from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from .models.product import Product
from .models.category import Category
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.views.generic.edit import FormMixin
from django.contrib.auth import login
from .models.auth import RegisterForm
from django.views.generic import FormView, DetailView, DeleteView, CreateView, UpdateView
from django.views import View
from .models.orders import Order, OrderItem
from .models.comment import CommentForm
from django.conf import settings
import uuid
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models import Avg
from .models.profile import Profile
from .models.rating import Rating, RatingForm

class HomeView(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        return redirect('home')

    def get(self, request):
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

def register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is taken.')
                return redirect('signup')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is taken.')
                return redirect('signup')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(
                user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('token_send')

        except Exception as e:
            print(e)

    return render(request, 'users/signup.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('home')


def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def token_send(request):
    return render(request, 'users/token_send.html')


def error_page(request):
    return render(request, 'users/error.html')


class MyLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'core/cart.html', {'products': products})


@login_required
def checkout(request):
    ids = list(request.session.get('cart').keys())
    products = Product.get_products_by_id(ids)
    return render(request, 'core/checkout.html', {'products': products})


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

        order = Order.objects.create(user=request.user, first_name=first_name, last_name=last_name,
                                     email=email, phone=phone, address=address, zipcode=zipcode, place=place)

        for item in products:
            product = item
            quantity = cart.get(str(product.id))
            price = product.price * quantity

            item = OrderItem.objects.create(
                order=order, product=product, price=price, quantity=quantity)

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
        return reverse_lazy('detail', kwargs={'pk': self.get_object().id})

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
