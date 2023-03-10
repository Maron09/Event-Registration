from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('event/<str:pk>/', views.event_page, name='event'),
    path('user/<str:pk>/', views.userProfile, name='user'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('register/', views.register_page, name='register'),
    path('account/', views.account_page, name='my-account'),

    path('confirmation/<str:pk>/', views.register_confirmation, name='confirmation'),
    path('submission/<str:pk>/', views.project_sub, name='submit-project'),
    path('update_submission/<str:pk>/', views.update_sub, name='update-submission'),

]