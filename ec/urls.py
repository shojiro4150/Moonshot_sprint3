from django.urls import path
from . import views


app_name = 'ec'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('test', views.ConfirmInsuranceView.as_view(), name="confirm_insurance"),
    path('get-insurance/', views.GetInsuranceView.as_view(), name="get_insurance"),
    path('confirm-insurance/', views.ConfirmInsuranceView.as_view(), name="confirm_insurance"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
]
