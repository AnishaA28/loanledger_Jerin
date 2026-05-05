from django.urls import path
from . import views

urlpatterns = [
    path('loans/', views.loans_list),
    path('loans/<int:pk>/', views.loan_detail),
    path('loans/<int:pk>/repayments/', views.repayments),
]
