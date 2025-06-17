from django.urls import path
from .views import signup,login,logout,password_reset_request, password_reset_confirm,webhook_listener,register_user


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset/confirm/', password_reset_confirm, name='password_reset_confirm'),
    path('webhook/', webhook_listener, name='webhook-listener'),
    path('register/', register_user, name='register_user'),
]
