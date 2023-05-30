from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.comment import Comment

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price','category',]
    list_filter = ('price', 'category')
    search_fields = ('name', 'category')


class AdminCategory(admin.ModelAdmin):
    list_display =  ['categoryName']


admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)

@admin.register(Comment)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'product', 'created_on', 'active')
    list_filter = ('active', 'created_on', 'product')
    search_fields = ('user', 'email', 'body')
    actions = ['approve_comments']
