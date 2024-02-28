"""resume_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from .views import CheckUrlNameView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('checkout/', checkout, name='checkout'),
    path('login', login, name='login'),
    path('logout/', logout, name='logout'),
    path('<int:account_id>/account_details/', account_details, name='account_details'),
    path('<int:account_id>/form/', form, name='form'),
    path('<int:account_id>/confirmation', confirmation, name='confirmation'),
    path('<int:account_id>/reload_resume_and_website', reload_resume_and_website, name='reload_resume_and_website'),
    path('<int:account_id>/reload_resume_and_website_with_job_description', reload_resume_and_website_with_job_description, name='reload_resume_and_website_with_job_description'),
    path('<int:account_id>/build_cover_letter', build_cover_letter, name='build_cover_letter'),
    path('<int:account_id>/account_payments', account_payments, name='account_payments'),
    path('cancel_subscription/<int:account_id>/<str:subscription_id>/', cancel_subscription, name='cancel_subscription'),
    
    # path('payment_basic', payment_basic, name='payment_basic'),
    # path('product_page', product_page, name='product_page'),
    path('payment_successful', payment_successful, name='payment_successful'),
    path('payment_cancelled', payment_cancelled, name='payment_cancelled'),
    # path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
    path('<str:url_name>/', website, name='website'),  
    path('form/CheckUrlNameView/', CheckUrlNameView.as_view(), name='CheckUrlNameView'),
    path('login/check_account_name/', CheckAccountNameView.as_view(), name='CheckAccountNameView'),

]

