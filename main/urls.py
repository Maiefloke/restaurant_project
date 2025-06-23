from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/repeat/<int:order_id>/', views.repeat_order, name='repeat_order'),
    path('dish/<int:dish_id>/reviews/', views.review_list, name='review_list'),
    path('dish/<int:dish_id>/add-review/', views.leave_review, name='add_review'),
    path('dish/<int:dish_id>/review/new/', views.leave_review, name='leave_review'),
    #path('admin/reviews/', views.review_moderation, name='review_moderation'),
    #path('admin/reviews/approve/<int:review_id>/', views.approve_review, name='approve_review'),
]