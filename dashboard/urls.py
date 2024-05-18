from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('q/',views.search,name='search'),
    path('report/',views.report,name='report'),

    path('login/',views.log_in,name='login'),
    path('logout/',views.log_out,name='logout'),

    path('category/create',views.create_category,name='create_category'),
    path('category/list',views.category_list,name='category_list'),
    path('category/update/<str:code>/',views.update_category,name='update_category'),
    path('category/delete/<str:code>/',views.category_delete,name='category_delete'),
    path('product/list/<str:code>/',views.product_list,name='product_list'),

    path('product/create/',views.create_product,name='create_product'),
    path('product/detail/<str:code>/',views.product_detail,name='product_detail'),
    path('product/list/',views.product_list,name='product_list'),
    path('product/update/<str:code>/',views.update_product,name='update_product'),
    path('product/delete/<str:code>/',views.product_delete,name='product_delete'),

    path('product/image/delete/<str:code>/',views.delete_product_image,name='delete_product_image'),

    path('enter/',views.enter_list,name='enter_list'),
    path('enter/create/',views.create_enter,name='create_enter'),
    path('enter/update/<str:code>/',views.update_enter,name='update_enter'),
    path('enter/<str:code>/',views.enter_list,name='enter_list'),

    path('outs/',views.out_list,name='out_list'),
    path('outs/create/',views.create_out,name='create_out'),
    path('outs/<str:code>',views.out_list,name='out_list'),
    path('outs/update/<str:code>/',views.update_out,name='update_out'),

    path('return/',views.return_list,name='return_list'),
    path('return/create/',views.create_return,name='create_return'),

]
