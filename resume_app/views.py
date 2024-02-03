import os
from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse
from .models import UserProfile
from .forms import *
import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
import gspread
from google.oauth2.service_account import Credentials
from django.shortcuts import redirect
import openai
import httplib2
from django.http import JsonResponse
from django.views import View
from .models import UserProfile


def home(request):
    return render(request, "home.html")

def website_form(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        for key, value in request.POST.items():
            print(f"{key}: {value}")

        if form.is_valid():
            user_profile = form.save(commit=False) 
            user_profile.save()
            if 'profile_image' in request.FILES:
                profile_image = request.FILES['profile_image']
                destination_path = os.path.join(settings.STATIC_ROOT_PROFILE_PICS, f"{str(user_profile.id)}.jpg")
                with open(destination_path, 'wb+') as destination:
                    for chunk in profile_image.chunks():
                        destination.write(chunk)

                # Update the UserProfile instance with the correct profile_image path
                user_profile.profile_image = f"profile_pics/{str(user_profile.id)}.jpg"
                user_profile.save()
                delete_jpeg_files()
        else:
            print("Form is not valid!")
            print("Errors:", form.errors)
            print("Cleaned data:", form.cleaned_data)
            print("Non-form errors:", form.non_field_errors())

        work_experience_formset = WorkExperienceFormSet(request.POST, instance=user_profile)
        if request.POST["hasWorkExperience"] == "on":
            for workForm in work_experience_formset:
                company_name = workForm.cleaned_data.get('company_name')
                job_title = workForm.cleaned_data.get('job_title')
                description = workForm.cleaned_data.get('description')

                #bullet1, bullet2, bullet3 = openai_work_experience(company_name, job_title, description)
                bullet1, bullet2, bullet3 = "bullet1", "bullet2", "bullet3"

                work_experience_instance = workForm.save(commit=False)
                work_experience_instance.bullet1 = bullet1
                work_experience_instance.bullet2 = bullet2
                work_experience_instance.bullet3 = bullet3
                work_experience_instance.save()
    
            work_experience_formset.save()
        else:
            print("there is no work experiences")

        project_formset = ProjectsFormSet(request.POST, instance=user_profile)
        if project_formset.is_valid():
            for projectForm in project_formset:
                project_name = projectForm.cleaned_data.get('project_name')
                description = projectForm.cleaned_data.get('description')
                #bullet1, bullet2 = openai_project(project_name , description)
                bullet1, bullet2 = "bullet1", "bullet2"
                project_instance = projectForm.save(commit=False)
                project_instance.bullet1 = bullet1
                project_instance.bullet2 = bullet2
                project_instance.save()
        else:
            print("project_formset is not valid!")
            print("Errors:", form.errors)
            print("Cleaned data:", form.cleaned_data)
            print("Non-form errors:", form.non_field_errors())

        user_profile.save()
        return redirect('website', url_name=user_profile.url_name)

    if request.method == 'GET':
        form = UserProfileForm()
        work_experience_formset = WorkExperienceFormSet(instance=UserProfile())
        projects_formset = ProjectsFormSet(instance=UserProfile())

        context = {
            'form': form,
            'work_experience_formset': work_experience_formset,
            'projects_formset': projects_formset,
        }
        
        return render(request, 'website_form.html', context)

def website(request, url_name):
    # Retrieve the user profile using url_name
    user_profile = get_object_or_404(UserProfile, url_name=url_name)

    # Pass the user profile to the template
    context = {
        'user_profile': user_profile,
    }

    # Render the template with the context
    return render(request, 'website.html', context)

def edit_website(request, url_name):
    user_profile = get_object_or_404(UserProfile, url_name=url_name)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            new_url_name = form.cleaned_data['url_name']
            # if new_url_name != user_profile.url_name:
                # validate_unique_url_name(new_url_name)

            if 'profile_image' in request.FILES:
                profile_image = request.FILES['profile_image']
                destination_path = os.path.join(settings.STATIC_ROOT_PROFILE_PICS, f"{str(user_profile.id)}.jpg")
                with open(destination_path, 'wb+') as destination:
                    for chunk in profile_image.chunks():
                        destination.write(chunk)
                user_profile.profile_image = f"profile_pictures/{user_profile.id}.jpg"
                user_profile.save()

            form.save()

            # Handle work experiences and projects similarly to website_form
            total_project_forms = request.POST.get('projects-TOTAL_FORMS')
            total_project_forms = int(total_project_forms) if total_project_forms else 0
            print("total_project_forms is ", total_project_forms)
            for i in range(total_project_forms+1):
                project_name = request.POST.get(f'projects-{i}-project_name')
                project_skills = request.POST.get(f'projects-{i}-project_skills')
                description = request.POST.get(f'projects-{i}-description')

                if project_name:
                    Project.objects.create(
                        user_profile=user_profile,
                        project_name=project_name,
                        project_skills=project_skills,
                        description=description
                    )

            return redirect('website', url_name=user_profile.url_name)

    else:
        form = UserProfileForm(instance=user_profile)

    # Similar to website_form, retrieve and pass project forms to the template
    projects_formset = ProjectsFormSet(instance=user_profile)
    context = {
        'form': form,
        'user_profile': user_profile,
        'projects_formset': projects_formset,
    }
    return render(request, 'edit_website_form.html', context)

def delete_jpeg_files():
    # Get the current directory
    current_directory = os.getcwd()

    # List all files in the current directory
    files = os.listdir(current_directory)

    # Iterate through files and delete JPEG files
    for file in files:
        if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg"):
            file_path = os.path.join(current_directory, file)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

def create_resume(user_profile):
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
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
            f'skills{i}': project.project_skills.title(),
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
    for i in range(len(body_content) - 1, -1, -1):
        paragraph = body_content[i]
        if 'paragraph' in paragraph:
            elements = paragraph['paragraph']['elements']
            for element in elements:
                if 'textRun' in element:
                    content = element['textRun']['content']
                    if 'empty' in content:
                        # Remove the paragraph if it contains the string "empty"
                        requests = [
                            {
                                'deleteContentRange': {
                                    'range': {
                                        'startIndex': paragraph['startIndex'],
                                        'endIndex': paragraph['endIndex']
                                    }
                                }
                            }
                        ]
                        service.documents().batchUpdate(documentId=DOCUMENT_ID,  body={'requests': requests}).execute()
                        break  # Skip to the next paragraph after deleting the current one

    print("Rows with 'empty' text removed successfully!")
    # Get the link of the Google Doc
    resume_link = f"https://docs.google.com/document/d/{DOCUMENT_ID}"
    print("Link to the Google Doc:", resume_link)
    return resume_link

def openai_work_experience(EXPERIENCE ,TITLE, DESCRIPTION):

    openai.api_key = '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'

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

    openai.api_key = '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'

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

    # Assign each bullet point to a variable
    one = lines[0].split('. ')[1]
    two = lines[1].split('. ')[1]

    return one, two



class CheckUrlNameView(View):
    def get(self, request, *args, **kwargs):
        url_name = request.GET.get('url_name', None)
        data = {'is_taken': UserProfile.objects.filter(url_name=url_name).exists()}
        return JsonResponse(data)


