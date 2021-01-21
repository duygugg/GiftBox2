from django.urls import path
from . import views
from .views import FavoriteView, RemoveFavoriteList

urlpatterns = [
    path('',views.home,name="home"),
    path('whatsinside/',views.whatsinside,name="whatsInside"),
    path('givegift/',views.givegift,name="givegift"),
    path('orders/<int:order_id>', views.orderslist, name="orders"),
    path('questions/<str:category_name>',views.questionnaire,name="questions"),
    path('contact/',views.contact,name="contact"),
    path('giftcart-display/',views.giftcart,name="giftcart-display"),
    path('checkout/<int:order_id>', views.checkout, name="checkout"),
    path('cart/', views.cart, name="cart"),
    path('order-detail/', views.orderdetails, name="order-detail"),
    path('friends/', views.friendslist, name="friends-list"),
    path('friend_profile/<int:id>', views.friend_profile, name="friends_profile"),
    path('blog/', views.blog, name="blog"),

    path('favorite/<int:id>', FavoriteView, name="favorite_product"),
    path('remove_favorites/<int:id>', RemoveFavoriteList, name="remove_favorites"),

    path('messages/<int:id>', views.messages, name="messages"),
    path('search_results/', views.search_post, name="search"),
    path('blog', views.blog, name="blog"),
    path('blog/post/create', views.create_post, name="blog-create"),
    path('blog/post/<int:pk_blog>', views.show_post,name="post_details"),
    path('blog/post/<int:pk_blog>/edit', views.edit_post),
    path('blog/post/<int:pk_post>/delete', views.delete_post)
    ]