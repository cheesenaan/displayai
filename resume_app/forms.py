from django import forms
from .models import *
from django import forms
from django import forms
from .models import *

from django import forms
from django.core.exceptions import ValidationError
from .models import WorkExperience, UserProfile, Account

from django import forms
from .models import Education
from django.forms import formset_factory, BaseFormSet

from django import forms
from .models import Education

from django import forms
from .models import Education
from django.forms import inlineformset_factory

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'major', 'minor', 'start_date', 'end_date', 'current', 'degree_type', 'GPA', 'city', 'country', 'coursework']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'current': forms.CheckboxInput(),  # Add the checkbox widget
        }

    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['end_date'].widget = forms.DateInput(attrs={'type': 'date'})

EducationFormSet = inlineformset_factory(Account, Education, form=EducationForm, extra=1, can_delete=True)



class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'job_title', 'start_date', 'end_date', 'currently_working', 'city', 'state', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'currently_working': forms.CheckboxInput(),  # Add the checkbox widget
        }

    def clean(self):
        cleaned_data = super().clean()

        required_fields = [
            'company_name', 'job_title', 'start_date', 'city', 'state', 'description'
        ]

        for field_name in required_fields:
            if not cleaned_data.get(field_name):
                raise ValidationError(f"Please fill in the '{field_name.replace('_', ' ')}' field.")

        currently_working = cleaned_data.get('currently_working')
        end_date = cleaned_data.get('end_date')

        if currently_working:
            cleaned_data['end_date'] = None
        elif not end_date:
            raise ValidationError("Please provide an end date if you are not currently working.")

        if end_date and cleaned_data.get('start_date') > end_date:
            raise ValidationError("End date must be greater than start date.")

        return cleaned_data

WorkExperienceFormSet = forms.inlineformset_factory(Account, WorkExperience, form=WorkExperienceForm, extra=1, can_delete=True)



class ProjectsForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['project_name', 'description', 'project_skills']
        widgets = {
            'project_skills': forms.TextInput(attrs={'placeholder': 'Python, Excel, Communication'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['project_name', 'description', 'project_skills']

        for field_name in required_fields:
            if not cleaned_data.get(field_name):
                raise ValidationError(f"This field is required: {field_name.replace('_', ' ')}")

        return cleaned_data


ProjectsFormSet = forms.inlineformset_factory(Account, Project, form=ProjectsForm, extra=1, can_delete=True)

class UserProfileForm(forms.ModelForm):

    fields_to_capitalize = [
        'first_name', 'last_name', 'city', 'state', 
        'spoken_languages', 
        'programming_languages', 'technical_skills', 'leadership'
    ]


    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone','city', 'state', 'linkedin_link', 'github_link', 'profile_image', 'spoken_languages', 'programming_languages', 'technical_skills', 'leadership']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': ''}),
            'last_name': forms.TextInput(attrs={'placeholder': ''}),
            'phone': forms.TextInput(attrs={'placeholder': ''}),
            # 'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
            'city': forms.TextInput(attrs={'placeholder': ''}),
            'state': forms.TextInput(attrs={'placeholder': '2-letter abbreviation'}),
            'linkedin_link': forms.URLInput(attrs={'placeholder': 'https://www.'}),
            'resume_link': forms.URLInput(attrs={'placeholder': 'https://www.'}),
            'github_link': forms.URLInput(attrs={'placeholder': 'https://www.'}),
            'profile_image': forms.ClearableFileInput(attrs={'placeholder': ''}),
            'spoken_languages': forms.TextInput(attrs={'placeholder': 'English, Spanish, Arabic ... '}),
            'programming_languages': forms.TextInput(attrs={'placeholder': 'Python, R, C, Java ... '}),
            'technical_skills': forms.TextInput(attrs={'placeholder': 'Excel, AWS, GCP, ... '}),
            'leadership': forms.TextInput(attrs={'placeholder': 'Soccer club, Hackathon ...'}),
        }

        


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # self.fields['leadership'].help_text = '<h6 style="color: maroon; font-weight: bold;">Your website will be hosted on displayai.pythonanywhere.com/url-name/</h6> </p>'
        
    def clean(self):
        cleaned_data = super().clean()
        for field_name in self.fields_to_capitalize:
            if cleaned_data.get(field_name):
                cleaned_data[field_name] = cleaned_data[field_name].title()
        return cleaned_data
    

from django import forms
from .models import Account

class LoginForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    email = models.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['name','email', 'password']


    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # self.fields['password'].help_text = '<h6 style="color: maroon; font-weight: bold;">website will be hosted on display.ai/name/</h6> <br> <h6 style="color: maroon; font-weight: bold;"> Resume on google docs /</h6> </p>'
