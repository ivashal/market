from typing import Any, Dict
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from .models import Category, SubCategory, Products
from .forms import CategoryForm, SubCategoryForm, Products
from django.urls import reverse_lazy


def index(request):
    return HttpResponse('This is page PRODUCTS')

# def index(request):
#     # category = Category.objects.all()
#     # context = {
#     #     'category-list': category
#     # }
#     return HttpResponse(request, 'products/index.html', context=context)

def root_index(request):
    return render(request, 'products/index.html')


class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    form = CategoryForm
    template_name = 'products/category-form.html'
    success_url = reverse_lazy('products:category-list')


class CategoryListView(ListView):
    model = Category
    template_name = 'products/category-list.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:  ## Мы переопределили родительский объeкт
        context = super().get_context_data(**kwargs)
        subcategories = SubCategory.objects.all()  ## На это этапе получаем все данные о подкатегории
        context['subcategories'] = subcategories
        return context


class SubCategoryCreateViev(CreateView):
    model = SubCategory
    fields = '__all__'
    form = SubCategoryForm
    template_name = 'products/subcategory-form.html'
    success_url = reverse_lazy('products:category-list')
