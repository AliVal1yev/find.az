from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings





urlpatterns = [
    path('', views.home, name='home'),
    path('details/<int:id>/', views.deails, name='details'),
    path(
        'login/', 
        views.user_login,
        name='login'
    ),
    path(
        'accounts/login/',
        views.user_login,
        name='login'
    ),
    path(
        'sigup/',
        views.user_signup,
        name='signup'
    ),
    path(
        'logout/',
        views.user_logout,
        name='logout'
        ),
    path(
        'cart/',
        views.view_cart,
        name='cart'
    ),
    path(
        'add-to-cart/<int:product_id>/',
         views.add_to_cart,
         name='add_to_cart'
         ),
    path(
        'reset-cart/',
        views.reset_cart,
        name='reset_cart'
        ),
    path(
        'subcategory_products/<int:subcategory_id>/',
        views.subcategory_products, 
        name='subcategory_products'
    ),
     path(
        'toggle-favorite/<int:product_id>/',
        views.toggle_favorite,
        name='toggle_favorite'
        ),
    path(
        'wishlist',
        views.wishlist,
        name='wishlist'
    ),
    path(
        'checkout',
        views.checkout,
        name='checkout'
    ),
    path(
        'order_confirmation/<int:id>/',
        views.order_confirmation,
        name='order_confirmation'
    ),
    path(
        'success', 
        views.success,
        name='success'
    )
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)