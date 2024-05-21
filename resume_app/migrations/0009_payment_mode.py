# Generated by Django 4.2.7 on 2024-05-12 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0008_alter_account_user_alter_payment_account_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="mode",
            field=models.CharField(
                choices=[("payment", "Payment"), ("subscription", "Subscription")],
                default="payment",
                max_length=20,
            ),
        ),
    ]