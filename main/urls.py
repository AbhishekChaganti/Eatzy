from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update-quantity-ajax/', views.update_quantity_ajax, name='update_quantity_ajax'),
    path('cart/', views.cart_drawer, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('my-orders/<int:order_id>/edit/', views.edit_order, name='edit_order'),
    path('my-orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('admin/orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('profile/', views.profile_view, name='profile'),
]