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
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    linkedin_link = models.URLField()
    resume_link = models.URLField()
    github_link = models.URLField()
    profile_image = models.ImageField()
    institution = models.CharField(max_length=255, blank=True, null=True)
    major = models.CharField(max_length=255, blank=True, null=True)
    minor = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(default='2023-12-31')  
    end_date = models.DateField(default='2023-12-31')

    spoken_languages = models.CharField(max_length=255, blank=True, null=True)
    programming_languages = models.CharField(max_length=255, blank=True, null=True)
    technical_skills = models.CharField(max_length=255, blank=True, null=True)

    leadership = models.CharField(max_length=255, blank=True, null=True)

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

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date must be greater than start date.")

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




