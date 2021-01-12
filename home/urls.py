from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('whatsinside/',views.whatsinside,name="whatsInside"),
    path('givegift/',views.givegift,name="givegift"),
    path('orders/',views.orderslist,name="orders"),
    path('questions/',views.questionnaire,name="questions"),
    path('contact/',views.contact,name="contact"),
    path('giftcart-display/',views.giftcart,name="giftcart-display"),
    path('checkout/',views.checkout,name="checkout"),
    path('cart/', views.cart, name="cart"),
    path('order-detail/', views.orderdetails, name="order-detail"),
    path('friends/', views.friendslist, name="friends-list"),
    path('blog/', views.blog, name="blog"),
    path('favorites/', views.favorites, name="favorites"),
    path('messages/', views.messages, name="messages"),
    path('postdetails/', views.postdetails, name="post-details"),
    ]