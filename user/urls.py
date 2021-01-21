from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns =[
    path('signup/',views.register,name="signup"),
    path('login/',auth_views.LoginView.as_view(template_name='user/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home.html'), name='logout'),
    path('profile/', views.Profile, name='myprofile'),
    path('profile/<int:user_id>', views.show_profile),
    path('profile/<int:user_id>/addfriend', views.add_friend, name='add_friend'),
    path('friends/<int:user_id>', views.accept_friend, name='accept_request'),

    path('addresses/', views.addresses, name='myaddresses'),
    path('change_password/', views.change_password, name='change_password'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='user/password_reset_form.html',
             subject_template_name='users/password_reset_subject.txt',
             email_template_name='users/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('favorites/', views.favorite_list, name="favorites"),


]