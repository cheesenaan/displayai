import datetime
from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError

def validate_unique_url_name(value):
    existing_profiles = UserProfile.objects.filter(url_name=value)
    if existing_profiles.exists():
        raise ValidationError('This URL name is already taken. Please choose a different one.')

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    url_name = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, default='Sulemaan')
    last_name = models.CharField(max_length=255, default='Farooq')
    phone = models.CharField(max_length=15, default='9174565697')
    email = models.EmailField(default='shf46@rutgers.edu')
    city = models.CharField(max_length=255, default='Edison')
    state = models.CharField(max_length=255, default='NJ')
    linkedin_link = models.URLField(default='https://www.linkedin.com/in/sulemaan-farooq/')
    resume_link = models.URLField(default='https://www.linkedin.com/in/sulemaan-farooq/')
    github_link = models.URLField(default='https://www.linkedin.com/in/sulemaan-farooq/')
    profile_image = models.ImageField()
    institution = models.CharField(max_length=255, blank=True, null=True, default='Rutgers')
    major = models.CharField(max_length=255, blank=True, null=True, default='computer science')
    minor = models.CharField(max_length=255, blank=True, null=True, default='data science')
    start_date = models.DateField(default='2023-12-31')  
    end_date = models.DateField(default='2023-12-31')

    spoken_languages = models.CharField(max_length=255, blank=True, null=True, default='English, Arabic, Urdu')
    programming_languages = models.CharField(max_length=255, blank=True, null=True, default=' R, Java, , Spring Boot Pythonanywhere, React, Ruby')
    technical_skills = models.CharField(max_length=255, blank=True, null=True, default='GCP, Springboot, DataDog')

    leadership = models.CharField(max_length=255, blank=True, null=True, default='rutgers sports club')

    DEGREE_CHOICES = [
        ('Science', 'Science'),
        ('Art', 'Art'),
    ]

    degree_type = models.CharField(
        max_length=10,
        choices=DEGREE_CHOICES,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.id}: {self.url_name}"

class WorkExperience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='work_experiences')
    company_name = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    job_title = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2), MaxLengthValidator(2)])
    description = models.TextField(validators=[MinLengthValidator(1)])
    bullet1 = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    bullet2 = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    bullet3 = models.CharField(max_length=255, validators=[MinLengthValidator(1)])

    def __str__(self):
        return f"{self.id}: {self.user_profile}"

class Project(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=255)
    project_skills = models.CharField(max_length=255)
    description = models.TextField()
    bullet1 = models.CharField(max_length=255)
    bullet2 = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}: {self.user_profile}"




