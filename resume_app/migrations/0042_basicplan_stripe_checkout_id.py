# Generated by Django 4.2.7 on 2024-02-15 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0041_alter_freeplan_forms_remaining_basicplan"),
    ]

    operations = [
        migrations.AddField(
            model_name="basicplan",
            name="stripe_checkout_id",
            field=models.CharField(default=None, max_length=500),
        ),
    ]
