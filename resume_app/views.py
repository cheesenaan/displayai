import os
import time
import json
import base64
import secrets
import string
from io import BytesIO
from PIL import Image
from django.db import IntegrityError
import qrcode
import stripe
import httplib2
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views import View
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.auth import transport
from google.auth.exceptions import RefreshError
from requests.exceptions import Timeout
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import UserProfile, Account
from .forms import *
import openai
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from decouple import config



prices_dict_test = {
            'basic': 'price_1PGLwPBFOKaICuMNcQUiUkL8',
            'economy': 'price_1PGLxXBFOKaICuMNTWFFLW2Q',
            'business': 'price_1PGLylBFOKaICuMNAW5DbjE5',
            'first_class': 'price_1PGLzzBFOKaICuMNBaMJAJx2',
            'pilot': 'price_1PGM0lBFOKaICuMNLBT2PnVA',
            'pilot2': 'price_1PGM1VBFOKaICuMNuGNqILRd'
}

prices_dict_live = {
            'basic': 'prod_RETKXxCm6fDA6d',
            'economy': 'prod_RETKkDIFDl80Dn',
            'business': 'prod_RETKC5iUFUDmuy',
            'first_class': 'prod_RETKl8TiE4o65o',
            'pilot': 'prod_RETKqBNlUSqtbq',
            'pilot2': 'prod_RETK9ddl2v4BmB'
}
MODE = config('MODE')
prices_dict = ''
if MODE == 'test':
    print("stripe is in test mode")
    prices_dict = prices_dict_test
else:
    print("stripe is in live mode")
    prices_dict = prices_dict_live



action_words_list = ["Streamlined", "Leveraged", "Developed", "Engineered", "Deployed", "Incorporated", 
              "Accelerated", "Devised", "Evaluated", "Invented", "Integrated", "Orchestrated", 
              "Revamped", "Aggregated", "Optimized", "Conceptualized", "Overhauled", "Spearheaded", 
              "Reported", "Implemented", "Generated", "Forged", "Governed", "Experimented", "Centralized", "Deciphered", "Synthesized", "Troubleshot", "Collected"]

def home(request):
    return render(request, "home.html")

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import Account, User, Plan
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.conf import settings

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        user_name = request.POST['name'].lower()
        user_email = request.POST['email']
        user_password = request.POST['password']

        if request.POST['action'] == 'log_in':
            print("logging in user")

            try:
                # Use authenticate to check the username and password
                authenticated_user = authenticate(username=user_name, password=user_password)
                print("authenticated_user is ", authenticated_user)
                
                # If user exists in the database and the password is correct, authenticate them
                account = Account.objects.get(name=user_name, email=user_email)
                if authenticated_user is not None:
                    # User is authenticated, log them in
                    auth_login(request, authenticated_user)
                    # Redirect the user to the appropriate page
                    return redirect('form', account.id)
                else:
                    messages.error(request, 'Invalid login credentials.')
                    login_form = LoginForm()
                    context = {'login_form': login_form}
                    return render(request, 'login.html', context)
            except Account.DoesNotExist:
                messages.error(request, 'Invalid login credentials.')
                login_form = LoginForm()
                context = {'login_form': login_form}
                return render(request, 'login.html', context)
            except Exception as e:
                # Handle any other exceptions that might occur during the authentication process
                print(e)
                messages.error(request, 'An error occurred during login.')
                login_form = LoginForm()
                context = {'login_form': login_form}
                return render(request, 'login.html', context)

        elif request.POST['action'] == 'create_account':
            if Account.objects.filter(name=user_name).exists():
                messages.error(request, 'Username already taken. Please choose another.')
                login_form = LoginForm()
                context = {'login_form': login_form}
                return render(request, 'login.html', context)
            elif Account.objects.filter(email=user_email).exists():
                messages.error(request, 'Email already taken. Please choose another.')
                login_form = LoginForm()
                context = {'login_form': login_form}
                return render(request, 'login.html', context)
            else:
                try:
                    # Hash the password before creating the user
                    hashed_password = make_password(user_password)

                    # Create the user with the hashed password
                    user = User.objects.create_user(user_name, user_email, user_password)  # user_password is already hashed
                    new_account = Account(name=user_name, email=user_email, password=hashed_password, user=user)
                    new_account.save()

                    # Create a free plan and link to the account
                    free_plan = Plan(account=new_account)
                    free_plan.user = user
                    free_plan.save()
                    new_account.user_plan = free_plan
                    new_account.save()

                    print("new account saved")
                    print("id of new account is ", new_account.id)

                    # Authenticate the user after account creation
                    authenticated_user = authenticate(username=user_name, password=user_password)

                    if authenticated_user is not None:
                        auth_login(request, authenticated_user)

                    # Send the welcome email
                    try:
                        subject = 'Welcome to CheeseCV'
                        from_email = settings.EMAIL_HOST_USER
                        recipient_list = [new_account.email]

                        context_email = {
                            'account': new_account,
                        }

                        email_html = render_to_string('new_account_email.html', context_email)
                        send_mail(subject, '', from_email, recipient_list, html_message=email_html, fail_silently=False)

                    except Exception as e:
                        print("this is the error: ", e)
                        print("unable to send create account email")

                    messages.success(request, 'Account created!')
                    return redirect('form', account_id=new_account.id)

                except IntegrityError as e:
                    messages.error(request, 'Username or Email already taken. Please choose another.')
                    login_form = LoginForm()
                    context = {'login_form': login_form}
                    return render(request, 'login.html', context)

    else:
        login_form = LoginForm()
        context = {'login_form': login_form}
        return render(request, 'login.html', context)

@login_required
def logout(request, account_id):
    # Retrieve the account based on the provided account_id
    account = Account.objects.get(id=account_id)
    
    # Log out the currently logged-in user
    auth_logout(request)
    
    return redirect('home')

@login_required
def forgot_password(request):
    if request.method == 'POST':
        # Extracting form data
        name = request.POST.get('name')
        email = request.POST.get('email')

        try:
            account = Account.objects.get(name=name, email=email)

            def generate_reset_code():
                alphabet = string.ascii_letters + string.digits
                reset_code = ''.join(secrets.choice(alphabet) for _ in range(20)) 
                return reset_code

            # Generate a unique reset password code
            reset_code = generate_reset_code()

            # Check if the generated code already exists, generate again if it does
            while Account.objects.filter(reset_password_code=reset_code).exists():
                reset_code = generate_reset_code()

            # Update the account with the new reset password code
            account.reset_password_code = reset_code
            account.save()

            subject = 'Reset Password Instructions'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [account.email]

            # Prepare context with reset password code
            context_email = {
                'account': account,
                'reset_code': reset_code,
            }

            # Render email template
            email_html = render_to_string('forgot_password_email.html', context_email)

            # Send email
            send_mail(subject, '', from_email, recipient_list, html_message=email_html, fail_silently=False)

            messages.success(request, "Email instructions sent to " + email)
        except Account.DoesNotExist:
            messages.error(request, "Invalid credentials.")

        return redirect('forgot_password')

    else:
        return render(request, "forgot_password.html")

@login_required
def reset_password(request, account_id):

    if request.method == 'POST':
        account = Account.objects.get(id=account_id)
        verification_code = request.POST.get('verification_code')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if verification_code == account.reset_password_code and new_password == confirm_new_password:
                account.password = new_password
                account.reset_password_code = ""
                account.save()
                messages.success(request, "Password has been reset. Log In ")
                return redirect('login')
        else:
            if verification_code != account.reset_password_code:
                messages.error(request, "verification code invalid")
            if new_password != confirm_new_password:
                messages.error(request, "Confirm password does not match")
            
        return redirect('reset_password', account_id)

    else:
        account = Account.objects.get(id = account_id)
        context = {
            'account' :account
        }

        return render(request, "reset_password.html", context)

@login_required
def account(request , account_id):
    
    account = Account.objects.get(id=account_id)
    user_plan = Plan.objects.get(account = account)
    user_profile = UserProfile.objects.get(account = account)
    educations = Education.objects.filter(account=account)
    work_experiences = WorkExperience.objects.filter(account=account)
    projects = Project.objects.filter(account=account)

    context = {
        'account' : account ,
        'user_plan': user_plan ,
        'user_profile' : user_profile ,
        'educations' : educations ,
        'remaining' : user_plan.forms_remaining - user_plan.forms_filled_on_current_plan,
        'work_experiences' : work_experiences,
        'projects' : projects

    }

    return render (request, "account.html", context)

@login_required
def edit_account_name(request, account_id):
    account = Account.objects.get(id=account_id)

    password = request.POST.get('password')
    name = request.POST.get('name')

    # Check if the password is correct using hash comparison
    if not check_password(password, account.password):  # Hash comparison
        messages.error(request, "Incorrect password")
        return redirect('account', account_id)  # Return early if password is incorrect

    # Check if the name already exists (excluding the current account)
    if Account.objects.filter(name=name).exclude(id=account_id).exists():
        messages.error(request, f"An account with the name '{name}' already exists.")
    else:
        # Proceed with name change if password is correct and name is not the same
        if name != account.name:
            account.name = name
            account.save()
            messages.success(request, f"Name has been changed to {name}")
        else:
            messages.error(request, f"Already registered with name: {name}")
    
    return redirect('account', account_id)

from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from .models import Account

@login_required
def edit_account_email(request, account_id):
    account = Account.objects.get(id=account_id)

    password = request.POST.get('password')
    email = request.POST.get('email')

    # Check if the password is correct using hash comparison
    if not check_password(password, account.password):  # Hash comparison
        messages.error(request, "Incorrect password")
        return redirect('account', account_id)  # Return early if password is incorrect

    # Check if the email already exists (excluding the current account)
    if Account.objects.filter(email=email).exclude(id=account_id).exists():
        messages.error(request, f"An account with the email '{email}' already exists.")
    else:
        # Proceed with email change if password is correct and email is not the same
        if email != account.email:
            account.email = email
            account.save()
            messages.success(request, f"Email has been changed to {email}")
        else:
            messages.error(request, f"Already registered with email: {email}")
    
    return redirect('account', account_id)


@login_required
def form(request , account_id):
    account = Account.objects.get(id=account_id)
    user_plan = Plan.objects.get(account = account)

    if request.method == 'POST':

        for key, value in request.POST.items():
            print(f"{key}: {value}")

        if UserProfile.objects.filter(account_id=account_id).exists():
            UserProfile.objects.filter(account_id=account_id).delete()
            print(f"Deleted prev UserProfile for account_id {account_id}")

        if Education.objects.filter(account_id=account_id).exists():
            Education.objects.filter(account_id=account_id).delete()
            print(f"Deleted prev Education records for account_id {account_id}")

        if WorkExperience.objects.filter(account_id=account_id).exists():
            WorkExperience.objects.filter(account_id=account_id).delete()
            print(f"Deleted prev WorkExperience records for account_id {account_id}")

        if Project.objects.filter(account_id=account_id).exists():
            Project.objects.filter(account_id=account_id).delete()
            print(f"Deleted prev Project records for account_id {account_id}")
        

        form = UserProfileForm(request.POST, request.FILES)
        user_profile = form.save(commit=False) 
        user_profile.account = account
        user_profile.website_link = settings.REDIRECT_DOMAIN + account.name
        user_profile.website_link = user_profile.website_link.replace("http://", "")
        user_profile.user = account.user
        user_profile.save()


        post_data = request.POST.dict()

        total_education_forms = int(post_data.get("account_education-TOTAL_FORMS", 0))
        print("total number of total_education_forms is : ", total_education_forms)

        for i in range(total_education_forms+1):
            prefix = f"account_education-{i}-"
            institution = post_data.get(prefix + "institution", "").title()
            major = post_data.get(prefix + "major", "").title()
            minor = post_data.get(prefix + "minor", "").title()
            GPA = post_data.get(prefix + "GPA", "")
            start_date = post_data.get(prefix + "start_date", "")
            end_date = post_data.get(prefix + "end_date", start_date)
            current = post_data.get(prefix + "current", "")
            city = post_data.get(prefix + "city", "").title()
            country = post_data.get(prefix + "country", "").title()
            coursework = post_data.get(prefix + "coursework", "")
            degree_type = post_data.get(prefix + "degree_type", "").title()

            if institution and major and GPA and start_date and (end_date or current) and city and coursework and degree_type:
                try:
                    # Create Education instance
                    education = Education.objects.create(
                        account=account,
                        institution=institution,
                        major=major,
                        minor=minor,
                        GPA=GPA,
                        start_date=start_date,
                        end_date=end_date,
                        city=city,
                        country=country,
                        current=current,  # Adjust this if you want to handle the 'current' field from post_data
                        degree_type=degree_type,
                        coursework=coursework
                    )
                    education.account = account
                    print(f"Education instance saved to database: {education}")
                    education.save()
                except Exception as e:
                    print(f"An error occurred with creating or saving education instance: {e}")


        total_work_forms = int(post_data.get("work_experiences-TOTAL_FORMS", 0))
        print("post_data for work", post_data)
        work_counter = 1
        if request.POST["hasWorkExperience"] == "yes":
            for i in range(total_work_forms+1):
                prefix = f"work_experiences-{i}-"
                print("processing", prefix)
                company_name = post_data.get(prefix + "company_name")
                job_title = post_data.get(prefix + "job_title")
                start_date = post_data.get(prefix + "start_date")
                end_date = post_data.get(prefix + "end_date")
                if not end_date:
                    end_date = start_date
                currently_working = post_data.get(prefix + "currently-working", False)
                city = post_data.get(prefix + "city")
                state = post_data.get(prefix + "state")
                description = post_data.get(prefix + "description")
                # bullet1 , bullet2, bullet3 = "bullet1" , "bullet2", "bullet3"

                if company_name and job_title and start_date and (end_date or currently_working) and city and state and description:
                    if work_counter == 1 or account.tier != "free":
                        bullet1 , bullet2, bullet3 = openai_work_experience(company_name ,job_title, description)
                        work_counter = work_counter + 1
                    else:
                        bullet1 , bullet2, bullet3 = "UPGRADE PLAN FOR OPTIMIZED BULLET" , "UPGRADE PLAN FOR OPTIMIZED BULLET", "UPGRADE PLAN FOR OPTIMIZED BULLET"
                    try:
                        print("trying to create work_experience")
                        work_experience = WorkExperience.objects.create(
                            account=account,
                            company_name=company_name,
                            job_title=job_title,
                            start_date=start_date,
                            end_date=end_date,
                            city=city,
                            state=state,
                            currently_working=currently_working,
                            description=description,
                            bullet1=bullet1,
                            bullet2=bullet2,
                            bullet3=bullet3
                        )
                        print("Saving work experience instance to database...")
                        work_experience.save()
                    except Exception as e:
                        print(f"An error occurred with creating or saving work experience instance : {e}")

        else:
            print("there is no work experiences")

        total_project_forms = int(request.POST.get("projects-TOTAL_FORMS", 0))
        if request.POST.get("hasProjectExperience") == "yes":
            for i in range(total_project_forms+1):    
                prefix = f"projects-{i}-"
                print("looping thru ", prefix)
                project_name = request.POST.get(prefix + "project_name")
                description = request.POST.get(prefix + "description")
                project_skills = request.POST.get(prefix + "project_skills")
                

                if project_name and description and project_skills:
                    if work_counter == 1 or account.tier != "free":
                        bullet1, bullet2 = openai_project(project_name, description)
                        work_counter = work_counter + 1
                    else:
                        bullet1, bullet2 = "UPGRADE PLAN FOR OPTIMIZED BULLET" , "UPGRADE PLAN FOR OPTIMIZED BULLET"
                    project = Project.objects.create(
                        account=account,
                        project_name=project_name,
                        description=description,
                        project_skills=project_skills,
                        bullet1=bullet1,
                        bullet2=bullet2,
                    )
                    print("saving ", prefix)
                    project.account = account
                    project.save()
        else:
            print("There are no projects")

        resume_link = create_resume(account)
        if resume_link == "TIME_OUT_ERROR_974":
            messages.error(request, "TIME_OUT_ERROR_974. Your profile was created however your resume could not due to poor internet signal. Please click the Re-build with same data")
            user_profile.save()
            account.user_profile = user_profile
            account.save()
            user_plan.save()
            return redirect('confirmation', account_id=account_id)

        account.set_resume_link(resume_link)
        account.user_profile = user_profile
        account.user_plan = user_plan
        user_profile.resume_link = resume_link
        messages.success(request, "User profile created. Website and resume built successfully !")
        user_profile.save()
        user_plan.forms_filled_on_current_plan = user_plan.forms_filled_on_current_plan + 1
        user_plan.total_forms_filled = user_plan.total_forms_filled + 1
        account.save()
        user_plan.save()
        return redirect('confirmation', account_id=account_id)
    
    if request.method == 'GET':
        form = UserProfileForm(instance=account.user_profile)

        # Set extra forms for Education
        education_extra = 1
        if Education.objects.filter(account_id=account_id).exists():
            education_extra = 0

        EducationFormSet = inlineformset_factory(Account, Education, form=EducationForm, extra=education_extra, can_delete=True)
        education_formset = EducationFormSet(instance=account)

        # Set extra forms for Work Experience
        work_experience_extra = 1
        if WorkExperience.objects.filter(account_id=account_id).exists():
            work_experience_extra = 0

        WorkExperienceFormSet = inlineformset_factory(Account, WorkExperience, form=WorkExperienceForm, extra=work_experience_extra, can_delete=True)
        work_experience_formset = WorkExperienceFormSet(instance=account)

        # Set extra forms for Projects
        project_extra = 1
        if Project.objects.filter(account_id=account_id).exists():
            project_extra = 0

        ProjectFormSet = inlineformset_factory(Account, Project, form=ProjectsForm, extra=project_extra, can_delete=True)
        projects_formset = ProjectFormSet(instance=account)

        required_fields = [
            'first_name', 'last_name', 'phone', 'city', 'state',
            'spoken_languages', 'programming_languages', 'technical_skills', 'leadership'
        ]

        context = {
            'form': form,
            'work_experience_formset': work_experience_formset,
            'projects_formset': projects_formset,
            'education_formset': education_formset,
            'account': account,
            'user_plan': user_plan,
            'remaining': user_plan.forms_remaining - user_plan.forms_filled_on_current_plan,
            'required_fields': required_fields
        }

        return render(request, 'form.html', context)

def website(request, url_name):
    # Retrieve the user profile using url_name
    try:
        account = Account.objects.get(name=url_name)
        user_profile = get_object_or_404(UserProfile, account=account)
        user_plan = Plan.objects.get(account=account)
        education_list = Education.objects.filter(account=account)  # Use filter to get all related education records
        print("education_list", education_list)

        # Pass the user profile to the template
        context = {
            'user_profile': user_profile,
            'account': account,
            'user_plan': user_plan,
            'education_list': education_list,  # Pass the list of education records
        }

        # Render the template with the context
        return render(request, 'website.html', context)
    except Account.DoesNotExist:
        # Log the error or handle it as needed
        print(f"Account with url_name {url_name} does not exist.")
        return render(request, 'home.html', status=404)  # Render a custom 404 page

@login_required
def confirmation(request, account_id):
    account = Account.objects.get(id=account_id)
    user_plan = Plan.objects.get(account = account)

    if request.method == 'POST':
        print(request.POST)

        stripe.api_key = settings.STRIPE_API_KEY

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', 'cashapp', 'us_bank_account'],
            line_items=[
                {
                    'price': prices_dict[request.POST.get('selected_plan')],
                    'quantity': 1,
                },
            ],
            # mode=request.POST.get('mode'),  
            mode = "payment",
            # customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + 'payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + 'payment_cancelled',
            metadata={
                'account_id': account_id,  # Include the account_id as metadata
                'price_dictionary_value' : request.POST.get('selected_plan'),
                'mode': "payment",
            },
        )
        print(checkout_session)
        print()
        print("stripe.checkout.Session.retrieve is ")
        print(stripe.checkout.Session.retrieve(checkout_session.id))
        return redirect(checkout_session.url, code=303)

    if request.method == 'GET':
        # Construct the URL
        url = f"{settings.REDIRECT_DOMAIN}/{account.name}"

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image to BytesIO
        qr_code_buffer = BytesIO()
        qr_img.save(qr_code_buffer)
        qr_code_buffer.seek(0)

        # Encode the image as base64
        qr_code_base64 = base64.b64encode(qr_code_buffer.getvalue()).decode("utf-8")

        # Create context for rendering
        context = {
            'account': account,
            'user_plan': user_plan,
            'user_profile': account.user_profile,
            'remaining': user_plan.forms_remaining - user_plan.forms_filled_on_current_plan,
            'qr_code_image': qr_code_base64,
            'redirect_domain': settings.REDIRECT_DOMAIN,
        }

        # Render the template
        template = loader.get_template('confirmation.html')
        return HttpResponse(template.render(context, request))


        

    
    # Render the template
        template = loader.get_template('confirmation.html')
        return HttpResponse(template.render(context, request))

@login_required
def payment_successful(request):
    if request.method == 'GET':
        stripe.api_key = settings.STRIPE_API_KEY
        print("inside payment_successful")

        session_id = request.GET.get('session_id', None)
        session = stripe.checkout.Session.retrieve(session_id)
        mode = session.get('metadata', {}).get('mode')

        print("session_id", session_id)
        print("session", session)
        print("mode", mode)


        if mode == 'subscription':

            session_id = request.GET.get('session_id', None)
            session = stripe.checkout.Session.retrieve(session_id)
            customer = stripe.Customer.retrieve(session.customer)
            account_id = session.get('metadata', {}).get('account_id')
            price_dictionary_value = session.get('metadata', {}).get('price_dictionary_value')
            account = Account.objects.get(id=account_id)
            user_plan = Plan.objects.get(account=account)
            userprofile = UserProfile.objects.get(account=account)

            stripe_payment_data = stripe.checkout.Session.retrieve(session_id)
            subscription_value = stripe_payment_data["subscription"]

            # Check if a Payment instance already exists
            payment_instance, created = Payment.objects.get_or_create(
                account=account,
                subscription_id=subscription_value
            )

            if created:
                # Payment instance already exists, update information
                print("updating other fields in payment_instance")
                payment_instance.update_subscription_info()
                payment_instance.mode = 'subscription'
                payment_instance.save()
                account.tier = price_dictionary_value
                user_plan.type = price_dictionary_value
                user_plan.forms_filled_on_current_plan = 0
                user_plan.set_subscription_ids(subscription_value)

            account.user_payment = payment_instance
            account.save()
            user_plan.save()
            userprofile.save()

            context = {
                'account': account,
                'user_profile': userprofile,
                'user_plan': user_plan,
                'remaining': user_plan.forms_remaining - user_plan.forms_filled_on_current_plan
            }

            payment_instance = Payment.objects.get(account=account, subscription_id=subscription_value)

            if payment_instance:
                subject = 'CheeseCV Order Confirmation - ' + str(account.tier)
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [account.email]

                # Prepare context with payment details
                context_email = {
                    'account': account,
                    'payment_instance' : payment_instance
                }

                # Render email template
                email_html = render_to_string('order_confirmation_subscription_email.html', context_email)

                # Send email
                send_mail(subject, '', from_email, recipient_list, html_message=email_html, fail_silently=False)

        elif mode == 'payment': 

            session_id = request.GET.get('session_id', None)
            session = stripe.checkout.Session.retrieve(session_id)
            account_id = session.get('metadata', {}).get('account_id')
            price_dictionary_value = session.get('metadata', {}).get('price_dictionary_value')
            account = Account.objects.get(id=account_id)
            user_plan = Plan.objects.get(account=account)
            userprofile = UserProfile.objects.get(account=account)

            stripe_payment_data = stripe.checkout.Session.retrieve(session_id)

            session = stripe.checkout.Session.retrieve(session_id)
            # Extract relevant information
            payment_intent_id = session.payment_intent
            amount = session.amount_total / 100  # Amount is in cents, convert to dollars
            currency = session.currency
            payment_status = session.payment_status
            date_of_purchase = datetime.fromtimestamp(session.created)

            mode = session.mode

            # Extract customer name and email
            customer_name = session.customer_details.name
            customer_email = session.customer_details.email


            payment_instance, created = Payment.objects.get_or_create(
                account=account,
                subscription_id=session.id
            )

            print("payment_instance is ", payment_instance)
            print("created is ", created)

            if created:
                payment_instance.save()
                account.tier = price_dictionary_value
                user_plan.type = price_dictionary_value
                user_plan.forms_filled_on_current_plan = 0
                user_plan.set_subscription_ids(session.id)
                payment_instance.subscription_id = session.id
                payment_instance.start_date = datetime.fromtimestamp(session.created)
                payment_instance.customer_email = customer_email
                payment_instance.customer_name = customer_name
                payment_instance.product_price = amount
                payment_instance.product_name = price_dictionary_value + " one time plan"
                payment_instance.save()
                account.user_payment = payment_instance
                account.save()
                user_plan.save()
                userprofile.save()

            context = {
                'account': account,
                'user_profile': userprofile,
                'user_plan': user_plan,
                'remaining': user_plan.forms_remaining - user_plan.forms_filled_on_current_plan
            }

            payment_instance = Payment.objects.get(account=account, subscription_id=session.id)

            if created:
                subject = 'CheeseCV Order Confirmation - ' + str(account.tier)
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [account.email]

                # Prepare context with payment details
                context_email = {
                    'account': account,
                    'payment_instance' : payment_instance
                }

                # Render email template
                email_html = render_to_string('order_confirmation_onetime_email.html', context_email)

                # Send email
                send_mail(subject, '', from_email, recipient_list, html_message=email_html, fail_silently=False)


        return render(request, 'payment_successful.html', context)
    else:
        # Redirect to prevent form resubmission
        messages.error(request, "You cannot reload this page.")
        return redirect('home')  # Redirect to your home page or any other appropriate

@login_required
def payment_cancelled(request):
    print("payment_cancelled")
    stripe.api_key = settings.STRIPE_API_KEY
    
    return render(request, 'payment_cancelled.html')

@login_required
def subscriptions(request, account_id):
    account = Account.objects.get(id=account_id)
    user_plan = Plan.objects.get(account = account)
    userprofile = UserProfile.objects.get(account = account)

    payment_instances = Payment.objects.filter(account=account)
    subscription_exists = any(payment_instance.mode == 'subscription' for payment_instance in payment_instances)


    # if request.method == 'POST':

    if request.method == 'GET':
        context = {
                    'account' : account,
                    'user_profile': userprofile,
                    'user_plan' : user_plan,
                    'payment_instances' : payment_instances ,
                    'remaining' : user_plan.forms_remaining - user_plan.forms_filled_on_current_plan,
                    'subscription_exists': subscription_exists,
        }

        return render(request, 'subscriptions.html' , context)

@login_required
def cancel_subscription(request, account_id, subscription_id):
    stripe.api_key = settings.STRIPE_API_KEY

    try:
        account = Account.objects.get(id=account_id)
        payment_instance = Payment.objects.filter(account=account, subscription_id=subscription_id).get()
        # if (account.password != password):
        #     messages.error(request,"error : incorrect password")
        #     return redirect('subscriptions', account_id=account_id)
    except Payment.DoesNotExist:
        messages.error(request,"error : Payment instance not found")
        return redirect('subscriptions', account_id=account_id)

    stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=True,
    )
    payment_instance = Payment.objects.filter(account=account, subscription_id=subscription_id).get()

    if payment_instance.subscription_status == "cancelled":
        messages.error(
            request,
            f"Error: Subscription {subscription_id} for {payment_instance.product_name} "
            f"with price {payment_instance.product_price} has already been cancelled."
        )

    else:
        payment_instance.update_subscription_info()
        payment_instance.subscription_status = "cancelled"
        payment_instance.save()

        # subject = 'CheeseCV' + str(account.tier) + 'Cancelled'
        # from_email = settings.EMAIL_HOST_USER
        # recipient_list = [account.user_profile.email]

        # # Prepare context with payment details
        # context_email = {
        #     'account': account,
        #     'payment_instance' : payment_instance
        # }

        # # Render email template
        # email_html = render_to_string('cancel_confirmation_email.html', context_email)

        # # Send email
        # send_mail(subject, '', from_email, recipient_list, html_message=email_html, fail_silently=False)

        messages.success(request, f"Your subscription has been cancelled and will no longer be charged. Plan is still active until {payment_instance.end_date}.")
        return redirect('subscriptions', account_id=account_id)

    return redirect('subscriptions', account_id=account_id)

@login_required
def reload_resume_and_website_with_job_description(request: HttpRequest, account_id: int):
    try:
        account = Account.objects.get(id=account_id)
        user_plan = Plan.objects.get(account=account)
        user_profile = UserProfile.objects.get(account=account)
        job_description = request.GET.get('JOB_DESCRIPTION', '').strip()

        work_counter = 1

        # Use WorkExperience.objects.filter for work experiences
        for i, work_experience in enumerate(WorkExperience.objects.filter(account_id=account_id), start=1):
            if work_counter == 1 or account.tier != "free":
                work_experience.bullet1, work_experience.bullet2, work_experience.bullet3 = openai_work_experience(
                    work_experience.company_name, work_experience.job_title, work_experience.description)
                work_counter += 1
            else:
                work_experience.bullet1, work_experience.bullet2, work_experience.bullet3 = (
                    "UPGRADE PLAN FOR OPTIMIZED BULLET", 
                    "UPGRADE PLAN FOR OPTIMIZED BULLET", 
                    "UPGRADE PLAN FOR OPTIMIZED BULLET"
                )
            work_experience.save()

        # Use Project.objects.filter for projects
        for i, project in enumerate(Project.objects.filter(account_id=account_id), start=1):
            if work_counter == 1 or account.tier != "free":
                project.bullet1, project.bullet2 = openai_project(project.project_name, project.description)
                work_counter += 1
            else:
                project.bullet1, project.bullet2 = (
                    "UPGRADE PLAN FOR OPTIMIZED BULLET", 
                    "UPGRADE PLAN FOR OPTIMIZED BULLET"
                )
            project.save()

        new_resume_link = create_resume(account)
        if new_resume_link == "TIME_OUT_ERROR_974":
            messages.error(request, "TIME_OUT_ERROR_974. Could not build personal website and tailored resume due to poor internet. Please try again")
            return redirect('confirmation', account_id=account_id)

        user_profile.resume_link = new_resume_link
        account.set_resume_link(new_resume_link)
        print(user_profile.resume_link)

        user_profile.save()
        user_plan.forms_filled_on_current_plan += 1
        user_plan.total_forms_filled += 1
        account.save()
        user_plan.save()

        messages.success(request, "Personal website and tailored resume created")

    except Timeout:
        messages.error(request, "Timeout error. Your internet connection is slow. Please click 'Build job description tailored resume' again.")
        return redirect('confirmation', account_id=account_id)
    except RefreshError as e:
        messages.error(request, "Timeout error. Your internet connection is slow. Please click 'Build job description tailored resume' again.")
        return redirect('confirmation', account_id=account_id)
    except Exception as e:
        messages.error(request, f"Unknown error: {str(e)}. Please click 'Build job description tailored resume' again.")
        return redirect('confirmation', account_id=account_id)

    return redirect('confirmation', account_id=account_id)

@login_required
def reload_resume_and_website(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        user_plan = Plan.objects.get(account=account)
        user_profile = UserProfile.objects.get(account=account)

        work_counter = 1
        # Use WorkExperience.objects.filter for filtering work experiences by account_id
        for i, work_experience in enumerate(WorkExperience.objects.filter(account_id=account_id), start=1):
            if work_counter == 1 or account.tier != "free":
                work_experience.bullet1, work_experience.bullet2, work_experience.bullet3 = openai_work_experience(work_experience.company_name, work_experience.job_title, work_experience.description)
                work_counter += 1
            else:
                work_experience.bullet1, work_experience.bullet2, work_experience.bullet3 = (
                    "UPGRADE PLAN FOR OPTIMIZED BULLET", 
                    "UPGRADE PLAN FOR OPTIMIZED BULLET", 
                    "UPGRADE PLAN FOR OPTIMIZED BULLET"
                )
            work_experience.save()

        # Use Project.objects.filter for filtering projects by account_id
        for i, project in enumerate(Project.objects.filter(account_id=account_id), start=1):
            if work_counter == 1 or account.tier != "free":
                project.bullet1, project.bullet2 = openai_project(project.project_name, project.description)
                work_counter += 1
            else:
                project.bullet1, project.bullet2 = "UPGRADE PLAN FOR OPTIMIZED BULLET", "UPGRADE PLAN FOR OPTIMIZED BULLET"
            project.save()

        new_resume_link = create_resume(account)
        if new_resume_link == "TIME_OUT_ERROR_974":
            messages.error(request, "TIME_OUT_ERROR_974. Could not re-build personal website and resume due to poor internet. Please try again")
            return redirect('confirmation', account_id=account_id)

        user_profile.resume_link = new_resume_link
        account.set_resume_link(new_resume_link)
        print(user_profile.resume_link)

        user_profile.save()
        user_plan.forms_filled_on_current_plan += 1
        user_plan.total_forms_filled += 1
        account.save()
        user_plan.save()

        messages.success(request, "Using the same profile data, resume and personal website have been re-built")

    except Timeout:
        messages.error(request, "Timeout error. Your internet connection is slow. Please click 'Re-Build with same data' again.")
    except Exception as e:
        messages.error(request, f"Unknown error: {str(e)}. Please click 'Re-Build with same data' again")

    return redirect('confirmation', account_id=account_id)

def create_resume(account):

    try:

        user_profile = get_object_or_404(UserProfile, account=account)


        # Dictionary to store the placeholder replacements
        placeholder_replacements = {
                'name': f"{user_profile.first_name.upper()} {user_profile.last_name.upper()}",
                'email': account.email,
                'phone': user_profile.phone,
                'city': user_profile.city,
                'state': user_profile.state.upper(),
                'linkedin_link': user_profile.linkedin_link,
                'resume_link': user_profile.resume_link,
                'github_link': user_profile.github_link,
                'spoken_languages': user_profile.spoken_languages,
                'languages': user_profile.programming_languages,
                'technical_skills': user_profile.technical_skills,
                'leadership': user_profile.leadership,
                'website_link': user_profile.website_link,
            }
        
         # Retrieve all education records associated with the account

        # Retrieve and sort education records: 'current' records first, then by latest end_date
        education_records = Education.objects.filter(account=account).order_by('-current', '-end_date')

        if education_records:
            for i, education in enumerate(education_records, start=1):
                print("Updating education placeholder for education ", i, education)
                placeholder_replacements.update({
                    f'university {i}': education.institution,
                    f'university start date {i}': education.start_date.strftime('%b %Y'),
                    f'university end date {i}': "Present" if education.current else education.end_date.strftime('%b %Y'),
                    f'degree_type {i}': education.degree_type,
                    f'Major {i}': f"{education.major} and Minor in {education.minor}" if education.minor else education.major,
                    f'coursework {i}': education.coursework
                    # f'location {i}': f"{education.city}, {education.country}"
                })


        # Retrieve and sort work records: 'currently_working' records first, then by latest end_date
        work_records = WorkExperience.objects.filter(account=account).order_by('-currently_working', '-end_date')

        if work_records:
            for i, work_experience in enumerate(work_records, start=1):
                placeholder_replacements.update({
                    f'experience{i}': work_experience.company_name.title(),
                    f'title{i}': work_experience.job_title.title(),
                    f'experience{i} start date': work_experience.start_date.strftime('%b %Y'),
                    f'experience{i} end date': "Present" if work_experience.currently_working else work_experience.end_date.strftime('%b %Y'),
                    f'experience{i} location': f"{work_experience.city.strip().title()}, {work_experience.state.strip().upper()}",
                    f'experience{i} bullet1': work_experience.bullet1,
                    f'experience{i} bullet2': work_experience.bullet2,
                    f'experience{i} bullet3': work_experience.bullet3,
                })



        project_records = Project.objects.filter(account=account)
        if project_records:
            for i, project in enumerate(project_records, start=1):
                placeholder_replacements.update({
                    f'project{i}': project.project_name.title(),
                    f'skills{i}': project.project_skills,
                    f'project{i} bullet1': project.bullet1,
                    f'project{i} bullet2': project.bullet2,
                })

        # Path to your service account credentials JSON file
        SERVICE_ACCOUNT_FILE = settings.SERVICE_ACCOUNT_FILE

        # ID of the Google Doc you want to modify
        DOCUMENT_ID = '1PVKqAkOTjdorBmlJOIGHYhIjYuBPxuPZzKeN4TUQZNE'
        # Folder ID where the copy will be placed
        FOLDER_ID = '1aGcF78a65Nus-K9kCv8P7NzMBSZjJnNY'

        # Authenticate and create the Google Drive API service
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive'])
        service = build('drive', 'v3', credentials=credentials)

        # Create a copy of the document
        copy_metadata = {
            'name': user_profile.first_name + ' - Resume',
            'parents': [FOLDER_ID]
        }
        copy_response = service.files().copy(fileId=DOCUMENT_ID,  body=copy_metadata).execute()
        copy_id = copy_response['id']

        print(f"Copy created with ID: {copy_id}")

        DOCUMENT_ID = str(copy_id)

        # Authenticate and create the Google Docs API service
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/documents'])
        service = build('docs', 'v1', credentials=credentials)

        # Get the content of the Google Doc
        doc = service.documents().get(documentId=DOCUMENT_ID).execute()

        # Process each content element and replace placeholders
        for content in doc['body']['content']:
            if 'paragraph' in content:
                elements = content['paragraph']['elements']
                for element in elements:
                    if 'textRun' in element:
                        text_run = element['textRun']
                        if 'content' in text_run:
                            content_text = text_run['content']
                            for placeholder, replacement in placeholder_replacements.items():
                                if placeholder in content_text:
                                    content_text = content_text.replace(placeholder, replacement)
                                    text_run['content'] = content_text

        # Create the requests list for batch updating
        requests = []
        for placeholder, replacement in placeholder_replacements.items():
            requests.append({
                'replaceAllText': {
                    'containsText': {
                        'text': '{{' + placeholder + '}}',
                        'matchCase': False
                    },
                    'replaceText': replacement
                }
            })

        # Execute the batch update requests
        result = service.documents().batchUpdate(documentId=DOCUMENT_ID,  body={'requests': requests}).execute()

        print('Placeholders replaced successfully in the Google Doc')

        # Get the content of the Google Doc
        doc = service.documents().get(documentId=DOCUMENT_ID).execute()
        body_content = doc['body']['content']

        # Iterate over the paragraphs in reverse order
        requests = []
        for i in range(len(body_content) - 1, -1, -1):
            paragraph = body_content[i]
            if 'paragraph' in paragraph:
                elements = paragraph['paragraph']['elements']
                contains_template_text = any('{{' in element['textRun']['content'] and '}}' in element['textRun']['content'] for element in elements)
                if contains_template_text:
                    # Remove the paragraph if it contains {{}} template text
                    requests.append({
                        'deleteContentRange': {
                            'range': {
                                'startIndex': paragraph['startIndex'],
                                'endIndex': paragraph['endIndex']
                            }
                        }
                    })

        # Execute the batch update requests to remove paragraphs with unfilled {{}} template text
        if requests:
            service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
            print("Lines with unfilled {{}} template text removed successfully!")

        def remove_blank_lines(DOCUMENT_ID):
            # Get the content of the Google Doc
            doc = service.documents().get(documentId=DOCUMENT_ID).execute()
            body = doc['body']

            # Lists to store delete requests
            delete_start_indices = []
            delete_end_indices = []
            delete_rows = []

            # Iterate through all elements in reverse order
            total_elements = len(body['content'])
            i = total_elements - 1
            while i >= 0:
                element = body['content'][i]

                # Check if the element is a paragraph
                if 'paragraph' in element:
                    paragraph = element['paragraph']
                    text = paragraph['elements'][0]['textRun']['content'].strip()

                    # Check if the current element is empty and the previous element exists and is also empty
                    if i != total_elements - 1 and len(text) == 0 and 'paragraph' in body['content'][i - 1] and \
                            body['content'][i - 1]['paragraph']['elements'][0]['textRun']['content'].strip() == '':
                        # Store the character index where the row starts
                        start_index = paragraph['elements'][0]['startIndex']
                        end_index = paragraph['elements'][0]['endIndex']
                        delete_start_indices.append(start_index)
                        delete_end_indices.append(end_index)
                        delete_rows.append(i)

                i -= 1

            # Create a list of delete requests based on the stored start and end indices
            requests = [
                {
                    'deleteContentRange': {
                        'range': {
                            'startIndex': start_index,
                            'endIndex': end_index,
                        }
                    }
                }
                for start_index, end_index in zip(delete_start_indices, delete_end_indices)
            ]

            # Execute the batch update with delete requests
            result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
            return
        remove_blank_lines(DOCUMENT_ID)

        # Get the link of the Google Doc
        resume_link = f"https://docs.google.com/document/d/{DOCUMENT_ID}"
        print("Link to the Google Doc:", resume_link)
        return resume_link
    except RefreshError as e:
        print(f"RefreshError: {e}")
        return "TIME_OUT_ERROR_974"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "TIME_OUT_ERROR_974"

def create_cover_letter_google_doc(data):

    try:
        # Path to your service account credentials JSON file
        SERVICE_ACCOUNT_FILE = settings.SERVICE_ACCOUNT_FILE
        
        FOLDER_ID = '1aGcF78a65Nus-K9kCv8P7NzMBSZjJnNY'

        # Authenticate and create the Google Drive API service
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive.file'])
        drive_service = build('drive', 'v3', credentials=credentials)

        # Create a new Google Doc
        doc_service = build('docs', 'v1', credentials=credentials)
        document = doc_service.documents().create().execute()
        document_id = document['documentId']

        # Insert text into the Google Doc
        requests = [
            {
                'insertText': {
                    'text': data,
                    'location': {
                        'index': 1,
                    },
                },
            },
        ]
        doc_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

        # Share the Google Doc
        drive_service.permissions().create(
            fileId=document_id,
            body={
                'type': 'anyone',
                'role': 'writer',
            }
        ).execute()

        # Get the link to the shared Google Doc
        document_url = f'https://docs.google.com/document/d/{document_id}/edit'

        return document_url
    except RefreshError as e:
        print(f"RefreshError: {e}")
        return "TIME_OUT_ERROR_974"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "TIME_OUT_ERROR_974"

def build_cover_letter(request: HttpRequest, account_id: int):

    try:
        account = Account.objects.get(id=account_id)
        user_plan = Plan.objects.get(account = account)
        user_profile = UserProfile.objects.get(account = account)
        job_description = request.GET.get('JOB_DESCRIPTION', '').strip()

        education = Education.objects.filter(account_id=account_id)
        work_experiences = WorkExperience.objects.filter(account_id=account_id)
        projects = Project.objects.filter(account_id=account_id)

        openai.api_key = settings.OPENAI_API_KEY
        current_date = time.strftime("%Y-%m-%d")

        prompt = f"""
You are tasked with writing a professional, concise, and personalized cover letter based on the details provided below. 
Please make sure the cover letter is well-structured and tailored to the job description, avoiding any placeholders.

Personal Information:
- Name: {user_profile.first_name} {user_profile.last_name}
- Phone: {user_profile.phone}
- Email: {account.email}
- Address: {user_profile.city}, {user_profile.state}
- Website: {user_profile.website_link}

Education:
{", ".join([
    f"{edu.institution}, {edu.degree_type} in {edu.major} {'(Minor in ' + edu.minor + ')' if edu.minor else ''} - GPA: {edu.GPA if edu.GPA else 'N/A'}"
    f" ({edu.start_date.strftime('%Y')} - {edu.end_date.strftime('%Y') if not edu.current else 'Present'})"
    f" Location: {edu.city}, {edu.country} - Coursework: {edu.coursework}" 
    for edu in education
])}

Skills:
- Programming Languages: {user_profile.programming_languages}
- Technical Skills: {user_profile.technical_skills}

Work Experiences:
{", ".join([f"{exp.company_name}, {exp.job_title} ({exp.start_date} - {exp.end_date}): {exp.description}" for exp in work_experiences])}

Projects:
{", ".join([f"{proj.project_name}: {proj.description}" for proj in projects])}

Job Description:
{job_description}

"""


        # Make a request to OpenAI API using the chat/completions endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=900,  # Adjust as needed
            temperature=0.7  # Adjust as needed
        )

        # Extract and print the assistant's reply
        reply = response['choices'][0]['message']['content']
        print(reply)

        cover_letter_link = create_cover_letter_google_doc(reply)
        if cover_letter_link == "TIME_OUT_ERROR_974":
            messages.error(request, "TIME_OUT_ERROR_974. Could not build cover letter due to poor internet. Please try again")
            return redirect('confirmation', account_id=account_id)

        user_profile.resume_link = cover_letter_link
        account.set_resume_link(cover_letter_link)
        print(user_profile.resume_link)

        user_profile.save()
        user_plan.forms_filled_on_current_plan = user_plan.forms_filled_on_current_plan + 1
        user_plan.total_forms_filled = user_plan.total_forms_filled + 1
        user_plan.total_cover_letters = user_plan.total_cover_letters + 1
        
        account.save()
        user_plan.save()

        messages.success(request, "cover letter built successfully")
    except Timeout:
        messages.error(request, "Timeout error. Your internet connection is slow. Please try again.")
    except Exception as e:
        messages.error(request, "Unkown error. Please try again.")

    return redirect('confirmation', account_id=account_id)

def openai_work_experience_with_job_description(JOB_DESCRIPTION, EXPERIENCE ,TITLE, DESCRIPTION ):
    openai.api_key = settings.OPENAI_API_KEY

    prompt = f"""
    using job description give me exactly 3 very short, concise, and numerically quantified one sentence resume points for experience
    job description : {JOB_DESCRIPTION}
    company : {EXPERIENCE}
    position : {TITLE}
    description : {DESCRIPTION}
    """

    # Make a request to OpenAI API using the chat/completions endpoint
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=80,  # Adjust as needed
        temperature=0.7  # Adjust as needed
    )

    # Extract and print the assistant's reply
    reply = response['choices'][0]['message']['content']

    # Clean the text and extract bullet points
    lines = [line.strip().rstrip('.') for line in reply.split('\n') if line.strip()]

    # Assign each bullet point to a variable
    one = lines[0].split('. ')[1]
    two = lines[1].split('. ')[1]
    three = lines[2].split('. ')[1]

    return one, two, three

def openai_project_with_job_description(JOB_DESCRIPTION, PROJECT, DESCRIPTION):
    openai.api_key = settings.OPENAI_API_KEY

    prompt = f"""
    using job description give me exactly 2 very short, concise, and numerically quantified one sentence resume points
    job description : {JOB_DESCRIPTION}
    project : {PROJECT}
    description : {DESCRIPTION}
    """

    # Make a request to OpenAI API using the chat/completions endpoint
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,  # Adjust as needed
        temperature=0.7  # Adjust as needed
    )

    # Extract and print the assistant's reply
    reply = response['choices'][0]['message']['content']
    print(reply)

    # Clean the text and extract bullet points
    lines = [line.strip().rstrip('.') for line in reply.split('\n') if line.strip()]
    lines = [line.replace('-', ' ') for line in lines]
    print(lines)

    # Assign each bullet point to a variable, if available
    one = lines[0].split('. ')[1]
    two = lines[1].split('. ')[1]

    return one, two

def openai_work_experience(EXPERIENCE ,TITLE, DESCRIPTION):
    
    openai.api_key = settings.OPENAI_API_KEY

    prompt = f"""
    give me exactly 3 very short, concise, and numerically quantified one sentence resume points for
    company : {EXPERIENCE}
    position : {TITLE}
    description : {DESCRIPTION}
    """

    # Make a request to OpenAI API using the chat/completions endpoint
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=80,  # Adjust as needed
        temperature=0.7  # Adjust as needed
    )

    # Extract and print the assistant's reply
    reply = response['choices'][0]['message']['content']

    # Clean the text and extract bullet points
    lines = [line.strip().rstrip('.') for line in reply.split('\n') if line.strip()]

    # Assign each bullet point to a variable
    one = lines[0].split('. ')[1]
    two = lines[1].split('. ')[1]
    three = lines[2].split('. ')[1]

    print(one, two, three)
    print()

    return one, two, three

def openai_project(PROJECT, DESCRIPTION):

    openai.api_key = settings.OPENAI_API_KEY

    prompt = f"""
    give me exactly 2 very short, concise, and numerically quantified one sentence resume points
    project : {PROJECT}
    description : {DESCRIPTION}
    """

    # Make a request to OpenAI API using the chat/completions endpoint
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,  # Adjust as needed
        temperature=0.7  # Adjust as needed
    )

    # Extract and print the assistant's reply
    reply = response['choices'][0]['message']['content']

    # Clean the text and extract bullet points
    lines = [line.strip().rstrip('.') for line in reply.split('\n') if line.strip()]
    print(lines)

    # Assign each bullet point to a variable
    one = lines[0].split('. ')[1]
    two = lines[1].split('. ')[1]

    return one, two

class CheckUrlNameView(View):
    def get(self, request, *args, **kwargs):
        url_name = request.GET.get('url_name', None)
        account_id = request.GET.get('account_id', None)

        # Check if the url_name is taken for the current account
        is_taken_current_account = UserProfile.objects.filter(url_name=url_name, account_id=account_id).exists()

        # Check if the url_name is taken in any other account except the current account
        is_taken = UserProfile.objects.exclude(account_id=account_id).filter(url_name=url_name).exists()

        data = {
            'is_taken_current_account': is_taken_current_account,
            'is_taken': is_taken,
        }
        return JsonResponse(data)


class CheckAccountNameView(View):
    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', '').lower()  # Convert input to lowercase
        # Check if the account name exists in lowercase
        data = {'is_taken': Account.objects.filter(name__iexact=name).exists()}
        return JsonResponse(data)


class CheckAccountEmailView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', None)
        data = {'is_taken': User.objects.filter(email=email).exists()}
        return JsonResponse(data)

def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_API_KEY

    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print("inside stripe_webhook")
    try:
        print("event 1")
        event = stripe.Webhook.construct_event(
            payload, signature_header, 'whsec_225411bfa0199497eabcad4a58cfc6cd5007421edbc018658d5ab000eeeeccdc'
        )
    except ValueError as e:
        print("event 2")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("event 3")
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        print("checkout.session.completed !!!!")

        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
    
    return HttpResponse(status=200)



def terms_of_service(request):
    print("inside terms_of_service")
    return render(request, 'terms_of_service.html')
