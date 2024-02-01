from django import forms
from .models import *
from django import forms
from django import forms
from .models import UserProfile

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'job_title', 'start_date', 'end_date', 'city', 'state', 'description']
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

class UserProfileForm(forms.ModelForm):

    fields_to_capitalize = [
        'first_name', 'last_name', 'city', 'state', 
        'institution', 'major', 'minor', 'spoken_languages', 
        'programming_languages', 'technical_skills', 'leadership'
    ]

    DEGREE_CHOICES = [
        ('Science', 'Science'),
        ('Art', 'Art'),
    ]

    degree_type = forms.ChoiceField(
        choices=DEGREE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )


    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone', 'email', 'city', 'state', 'linkedin_link', 'resume_link', 'github_link', 'profile_image', 'institution', 'degree_type', 'major', 'minor', 'start_date', 'end_date', 'spoken_languages', 'programming_languages', 'technical_skills', 'leadership', 'url_name']
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
            'spoken_languages': forms.TextInput(attrs={'placeholder': 'English, Spanish, Arabic ... '}),
            'programming_languages': forms.TextInput(attrs={'placeholder': 'Python, R, C, Java ... '}),
            'technical_skills': forms.TextInput(attrs={'placeholder': 'Excel, AWS, GCP, ... '}),
            'leadership': forms.TextInput(attrs={'placeholder': 'Soccer club, Hackathon ...'}),
            'url_name': forms.TextInput(attrs={'placeholder': 'REQUIRED'}),
        }


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['leadership'].help_text = '<h6 style="color: maroon; font-weight: bold;">Your website will be hosted on displayai.pythonanywhere.com/url-name/</h6> </p>'
        self.fields['linkedin_link'].help_text = '<h6 style="color: maroon; font-weight: bold;">Leave resume link blank and we will create one for you !</h6> </p>'
        
    def clean(self):
        cleaned_data = super().clean()
        for field_name in self.fields_to_capitalize:
            if field_name in cleaned_data:
                cleaned_data[field_name] = cleaned_data[field_name].title()
        return cleaned_data
    
    def clean_url_name(self):
        url_name = self.cleaned_data['url_name']
        existing_profiles = UserProfile.objects.filter(url_name=url_name)

        if self.instance.pk:
            existing_profiles = existing_profiles.exclude(pk=self.instance.pk)

        if existing_profiles.exists():
            raise ValidationError('This URL name is already in use. Please choose a different one.')

        return url_name

