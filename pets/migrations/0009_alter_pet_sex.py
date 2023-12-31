# Generated by Django 4.2.4 on 2023-08-04 19:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0008_alter_pet_group_alter_pet_sex"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="sex",
            field=models.CharField(
                choices=[
                    ("Male", "Male"),
                    ("Female", "Female"),
                    ("Not Informed", "Default"),
                ],
                default="Not Informed",
                max_length=20,
            ),
        ),
    ]
