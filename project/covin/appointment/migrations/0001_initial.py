# Generated by Django 3.1.6 on 2021-03-17 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('centre_id', models.CharField(max_length=50)),
                ('centre_name', models.CharField(max_length=200)),
                ('state_name', models.CharField(max_length=200)),
                ('district_name', models.CharField(max_length=200)),
                ('block_name', models.CharField(max_length=200)),
                ('pincode', models.CharField(max_length=10)),
                ('dose', models.CharField(max_length=2)),
                ('appointment_id', models.CharField(max_length=20)),
                ('session_date', models.CharField(max_length=20)),
                ('slot', models.CharField(max_length=50)),
            ],
        ),
    ]
