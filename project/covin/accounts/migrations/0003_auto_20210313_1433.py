# Generated by Django 3.1.6 on 2021-03-13 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('accounts', '0002_personalinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.user')),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('year_of_birth', models.CharField(max_length=20, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=200, null=True)),
                ('mobile_no', models.CharField(max_length=200, null=True)),
                ('dose1_status', models.CharField(choices=[('Sheduled', 'Sheduled'), ('Not-Sheduled', 'Not-Sheduled'), ('Vaccinated', 'Vaccinated')], max_length=200, null=True)),
                ('dose2_status', models.CharField(choices=[('Sheduled', 'Sheduled'), ('Not-Sheduled', 'Not-Sheduled'), ('Vaccinated', 'Vaccinated')], max_length=200, null=True)),
                ('chronic_health_condition', models.TextField(blank=True, null=True)),
                ('current_medicine', models.CharField(max_length=300)),
                ('allergies', models.CharField(max_length=300)),
                ('diagonised_with_covid', models.BooleanField()),
                ('diagonised_further_detail', models.TextField(blank=True, null=True)),
                ('accurate_information', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('accounts.user',),
        ),
        migrations.DeleteModel(
            name='PersonalInfo',
        ),
    ]