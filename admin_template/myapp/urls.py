# myapp/urls.py

from django.urls import path
from . import views  # Import the views from the current app
from .views import user_data_view,delete_user,payment_list
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('view-info/', views.view_information, name='view-info'),
    path('create-info/', views.InsertInformation, name='create-info'),
    path('information/', user_data_view, name='information'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('update-user/<int:user_id>/', views.update_user, name='update_user'),
     path('payment-details/', views.payment_list, name='payment-details'),
]
