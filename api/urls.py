from django.urls import path
from . import views
from .views import MyTokenObtainPairView

urlpatterns = [
    path('',views.getRoutes),
    path('create/',views.createUser,name='createUser'),
    path('token/',MyTokenObtainPairView.as_view(),name='token_view'),
    # path('register/',views.registerUser,name='register')
]
