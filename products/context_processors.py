from . models import Category
from products.forms import CategoryForm
from django.shortcuts import render

def category(self):
    category = Category.objects.all()
    context = {
        'category_list': category
    }
    return context

def my_view(request):
    form = CategoryForm()
    context = {'form':form}

    return render(request, 'user/base.html', context=context)