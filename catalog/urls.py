from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

    path('profile/', views.profile, name='profile'),
    path('requests/', views.my_requests, name='my_requests'),
    path('requests/create/', views.create_request, name='create_request'),
    path('requests/<uuid:pk>/delete/', views.delete_request, name='delete_request'),
    path('requests/<uuid:pk>/', views.request_detail, name='request-detail'),

    path('admin/requests/', views.admin_all_requests, name='admin-all-requests'),
    path('admin/requests/<uuid:pk>/take-to-work/', views.admin_take_to_work, name='admin-take-to-work'),
    path('admin/requests/<uuid:pk>/complete/', views.admin_complete, name='admin-complete'),

    path('admin/categories/', views.admin_category_list, name='admin-category-list'),
    path('admin/categories/create/', views.admin_category_create, name='admin-category-create'),
    path('admin/categories/<int:pk>/delete/', views.admin_category_delete, name='admin-category-delete'),
]
