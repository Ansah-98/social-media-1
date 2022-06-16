from django.urls import path
from . import views

urlpatterns =[path('',views.home, name ='home'),
path('room/<str:pk>/',views.room, name ='room'),
path('room_form',views.createroom,name='create-room'),
path('update-room/<str:pk>',views.updateRoom,name= 'update-room'),
path('delete-room/<str:pk>',views.deleteRoom,name='delete-room'),
path('login', views.loginPage,name ='login'),
path('logout',views.signOut,name='logout'),
path('register',views.signUp,name='register'),
path('delete-message/<str:pk>',views.deleteComment, name= 'delete-message'),
path('profile/<str:pk>',views.userProfile,name ='profile'),
path('user-edit/',views.updateUser,name = 'edit-user'),
path('topic-page',views.topicPage,name='topic-page'),
path('activity',views.activities,name="activity")]
