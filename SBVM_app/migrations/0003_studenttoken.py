# Generated by Django 5.1.7 on 2025-06-19 05:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SBVM_app', '0002_student_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100, unique=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='SBVM_app.student')),
            ],
        ),
    ]
