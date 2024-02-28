import os
import datetime
from io import BytesIO
import time
from unittest import loader
from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse
from google.oauth2.service_account import Credentials
import openai
import httplib2
from django.views import View
from .models import UserProfile, Account
from .forms import *
from googleapiclient.discovery import build
from google.oauth2 import service_account
import qrcode
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe
from django.shortcuts import render
import json
from django.http import HttpResponse
import time
from django.shortcuts import render
import stripe
from django.http import JsonResponse
from googleapiclient.discovery import build
from google.oauth2 import service_account
import google.auth
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
from django.contrib import messages
from django.shortcuts import redirect
from requests.exceptions import Timeout
import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.template import loader
import base64
from django.shortcuts import render, redirect
from django.contrib import messages


prices_dict = {
            'basic': 'price_1OibgCBFOKaICuMNShWHaBHo',
            'economy': 'price_1OkLejBFOKaICuMNZEKWocxq',
            'business': 'price_1OkLHsBFOKaICuMNh2kNKtXF',
            'first_class': 'price_1OkLJfBFOKaICuMNDON9NIkm',
            'pilot': 'price_1OkLKeBFOKaICuMNSAiwrsVw',
            'pilot2': 'price_1OkLLVBFOKaICuMN557sysPE'
}


def checkout(request):
    return render(request, "checkout.html")

def home(request):
    return render(request, "home.html")

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if request.POST['action'] == 'log_in':
                print("logging in user")

                try:
                    account = Account.objects.get(name=request.POST['name'], password=request.POST['password'])
                    return redirect('form', account.id)
                except Account.DoesNotExist:
                    messages.error(request, 'Invalid login credentials.')

        elif request.POST['action'] == 'create_account':
                if Account.objects.filter(name=request.POST['name']).exists():
                    messages.error(request, 'Username already taken. Please choose another.')
                else:
                    new_account = Account()
                    new_account.name = request.POST['name']
                    new_account.password = request.POST['password']
                    new_account.save()
                    # create a new Plan instance and set Plan.account to be new_account
                    free_plan = Plan(account=new_account)
                    free_plan.save()

                    return redirect('form' , account_id = new_account.id)
    else:
        login_form = LoginForm()

    context = {'login_form': login_form}
    return render(request, 'login.html', context)

def logout(request):
    return redirect('home')

def account_details(request , account_id):
    
    account = Account.objects.get(id=account_id)

    account = Account.objects.get(id=account_id)
    user_plan = Plan.objects.get(account = account)
    user_profile = UserProfile.objects.get(account = account)

    context = {
        'account' : account ,
        'user_plan': user_plan ,
        'user_profile' : user_profile ,
        'remaining' : user_plan.forms_remaining - user_plan.forms_filled_on_current_plan
    }

    return render (request, "account_details.html", context)

def form(request , account_id):
    account = Account.objects.get(id=account_id)
    user_plan = Plan.objects.get(account = account)

    if request.method == 'POST':

        for key, value in request.POST.items():
            print(f"{key}: {value}")

        has_previous_user_profile = UserProfile.objects.filter(account_id=account_id).exists()
        if has_previous_user_profile:
            UserProfile.objects.filter(account=account).delete()

        form = UserProfileForm(request.POST, request.FILES)
        user_profile = form.save(commit=False) 
        user_profile.account = account
        user_profile.website_link = settings.REDIRECT_DOMAIN + "/" + account.name
        user_profile.website_link = user_profile.website_link.replace("http://", "")
        user_profile.save()

        post_data = request.POST.dict()
        total_work_forms = int(post_data.get("work_experiences-TOTAL_FORMS", 0))
        work_counter = 1
        if request.POST["hasWorkExperience"] == "yes":
            for i in range(total_work_forms):
                prefix = f"work_experiences-{i}-"
                company_name = post_data.get(prefix + "company_name")
                job_title = post_data.get(prefix + "job_title")
                start_date = post_data.get(prefix + "start_date")
                end_date = post_data.get(prefix + "end_date")
                city = post_data.get(prefix + "city")
                state = post_data.get(prefix + "state")
                description = post_data.get(prefix + "description")
                # bullet1 , bullet2, bullet3 = "bullet1" , "bullet2", "bullet3"

                if company_name and job_title and start_date and end_date and city and state and description:
                    if work_counter == 1 or account.tier != "free":
                        bullet1 , bullet2, bullet3 = openai_work_experience(company_name ,job_title, description)
                        work_counter = work_counter + 1
                    else:
                        bullet1 , bullet2, bullet3 = "UPGRADE PLAN FOR OPTIMIZED BULLET" , "UPGRADE PLAN FOR OPTIMIZED BULLET", "UPGRADE PLAN FOR OPTIMIZED BULLET"
                    work_experience = WorkExperience.objects.create(
                        user_profile=user_profile,
                        company_name=company_name,
                        job_title=job_title,
                        start_date=start_date,
                        end_date=end_date,
                        city=city,
                        state=state,
                        description=description,
                        bullet1= bullet1,
                        bullet2= bullet2,
                        bullet3= bullet3
                    )
                    work_experience.account = account
                    work_experience.save()
        else:
            print("there is no work experiences")

        total_project_forms = int(request.POST.get("projects-TOTAL_FORMS", 0))
        if request.POST.get("hasProjectExperience") == "yes":
            for i in range(total_project_forms):    
                prefix = f"projects-{i}-"
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
                        user_profile=user_profile,
                        project_name=project_name,
                        description=description,
                        project_skills=project_skills,
                        bullet1=bullet1,
                        bullet2=bullet2,
                    )
                    project.account = account
                    project.save()
        else:
            print("There are no projects")

        resume_link = create_resume(user_profile)
        if resume_link == "TIME_OUT_ERROR_974":
            messages.error(request, "TIME_OUT_ERROR_974. Your profile was created however your resume could not due to poor internet signal. Please click the Re-build with same data")
            user_profile.save()
            account.save()
            user_plan.save()
            return redirect('confirmation', account_id=account_id)

        account.set_resume_link(resume_link)
        account.user_profile = user_profile
        user_profile.resume_link = resume_link
        print(user_profile.resume_link)
        user_profile.save()
        user_plan.forms_filled_on_current_plan = user_plan.forms_filled_on_current_plan + 1
        user_plan.total_forms_filled = user_plan.total_forms_filled + 1
        account.save()
        user_plan.save()
        return redirect('confirmation', account_id=account_id)
    
    if request.method == 'GET':

        form = UserProfileForm()
        form = UserProfileForm(instance=account.user_profile)

        work_experience_formset = WorkExperienceFormSet(instance=UserProfile())
        projects_formset = ProjectsFormSet(instance=UserProfile())

        context = {
            'form': form,
            'work_experience_formset': work_experience_formset,
            'projects_formset': projects_formset,
            'account' : account,
            'user_plan' : user_plan,
            'remaining' : user_plan.forms_remaining - user_plan.forms_filled_on_current_plan
        }
        
        return render(request, 'form.html', context)

def website(request, url_name):
    # Retrieve the user profile using url_name
    account = Account.objects.get(name=url_name)
    user_profile = get_object_or_404(UserProfile, account=account)
    user_plan = Plan.objects.get(account = account)

    # Pass the user profile to the template
    context = {
        'user_profile': user_profile,
        'account' : account,
        'user_plan' : user_plan,
    }

    # Render the template with the context
    return render(request, 'website.html', context)

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
            mode='subscription',
            # customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
            metadata={
                'account_id': account_id,  # Include the account_id as metadata
                'price_dictionary_value' : request.POST.get('selected_plan'),
            },
        )
        # print(checkout_session)
        # print()
        # print("stripe.checkout.Session.retrieve is ")
        # print(stripe.checkout.Session.retrieve(checkout_session.id))
        return redirect(checkout_session.url, code=303)

    if request.method == 'GET':
        # Construct the URL
        url = f"http://127.0.0.1:8000/{account.name}"

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
        }

        # Render the template
        template = loader.get_template('confirmation.html')
        return HttpResponse(template.render(context, request))


        

    
    # Render the template
        template = loader.get_template('confirmation.html')
        return HttpResponse(template.render(context, request))

def payment_successful(request):
    if request.method == 'GET':
        stripe.api_key = settings.STRIPE_API_KEY
        print("inside payment_successful")
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
            payment_instance.save()
            account.tier = price_dictionary_value
            user_plan.type = price_dictionary_value
            user_plan.forms_filled_on_current_plan = 0
            user_plan.set_subscription_ids(subscription_value)

        account.save()
        user_plan.save()
        userprofile.save()

        context = {
            'account': account,
            'user_profile': userprofile,
            'user_plan': user_plan,
            'remaining': user_plan.forms_remaining - user_plan.forms_filled_on_current_plan
        }

        return render(request, 'payment_successful.html', context)
    else:
        # Redirect to prevent form resubmission
        messages.error(request, "You cannot reload this page.")
        return redirect('home')  # Redirect to your home page or any other appropriate

def payment_cancelled(request):
    print("payment_cancelled")
    stripe.api_key = settings.STRIPE_API_KEY
    
    return render(request, 'payment_cancelled.html')

def account_payments(request, account_id):
    account = Account.objects.get(id=account_id)
    user_plan = Plan.objects.get(account = account)
    userprofile = UserProfile.objects.get(account = account)

    payment_instances = Payment.objects.filter(account=account)

    # if request.method == 'POST':

    if request.method == 'GET':
        context = {
                    'account' : account,
                    'user_profile': userprofile,
                    'user_plan' : user_plan,
                    'payment_instances' : payment_instances ,
                    'remaining' : user_plan.forms_remaining - user_plan.forms_filled_on_current_plan
        }

        return render(request, 'account_payments.html' , context)

def cancel_subscription(request, account_id, subscription_id):
    stripe.api_key = settings.STRIPE_API_KEY

    try:
        account = Account.objects.get(id=account_id)
        payment_instance = Payment.objects.filter(account=account, subscription_id=subscription_id).get()
        # if (account.password != password):
        #     messages.error(request,"error : incorrect password")
        #     return redirect('account_payments', account_id=account_id)
    except Payment.DoesNotExist:
        messages.error(request,"error : Payment instance not found")
        return redirect('account_payments', account_id=account_id)

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
        messages.success(request, f"Subscription has been cancelled and your plan is still valid until {payment_instance.end_date}.")

    return redirect('account_payments', account_id=account_id)

def reload_resume_and_website_with_job_description(request: HttpRequest, account_id: int):
    try:
        account = Account.objects.get(id=account_id)
        user_plan = Plan.objects.get(account = account)
        user_profile = UserProfile.objects.get(account = account)
        job_description = request.GET.get('JOB_DESCRIPTION', '').strip()

        work_counter = 1
        for i, work_experience in enumerate(user_profile.work_experiences.all(), start=1):
            if work_counter == 1 or account.tier != "free":
                work_experience.bullet1, work_experience.bullet2, work_experience.bullet3 = openai_work_experience(work_experience.company_name, work_experience.job_title, work_experience.description)
                work_counter = work_counter + 1
            else:
                work_experience.bullet1, work_experience.bullet2, work_experience.bullet3 = "UPGRADE PLAN FOR OPTIMIZED BULLET" , "UPGRADE PLAN FOR OPTIMIZED BULLET", "UPGRADE PLAN FOR OPTIMIZED BULLET"
            work_experience.save()

        for i, project in enumerate(user_profile.projects.all(), start=1):
            if work_counter == 1 or account.tier != "free":
                project.bullet1, project.bullet2 = openai_project(project.project_name, project.description)
                work_counter = work_counter + 1
            else:
                project.bullet1, project.bullet2 = "UPGRADE PLAN FOR OPTIMIZED BULLET" , "UPGRADE PLAN FOR OPTIMIZED BULLET"
            project.save()

        new_resume_link = create_resume(user_profile)
        if new_resume_link == "TIME_OUT_ERROR_974":
            messages.error(request, "TIME_OUT_ERROR_974. Could not build personal website and tailored resume due to poor internet. Please try again")
            return redirect('confirmation', account_id=account_id)

        user_profile.resume_link = new_resume_link
        account.set_resume_link(new_resume_link)
        print(user_profile.resume_link)

        user_profile.save()
        user_plan.forms_filled_on_current_plan = user_plan.forms_filled_on_current_plan + 1
        user_plan.total_forms_filled = user_plan.total_forms_filled + 1
        account.save()
        user_plan.save()

        messages.success(request, "personal website and tailored resume created")

    except Timeout:
        messages.error(request, "Timeout error. Your internet connection is slow. Please try again.")
        return redirect('confirmation', account_id=account_id)
    except RefreshError as e:
        messages.error(request, "Timeout error. Your internet connection is slow. Please try again.")
        return redirect('confirmation', account_id=account_id)
    except Exception as e:
        messages.error(request, "Timeout error. Your internet connection is slow. Please try again.")
        return redirect('confirmation', account_id=account_id)

    return redirect('confirmation', account_id=account_id)

def reload_resume_and_website(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        user_plan = Plan.objects.get(account=account)
        user_profile = UserProfile.objects.get(account=account)
        
        work_counter = 1
        for i, work_experience in enumerate(user_profile.work_experiences.all(), start=1):
            if work_counter == 1 or account.tier != "free":
                work_experience.bullet1, work_experience.bullet2, work_experience.bullet3 = openai_work_experience(work_experience.company_name, work_experience.job_title, work_experience.description)
                work_counter = work_counter + 1
            else:
                work_experience.bullet1, work_experience.bullet2, work_experience.bullet3 = "upgrade plan to see optimized bullet" , "upgrade plan to see optimized bullet", "upgrade plan to see optimized bullet"
            work_experience.save()

        for i, project in enumerate(user_profile.projects.all(), start=1):
            if work_counter == 1 or account.tier != "free":
                project.bullet1, project.bullet2 = openai_project(project.project_name, project.description)
                work_counter = work_counter + 1
            else:
                project.bullet1, project.bullet2 = "UPGRADE PLAN FOR OPTIMIZED BULLET" , "UPGRADE PLAN FOR OPTIMIZED BULLET"
            project.save()

        new_resume_link = create_resume(user_profile)
        if new_resume_link == "TIME_OUT_ERROR_974":
            messages.error(request, "TIME_OUT_ERROR_974. Could not re-build personal website and reusme due to poor internet. Please try again")
            return redirect('confirmation', account_id=account_id)

        user_profile.resume_link = new_resume_link
        account.set_resume_link(new_resume_link)
        print(user_profile.resume_link)

        user_profile.save()
        user_plan.forms_filled_on_current_plan = user_plan.forms_filled_on_current_plan + 1
        user_plan.total_forms_filled = user_plan.total_forms_filled + 1
        account.save()
        user_plan.save()

        messages.success(request, "Using same profile data, resume and personal data has been re-built")

    except Timeout:
        messages.error(request, "Timeout error. Your internet connection is slow. Please try again.")

    return redirect('confirmation', account_id=account_id)

def update_resume(user_profile, DOCUMENT_ID):
    
    # Dictionary to store the placeholder replacements
    placeholder_replacements = {
            'name': f"{user_profile.first_name.upper()} {user_profile.last_name.upper()}",
            'email': user_profile.email,
            'phone': user_profile.phone,
            'city': user_profile.city,
            'state': user_profile.state.upper(),
            'linkedin_link': user_profile.linkedin_link,
            'resume_link': user_profile.resume_link,
            'github_link': user_profile.github_link,
            'university': user_profile.institution,
            'university start date': user_profile.start_date.strftime('%b %Y'),
            'university end date' : user_profile.end_date.strftime('%b %Y'),
            'major': user_profile.major,
            'minor': user_profile.minor,
            'spoken_languages': user_profile.spoken_languages,
            'languages': user_profile.programming_languages,
            'technologies': user_profile.technical_skills,
            'leadership': user_profile.leadership,
            'degree_type' : user_profile.degree_type,
            'website_link': user_profile.website_link ,
        }

        # Work experiences
    for i, work_experience in enumerate(user_profile.work_experiences.all(), start=1):
        placeholder_replacements.update({
            f'experience{i}': work_experience.company_name.title(),
            f'title{i}': work_experience.job_title.title(),
            f'experience{i} start date': work_experience.start_date.strftime('%b %Y'),
            f'experience{i} end date': work_experience.end_date.strftime('%b %Y'),
            f'experience{i} location': work_experience.city.strip().title() + ' , ' + work_experience.state.strip().upper(),
            f'experience{i} bullet1': work_experience.bullet1,
            f'experience{i} bullet2': work_experience.bullet2,
            f'experience{i} bullet3': work_experience.bullet3,
        })

    # Projects
    for i, project in enumerate(user_profile.projects.all(), start=1):
        placeholder_replacements.update({
            f'project{i}': project.project_name.title(),
            f'skills{i}': project.project_skills,
            f'project{i} bullet1': project.bullet1,
            f'project{i} bullet2': project.bullet2,
        })

    # Path to your service account credentials JSON file
    SERVICE_ACCOUNT_FILE = '/Users/cheesenaan/Documents/projects/resume_app/project/.ipynb_checkpoints/resume_App/resume_app/resume_app/doc.json'
    #SERVICE_ACCOUNT_FILE = '/home/displayai/displayai/resume_app/doc.json'

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
    remove_blank_lines(DOCUMENT_ID)


    # Get the link of the Google Doc
    resume_link = f"https://docs.google.com/document/d/{DOCUMENT_ID}"
    print("Link to the Google Doc:", resume_link)
    user_profile.resume_link = resume_link
    user_profile.save()
    return 

def create_resume(user_profile):
    
    try:
        # Dictionary to store the placeholder replacements
        placeholder_replacements = {
                'name': f"{user_profile.first_name.upper()} {user_profile.last_name.upper()}",
                'email': user_profile.email,
                'phone': user_profile.phone,
                'city': user_profile.city,
                'state': user_profile.state.upper(),
                'linkedin_link': user_profile.linkedin_link,
                'resume_link': user_profile.resume_link,
                'github_link': user_profile.github_link,
                'university': user_profile.institution,
                'university start date': user_profile.start_date.strftime('%b %Y'),
                'university end date' : user_profile.end_date.strftime('%b %Y'),
                'major': user_profile.major,
                'minor': user_profile.minor,
                'spoken_languages': user_profile.spoken_languages,
                'languages': user_profile.programming_languages,
                'technologies': user_profile.technical_skills,
                'leadership': user_profile.leadership,
                'degree_type' : user_profile.degree_type,
                'website_link': user_profile.website_link ,
            }

            # Work experiences
        for i, work_experience in enumerate(user_profile.work_experiences.all(), start=1):
            placeholder_replacements.update({
                f'experience{i}': work_experience.company_name.title(),
                f'title{i}': work_experience.job_title.title(),
                f'experience{i} start date': work_experience.start_date.strftime('%b %Y'),
                f'experience{i} end date': work_experience.end_date.strftime('%b %Y'),
                f'experience{i} location': work_experience.city.strip().title() + ' , ' + work_experience.state.strip().upper(),
                f'experience{i} bullet1': work_experience.bullet1,
                f'experience{i} bullet2': work_experience.bullet2,
                f'experience{i} bullet3': work_experience.bullet3,
            })
        for i, project in enumerate(user_profile.projects.all(), start=1):
            placeholder_replacements.update({
                f'project{i}': project.project_name.title(),
                f'skills{i}': project.project_skills,
                f'project{i} bullet1': project.bullet1,
                f'project{i} bullet2': project.bullet2,
            })

        # Path to your service account credentials JSON file
        SERVICE_ACCOUNT_FILE = '/Users/cheesenaan/Documents/projects/resume_app/project/.ipynb_checkpoints/resume_App/resume_app/resume_app/doc.json'
        #SERVICE_ACCOUNT_FILE = '/home/displayai/displayai/resume_app/doc.json'

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
        SERVICE_ACCOUNT_FILE = '/Users/cheesenaan/Documents/projects/resume_app/project/.ipynb_checkpoints/resume_App/resume_app/resume_app/doc.json'
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
        work_experiences = []
        projects = []

        for i, work_experience in enumerate(user_profile.work_experiences.all(), start=1):
            work_experiences.append(work_experience)

        for i, project in enumerate(user_profile.projects.all(), start=1):
            projects.append(project)


        openai.api_key = settings.OPENAI_API_KEY
        current_date = time.strftime("%Y-%m-%d")

        prompt = f"""
        Using my work experinces and projects, build a cover letter. Do not add any placeholders
        name : {user_profile.first_name} + {user_profile.last_name}
        phone : {user_profile.phone}
        email : {user_profile.email}
        address : {user_profile.city} + {user_profile.state}
        institution : {user_profile.institution}
        education : {user_profile.major} + {user_profile.minor}
        skills : {user_profile.programming_languages}  + {user_profile.technical_skills}
        date : {current_date}
        work_experiences : {work_experiences}
        projects ; {projects}
        job description : {job_description}
        'website_link': {user_profile.website_link} ,
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

    return redirect('confirmation', account_id=account_id)

def openai_work_experience_with_job_description(JOB_DESCRIPTION, EXPERIENCE ,TITLE, DESCRIPTION):
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
    give me exactly 3 very short, concise, and numerically quantified one sentence resume points for experience
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
        name = request.GET.get('name', None)
        data = {'is_taken': Account.objects.filter(name=name).exists()}
        return JsonResponse(data)

# def stripe_webhook(request):
#     stripe.api_key = settings.STRIPE_API_KEY

#     time.sleep(10)
#     payload = request.body
#     signature_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None
#     print("inside stripe_webhook")
#     try:
#         print("event 1")
#         event = stripe.Webhook.construct_event(
#             payload, signature_header, 'whsec_225411bfa0199497eabcad4a58cfc6cd5007421edbc018658d5ab000eeeeccdc'
#         )
#     except ValueError as e:
#         print("event 2")
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         print("event 3")
#         return HttpResponse(status=400)
    
#     if event['type'] == 'checkout.session.completed':
#         print("checkout.session.completed !!!!")

#         session = event['data']['object']
#         session_id = session.get('id', None)
#         time.sleep(15)
    
#     return HttpResponse(status=200)

