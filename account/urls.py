from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    # Authentication
    path("create-user/", views.CreateUserAPIView.as_view(), name="create-user"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path(
        "export-subscribers/", views.ExportSubscribersCSVView.as_view(), name="export_subscribers"
    ),
    path(
        "get-subscribers/", views.GetSubscribers.as_view(), name="get_subscribers"
    ),
    path('changePass/', views.ChangePassword.as_view(), name='changePass'),
     path('requestOtp/', views.RequestOtp.as_view(), name='requestOtp'),
    path('verify_otp/', views.VerifyOtp.as_view(), name='verify_otp'),
    path('resetPass/', views.ResetPassword.as_view(), name='resetPass'),
]