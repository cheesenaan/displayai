# Generated by Django 4.2.7 on 2024-07-24 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0019_education_city_education_country_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="education",
            name="city",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="education",
            name="country",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]