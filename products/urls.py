from django.urls import path
from .views import *


app_name = 'products'
urlpatterns = [
    path('', index, name='index'),
    path('category-form/', CategoryCreateView.as_view(), name='category-form'),
    path('category-list/', CategoryListView.as_view(), name='category-list'),
    path('product-form/', ProductCreateView.as_view(), name="product-form"),
    path('subcategory-form/', SubCategoryCreateViev.as_view(), name='subcategory-form'),
    path('<slug:cat_slug>/<slug:subcat_slug>/', ProductListView.as_view(), name='product-list'),
    # path('<slug:cat_slug>/<slug:subcat_slug>/<slug:product', ProductListView.as_view(), name='product-list'),

]
