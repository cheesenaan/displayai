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
from django.urls import include, path
from .views import *
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('terms-of-service/', terms_of_service, name='terms_of_service'),
    path('login/', login, name='login'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('<int:account_id>/logout/', logout, name='logout'),
    path('<int:account_id>/account/', account, name='account'),
    path('<int:account_id>/form/', form, name='form'),
    path('<int:account_id>/reset_password/', reset_password, name='reset_password'),
    path('<int:account_id>/edit_account_name/', edit_account_name, name='edit_account_name'),
    path('<int:account_id>/edit_account_email/', edit_account_email, name='edit_account_email'),
    path('<int:account_id>/confirmation', confirmation, name='confirmation'),
    path('<int:account_id>/reload_resume_and_website', reload_resume_and_website, name='reload_resume_and_website'),
    path('<int:account_id>/reload_resume_and_website_with_job_description', reload_resume_and_website_with_job_description, name='reload_resume_and_website_with_job_description'),
    path('<int:account_id>/build_cover_letter', build_cover_letter, name='build_cover_letter'),
    path('<int:account_id>/subscriptions', subscriptions, name='subscriptions'),
    path('cancel_subscription/<int:account_id>/<str:subscription_id>/', cancel_subscription, name='cancel_subscription'),
    path('payment_successful', payment_successful, name='payment_successful'),
    path('payment_cancelled', payment_cancelled, name='payment_cancelled'),
    path('<str:url_name>/', website, name='website'),
    path('form/CheckUrlNameView/', CheckUrlNameView.as_view(), name='CheckUrlNameView'),
    path('login/CheckAccountNameView/', CheckAccountNameView.as_view(), name='CheckAccountNameView'),
    path('login/CheckAccountEmailView/', CheckAccountEmailView.as_view(), name='CheckAccountEmailView'),
    # Correct URL pattern for terms of service
]



    # path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),

