from django.urls import path
from . import views

urlpatterns =[
    
    # path('', views.Landing_1, name='Landing_1'),
    path('Register_2/', views.Register_2, name='Register_2'),
    path('Login_3/', views.Login_3, name='Login_3'),
    path('profile/', views.profile_view, name='profile'),

    path('', views.Home_4, name='Home_4'),
    path('Teamates_5/', views.Teamates_5, name='Teamates_5'),
    path('patient_list/', views.patient_list, name='patient_list'),
    path('report/', views.report, name='report'),
    path('Deploy_9/', views.Deploy_9, name='Deploy_9'),
    path('Deploy_10/', views.Deploy_10, name='Deploy_10'),
    path('res/', views.res, name='res'),
    path('database/',views.database,name='database'),
    path('matrix/',views.matrix,name='matrix'),
    path('Logout/', views.Logout, name='Logout'),
]