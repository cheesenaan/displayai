import datetime
import os
from django.conf import settings
from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError
import stripe
from django.db import models
import stripe
from datetime import datetime
from django.db import models
from datetime import date
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import date
import os


def validate_unique_url_name(value):
    existing_profiles = UserProfile.objects.filter(url_name=value)
    if existing_profiles.exists():
        raise ValidationError('This URL name is already taken. Please choose a different one.')

from django.contrib.auth.models import User 

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='account_user')
    name = models.CharField(max_length=255, unique=True) # needs to be unique
    password = models.CharField(max_length=255)
    email = models.EmailField()
    tier = models.CharField(max_length=255, default = "free")
    user_profile = models.ForeignKey('UserProfile', on_delete=models.SET_NULL, null=True, related_name='user_profile_account')
    user_plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True, related_name='user_plan')
    user_payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, related_name='user_payment')
    resume_links = models.CharField(max_length=100000, blank=True, null=True, help_text="Separate links with commas")
    unique_words = models.CharField(max_length=10000000, blank=True, null=True, help_text="Separate actions words with commas")
    reset_password_code = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)

    def get_resume_links(self):
        return self.resume_links.split(',') if self.resume_links else []

    def set_resume_link(self, link):
        links = self.get_resume_links()
        links.append(link)
        self.resume_links = ','.join(links)

    def get_unique_words_list(self):
        return self.unique_words.split(',') if self.unique_words else []

    def add_unique_word(self, word):
        words = self.get_unique_words_list()
        words.append(word)
        self.unique_words = ','.join(words)


    def __str__(self):
        return f"{self.id}: {self.name}"

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # If the file already exists, remove it so the new file can be saved
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class UserProfile(models.Model):

    def profile_image_upload_to(instance, filename):
        return f"profile_pictures/{instance.account.id}.jpg"
    
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='account_user_profile')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_profile_user')
    # url_name = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    # email = models.EmailField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    linkedin_link = models.URLField(blank=True, null=True)
    resume_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    website_link = models.URLField(blank=True, null=True)
    profile_image = models.ImageField(upload_to=profile_image_upload_to, storage=OverwriteStorage(), blank=True, null=True)
    institution = models.CharField(max_length=255, blank=True, null=True)
    major = models.CharField(max_length=255, blank=True, null=True)
    minor = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
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
    subscription_ids = models.CharField(max_length=100000, blank=True, null=True, help_text="subscription_ids seperated by commas")


    def get_subscription_ids(self):
        return self.subscription_ids.split(',') if self.subscription_ids else []

    def set_subscription_ids(self, subscription_id):
        ids = set(self.get_subscription_ids())  # Use a set to ensure uniqueness
        ids.add(subscription_id)
        self.subscription_ids = ','.join(ids)


    def save(self, *args, **kwargs):
        # Define the mapping of types to forms_remaining values
        type_forms_mapping = {
            'free': 2,
            'basic': 20,
            'economy': 50,
            'business': 100,
            'first_class': 200,
            'pilot': 400,
            'pilot2': 1000,
        }

        # Update forms_remaining based on the type
        self.forms_remaining = type_forms_mapping.get(self.type, 2)

        # Call the original save method to save the changes
        super(Plan, self).save(*args, **kwargs)

    def __str__(self):
            return f"{self.account}"

class Payment(models.Model):

    PAYMENT_MODE_CHOICES = [
        ('payment', 'Payment'),
        ('subscription', 'Subscription'),
    ]

    mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, default='payment')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='account_payments')
    subscription_id = models.CharField(max_length=100000, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    subscription_status = models.CharField(max_length=100, blank=True, null=True)
    subscription_cancel_status = models.BooleanField(default=False)
    subscription_cancel_status_text = models.CharField(max_length=100, blank=True, null=True)
    customer_id = models.CharField(max_length=100, blank=True, null=True)
    customer_email = models.CharField(max_length=100000, blank=True, null=True)
    customer_name = models.CharField(max_length=100000, blank=True, null=True)
    price_id = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def update_subscription_info(self):
        try:
            # Retrieve subscription information from Stripe
            subscription = stripe.Subscription.retrieve(self.subscription_id)

            # Extract start and end dates
            start_timestamp = subscription.current_period_start
            end_timestamp = subscription.current_period_end

            # Convert timestamps to datetime objects
            self.start_date = datetime.utcfromtimestamp(start_timestamp)
            self.end_date = datetime.utcfromtimestamp(end_timestamp)

            # Update subscription status
            self.subscription_status = subscription.status

            # Check if the subscription is scheduled to be canceled
            if subscription.cancel_at is not None:
                self.subscription_cancel_status = True
                cancel_at_date = datetime.utcfromtimestamp(subscription.cancel_at).strftime('%Y-%m-%d %H:%M:%S UTC')
                self.subscription_cancel_status_text = f"Subscription is scheduled to be canceled on {cancel_at_date}"
            else:
                self.subscription_cancel_status = False
                self.subscription_cancel_status_text = "Subscription is not scheduled to be canceled."

            # Update customer information
            self.customer_id = subscription.customer

            items = subscription.get("items")
            for item in items.get("data", []):
                self.price_id = item.price.id

            price = stripe.Price.retrieve(self.price_id)
            amount = float(price.unit_amount_decimal) / 100  # Convert from cents to dollars

            # Retrieve product information if available
            product_name = None
            if price.product:
                product = stripe.Product.retrieve(price.product)
                product_name = product.name

            self.product_price = amount
            self.product_name = product_name

            customer = stripe.Customer.retrieve(self.customer_id)
            self.customer_email = customer.email
            self.customer_name = customer.name

            # Save the changes to the database
            self.save()

        except stripe.error.StripeError as e:
            # Handle Stripe API errors
            print(f"Stripe error while updating subscription info: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred while updating subscription info: {e}")

    def __str__(self):
        return f"{self.account}, {self.product_name}"
