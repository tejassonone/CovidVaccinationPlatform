from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
                email,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
                email,
                password=password,
                is_staff=True,
                is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True)
    # full_name   = models.CharField(max_length=255, blank=True, null=True)
    active      = models.BooleanField(default=True) # can login 
    staff       = models.BooleanField(default=False) # staff user non superuser
    admin       = models.BooleanField(default=False) # superuser 
    timestamp   = models.DateTimeField(auto_now_add=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email' #username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = [] #['full_name'] #python manage.py createsuperuser



    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active




class PersonalInfo(User):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )

    DOSE_STATUS = (
        ('Sheduled', 'Sheduled'),
        ('Not-Sheduled', 'Not-Sheduled'),
        ('Vaccinated', 'Vaccinated')
    )
    
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    year_of_birth = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    mobile_no = models.CharField(max_length=200, null=True)
    dose1_status = models.CharField(max_length=200, null=True, choices=DOSE_STATUS)
    dose2_status = models.CharField(max_length=200, null=True, choices=DOSE_STATUS)


    class Meta:
        abstract = True


class Beneficiary(PersonalInfo):
    chronic_health_condition = models.TextField(blank=True, null=True)
    current_medicine = models.CharField(max_length=300)
    allergies = models.CharField(max_length=300)
    diagonised_with_covid = models.BooleanField()
    diagonised_further_detail = models.TextField(blank=True, null=True)
    accurate_information = models.BooleanField(default=False)





