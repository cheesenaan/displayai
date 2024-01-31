from django import forms
from .models import *

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'job_title', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


WorkExperienceFormSet = forms.inlineformset_factory(UserProfile, WorkExperience, form=WorkExperienceForm, extra=1, can_delete=True)

class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'description', 'project_skills']
        widgets = {
            'project_skills': forms.TextInput(attrs={'placeholder': 'Python, HTML, CSS, Javascript'}),
        }

ProjectsFormSet = forms.inlineformset_factory(UserProfile, Project, form=ProjectsForm, extra=1, can_delete=True)

from django import forms

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone', 'email', 'city', 'state', 'linkedin_link', 'resume_link', 'github_link' ,'profile_image', 'institution', 'major', 'minor', 'start_date', 'end_date', 'url_name', 'spoken_languages', 'programming_languages', 'technical_skills', 'leadership']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'REQUIRED'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'REQUIRED'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter your city'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter your state'}),
            'linkedin_link': forms.URLInput(attrs={'placeholder': 'https://www.linkedin.com/in/sulemaan-farooq/'}),
            'resume_link': forms.URLInput(attrs={'placeholder': 'https://www.'}),
            'github_link': forms.URLInput(attrs={'placeholder': 'https://www.github.com'}),
            'profile_image': forms.ClearableFileInput(attrs={'placeholder': 'Choose a profile image'}),
            'institution': forms.TextInput(attrs={'placeholder': 'Enter your university'}),
            'major': forms.TextInput(attrs={'placeholder': 'Enter your major'}),
            'minor': forms.TextInput(attrs={'placeholder': 'Enter your minor'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'url_name': forms.TextInput(attrs={'placeholder': 'REQUIRED'}),
            'spoken_languages': forms.TextInput(attrs={'placeholder': 'English, Spanish, Arabic ... '}),
            'programming_languages': forms.TextInput(attrs={'placeholder': 'Python, R, C, Java ... '}),
            'technical_skills': forms.TextInput(attrs={'placeholder': 'Excel, AWS, GCP, ... '}),
            'leadership': forms.TextInput(attrs={'placeholder': 'Soccer club, Hackathon ...'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False  # Make all fields initially not required

        # Set required status for specific fields
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['url_name'].required = True


