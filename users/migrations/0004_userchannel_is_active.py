# Generated by Django 4.2.7 on 2023-12-02 09:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_userchannel"),
    ]

    operations = [
        migrations.AddField(
            model_name="userchannel",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]