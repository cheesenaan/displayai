# Generated by Django 4.2.7 on 2024-02-10 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0028_freeplan"),
    ]

    operations = [
        migrations.AddField(
            model_name="freeplan",
            name="forms_remaining",
            field=models.IntegerField(default=5),
        ),
    ]
