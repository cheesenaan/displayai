import datetime
from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError

def validate_unique_url_name(value):
    existing_profiles = UserProfile.objects.filter(url_name=value)
    if existing_profiles.exists():
        raise ValidationError('This URL name is already taken. Please choose a different one.')

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True) # needs to be unique
    password = models.CharField(max_length=255)
    tier = models.CharField(max_length=255, default = "free")
    user_profile = models.ForeignKey('UserProfile', on_delete=models.SET_NULL, null=True, related_name='user_profile_account')
    resume_links = models.CharField(max_length=100000, blank=True, null=True, help_text="Separate links with commas")

    def get_resume_links(self):
        return self.resume_links.split(',') if self.resume_links else []

    def set_resume_link(self, link):
        links = self.get_resume_links()
        links.append(link)
        self.resume_links = ','.join(links)

    def __str__(self):
        return f"{self.id}: {self.name}"

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='account_user_profile')
    # url_name = models.CharField(max_length=255, unique=True)
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
    start_date = models.DateField()
    end_date = models.DateField()

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
        return f"{self.id}: {self.account}"

class WorkExperience(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
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
        return f"Account : {self.account} , {self.company_name}"

class Project(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=255)
    project_skills = models.CharField(max_length=255)
    description = models.TextField()
    bullet1 = models.CharField(max_length=255)
    bullet2 = models.CharField(max_length=255)

    def __str__(self):
        return f"Account : {self.account}"

class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, default="free")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    forms_remaining = models.IntegerField(default=2)
    forms_filled_on_current_plan = models.IntegerField(default=0)
    total_forms_filled = models.IntegerField(default=0)
    total_cover_letters = models.IntegerField(default=0)
    total_tailored_resumes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Define the mapping of types to forms_remaining values
        type_forms_mapping = {
            'free': 2,
            'basic': 5,
            'economy': 10,
            'business': 20,
            'first_class': 50,
            'pilot': 100,
            'pilot2': 300,
        }

        # Update forms_remaining based on the type
        self.forms_remaining = type_forms_mapping.get(self.type, 2)

        # Call the original save method to save the changes
        super(Plan, self).save(*args, **kwargs)

    
# class UserProfile(models.Model):
#     id = models.AutoField(primary_key=True)
#     url_name = models.CharField(max_length=255, unique=True)
#     first_name = models.CharField(max_length=255, default='Sulemaan')
#     last_name = models.CharField(max_length=255, default='Farooq')
#     phone = models.CharField(max_length=15, default='9174565697')
#     email = models.EmailField(default='shf46@rutgers.edu')
#     city = models.CharField(max_length=255, default='Edison')
#     state = models.CharField(max_length=255, default='NJ')
#     linkedin_link = models.URLField(default='https://www.linkedin.com/in/sulemaan-farooq/')
#     resume_link = models.URLField(default='https://www.linkedin.com/in/sulemaan-farooq/')
#     github_link = models.URLField(default='https://www.linkedin.com/in/sulemaan-farooq/')
#     profile_image = models.ImageField()
#     institution = models.CharField(max_length=255, blank=True, null=True, default='Rutgers')
#     major = models.CharField(max_length=255, blank=True, null=True, default='computer science')
#     minor = models.CharField(max_length=255, blank=True, null=True, default='data science')
#     start_date = models.DateField(default='2023-12-31')  
#     end_date = models.DateField(default='2023-12-31')

#     spoken_languages = models.CharField(max_length=255, blank=True, null=True, default='English, Arabic, Urdu')
#     programming_languages = models.CharField(max_length=255, blank=True, null=True, default=' R, Java, , Spring Boot Pythonanywhere, React, Ruby')
#     technical_skills = models.CharField(max_length=255, blank=True, null=True, default='GCP, Springboot, DataDog')

#     leadership = models.CharField(max_length=255, blank=True, null=True, default='rutgers sports club')

#     DEGREE_CHOICES = [
#         ('Science', 'Science'),
#         ('Art', 'Art'),
#     ]

#     degree_type = models.CharField(
#         max_length=10,
#         choices=DEGREE_CHOICES,
#         blank=True,
#         null=True,
#     )

#     def __str__(self):
#         return f"{self.id}: {self.url_name}"