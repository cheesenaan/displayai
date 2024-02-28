# Generated by Django 4.2.7 on 2024-02-26 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0055_alter_plan_subscription_id"),
    ]

    operations = [
        migrations.RemoveField(model_name="plan", name="subscription_id",),
        migrations.AddField(
            model_name="plan",
            name="subscription_ids",
            field=models.CharField(
                blank=True,
                help_text="subscription_ids seperated by commas",
                max_length=100000,
                null=True,
            ),
        ),
    ]
