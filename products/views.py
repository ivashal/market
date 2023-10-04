from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView
from .models import Category, SubCategory, Products
from .forms import CategoryForm, ProductForm, SubCategoryForm, Products
from django.urls import reverse_lazy
from cart.forms import CartAddProductForm

# def index(request):
#     return HttpResponse('This is page PRODUCTS')

def index(request):
    category = Category.objects.all()
    context = {
        'category_list': category
    }
    return render(request, 'products/index.html', context=context)

# def root_index(request):
#     return render(request, 'products/index.html')


# class CategoryCreateView(CreateView):
#     model = Category
#     fields = '__all__'
#     form = CategoryForm
#     template_name = 'products/category-form.html'
#     success_url = reverse_lazy('products:category-list')

class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    form = CategoryForm
    template_name = 'products/category-form.html'
    success_url = reverse_lazy('products:category-list')

    def my_view(request):
        form = CategoryForm()
        context = {'form':form}
        return render(request, 'users/base.html', context=context)



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


class ProductCreateView(CreateView):
    model = Products
    fields = '__all__'
    form = ProductForm
    template_name = 'products/product-form.html'
    success_url = reverse_lazy('products:index')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.all()
        return context
    
    def form_valid(self, form):
        self.instance = form.save(commit=False)
        self.instance.category_id = self.request.POST.get('category')
        self.instance.subcategory_id = self.request.POST.get('subcategory')
        self.instance.save()
        return super().form_valid(form)
    


class ProductListView(ListView):
    model = Products
    template_name = 'products/products-list.html'
    context_object_name = 'products'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        form = CartAddProductForm
        context = super().get_context_data(**kwargs)  
        context['cart_product_form'] = form
        return context

    def get_queryset(self) -> QuerySet[Any]:
        super().get_queryset()
        slug = self.request.resolver_match.kwargs['subcat_slug']
        queryset = Products.objects.filter(subcategory__slug = slug)  ## по двойному подчеркиванию мы обращаемся к полю связанной модели
        return queryset
    

def get_category(self):
    category = Category.objects.all()
    context = {
        'category_list': category
    }
    return context


class ProductDetailView(DetailView):
    model = Products
    template_name = "products/product-detail.html"
    context_object_name = 'product'
    slug_url_kwarg = 'prod_slug'


