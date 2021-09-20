from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from djoser import views

from .views import SendChangeEmailCode, ChangeEmail

from backend.utils.registration import CustomUserCreateView

urlpatterns = [
    # Урлы на получение и рефреш токена
    path('', obtain_jwt_token),
    path('refresh/', refresh_jwt_token),

    # Урлы на регистрацию и активацию юзера
    path('register/', CustomUserCreateView.as_view()),
    path('activate/', views.ActivationView.as_view()),

    # Урлы отправки ключа для смены email и непосредственно смены
    path('send_key/', SendChangeEmailCode.as_view()),
    path('change_email/', ChangeEmail.as_view()),

    # Урлы сброса и подтверждения сброса пароля
    path('reset/', views.PasswordResetView.as_view()),
    path('reset/confirm/', views.PasswordResetConfirmView.as_view()),

]
