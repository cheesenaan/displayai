# Generated by Django 4.2.7 on 2024-02-26 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0053_plan_subscription_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="subscription_id",
            field=models.CharField(blank=True, max_length=1000000),
        ),
    ]
