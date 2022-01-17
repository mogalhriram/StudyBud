from django.urls import path
from . import views


urlpatterns =[
    path('',views.home,name="home"),
    path('room/<str:pk>', views.room, name='room'),
    path('add-room/', views.add_room, name='add-room'),
    path('edit-room/<str:pk>', views.edit_room, name='edit-room'),
    path('delete-room/<str:pk>', views.delete_room, name='delete-room'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerUser, name='register')
]