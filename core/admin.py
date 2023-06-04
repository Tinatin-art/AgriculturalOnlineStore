from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product, Category, Comment, CustomUser, Order, OrderItem, Rating


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price','category',]
    list_filter = ('price', 'category')
    search_fields = ('name', 'category')


class AdminCategory(admin.ModelAdmin):
    list_display =  ['categoryName']


admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'created_at', 'ordered')
    

@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'ordered')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'product', 'created_on', 'active')
    list_filter = ('active', 'created_on', 'product')
    search_fields = ('user', 'email', 'body')
    actions = ['approve_comments']


@admin.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('name', 'surname', 'email', 'created_at',)
    # list_filter = ('created_at',)
    # search_fields = ('email', 'body')

    # add_fieldsets = (
    #     *UserAdmin.add_fieldsets, (
    #         'Custom fields', {
    #             'fields':(
    #                 'username',
    #                 'name',
    #                 'surname',
    #                 'gender',
    #                 'region',
    #                 'address',
    #                 'city',
    #                 'country',
    #                 'email',
    #                 'phone',
    #                 'image',
    #             )
    #         }
    #     )
    # )

    # fieldsets = (
    #     *UserAdmin.fieldsets, 
    #     (
    #         'Custom fields', 
    #         {
    #             'fields':(
    #                 'username',
    #                 'name',
    #                 'surname',
    #                 'gender',
    #                 'region',
    #                 'address',
    #                 'city',
    #                 'country',
    #                 'email',
    #                 'phone',
    #                 'image',
    #             )
    #         }
    #     )        
    # )