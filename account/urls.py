from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.AccountRegister.as_view()),
    path('login/', views.AccountLogin.as_view()),
    path('my-account/', views.MyAccount.as_view()),
    path('my-account-rud/<int:pk>/', views.MyAccountRUD.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


