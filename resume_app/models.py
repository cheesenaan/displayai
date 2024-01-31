import datetime
from django.db import models

# class user_resume_data(models.Model):
#     ID = models.AutoField(primary_key=True)
#     NAME = models.CharField(max_length=100, null=True)
#     LINK = models.CharField(max_length=100, null=True)
#     EMAIL = models.EmailField(null=True)
#     PHONE = models.CharField(max_length=20, null=True)
#     CITY = models.CharField(max_length=100, null=True)
#     STATE = models.CharField(max_length=50, null=True)
#     RESUME_LINK = models.URLField(null=True)
#     UNIVERSITY = models.CharField(max_length=100, null=True)
#     DEGREE_TYPE = models.CharField(max_length=100, null=True)
#     UNIVERSITY_START_DATE = models.CharField(max_length=100, null=True)
#     UNIVERSITY_END_DATE = models.CharField(max_length=100, null=True)
#     MAJOR = models.CharField(max_length=100, null=True)
#     MINOR = models.CharField(max_length=100, null=True)
#     GPA = models.FloatField(null=True)
#     EXPERIENCE1 = models.CharField(max_length=200, null=True)
#     EXPERIENCE1_START_DATE = models.CharField(max_length=100, null=True)
#     EXPERIENCE1_END_DATE = models.CharField(max_length=100, null=True)
#     TITLE1 = models.CharField(max_length=100, null=True)
#     EXPERIENCE1_LOCATION = models.CharField(max_length=100, null=True)
#     EXPERIENCE1_BULLET1 = models.TextField(null=True)
#     EXPERIENCE1_BULLET2 = models.TextField(null=True)
#     EXPERIENCE1_BULLET3 = models.TextField(null=True)
#     EXPERIENCE2 = models.CharField(max_length=200, null=True)
#     EXPERIENCE2_START_DATE = models.CharField(max_length=100, null=True)
#     EXPERIENCE2_END_DATE = models.CharField(max_length=100, null=True)
#     TITLE2 = models.CharField(max_length=100, null=True)
#     EXPERIENCE2_LOCATION = models.CharField(max_length=100, null=True)
#     EXPERIENCE2_BULLET1 = models.TextField(null=True)
#     EXPERIENCE2_BULLET2 = models.TextField(null=True)
#     EXPERIENCE2_BULLET3 = models.TextField(null=True)
#     EXPERIENCE3 = models.CharField(max_length=200, null=True)
#     EXPERIENCE3_START_DATE = models.CharField(max_length=100, null=True)
#     EXPERIENCE3_END_DATE = models.CharField(max_length=100, null=True)
#     TITLE3 = models.CharField(max_length=100, null=True)
#     EXPERIENCE3_LOCATION = models.CharField(max_length=100, null=True)
#     EXPERIENCE3_BULLET1 = models.TextField(null=True)
#     EXPERIENCE3_BULLET2 = models.TextField(null=True)
#     EXPERIENCE3_BULLET3 = models.TextField(null=True)
#     EXPERIENCE4 = models.CharField(max_length=200, null=True)
#     EXPERIENCE4_START_DATE = models.CharField(max_length=100, null=True)
#     EXPERIENCE4_END_DATE = models.CharField(max_length=100, null=True)
#     TITLE4 = models.CharField(max_length=100, null=True)
#     EXPERIENCE4_LOCATION = models.CharField(max_length=100, null=True)
#     EXPERIENCE4_BULLET1 = models.TextField(null=True)
#     EXPERIENCE4_BULLET2 = models.TextField(null=True)
#     EXPERIENCE4_BULLET3 = models.TextField(null=True)
#     EXPERIENCE5 = models.CharField(max_length=200, null=True)
#     EXPERIENCE5_START_DATE = models.CharField(max_length=100, null=True)
#     EXPERIENCE5_END_DATE = models.CharField(max_length=100, null=True)
#     TITLE5 = models.CharField(max_length=100, null=True)
#     EXPERIENCE5_LOCATION = models.CharField(max_length=100, null=True)
#     EXPERIENCE5_BULLET1 = models.TextField(null=True)
#     EXPERIENCE5_BULLET2 = models.TextField(null=True)
#     EXPERIENCE5_BULLET3 = models.TextField(null=True)
#     PROJECT1 = models.CharField(max_length=100, null=True)
#     PROJECT1_BULLET1 = models.TextField(null=True)
#     PROJECT1_BULLET2 = models.TextField(null=True)
#     PROJECT2 = models.CharField(max_length=100, null=True)
#     PROJECT2_BULLET1 = models.TextField(null=True)
#     PROJECT2_BULLET2 = models.TextField(null=True)
#     PROJECT3 = models.CharField(max_length=100, null=True)
#     PROJECT3_BULLET1 = models.TextField(null=True)
#     PROJECT3_BULLET2 = models.TextField(null=True)
#     PROJECT4 = models.CharField(max_length=100, null=True)
#     PROJECT4_BULLET1 = models.TextField(null=True)
#     PROJECT4_BULLET2 = models.TextField(null=True)
#     PROJECT5 = models.CharField(max_length=100, null=True)
#     PROJECT5_BULLET1 = models.TextField(null=True)
#     PROJECT5_BULLET2 = models.TextField(null=True)
#     LANGUAGES = models.CharField(max_length=200, null=True)
#     TECHNOLOGIES = models.CharField(max_length=200, null=True)
#     LEADERSHIP = models.CharField(max_length=200, null=True)

# class test(models.Model):
#     NAME = models.CharField(max_length=100)


from django.db import models
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


    def __str__(self):
        return f"{self.id}: {self.url_name}"


from django.db import models

class WorkExperience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='work_experiences')
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    bullet1 = models.CharField(max_length=255)
    bullet2 = models.CharField(max_length=255)
    bullet3 = models.CharField(max_length=255)

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




