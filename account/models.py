from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _                              # import translation package for different languages
from django_countries.fields import CountryField


class CustomAccountManager(BaseUserManager):
    """
    custom account manager class called CustomAccountManager.
    This class extends the BaseUserManager class, it is a custom manager for user accounts.
    """
    def create_superuser(self, email, user_name, password, **other_fields):
        """
        for superuser account
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):
        """
        for regular user account
        """
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)                                         # normalize_email to convert the email to lowercase and normalizes the domain
        user = self.model(email=email, user_name=user_name, **other_fields)         # the model attribute refers to the user model associated with the account manager
        user.set_password(password)                                                 # securely hashes the password
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    """
    extends two Django built-in classes: AbstractBaseUser and PermissionsMixin
    """
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(_('about'), max_length=500, blank=True)

    # Delivery details
    country = CountryField()                                                            # from the django-countries package to store the user's country
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)

    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()                                                    # allows the custom manager to be used for managing user accounts.

    USERNAME_FIELD = 'email'                                                            # specifies the field used as the unique identifier for the user model, which is the email field in this case
    REQUIRED_FIELDS = ['user_name']                                                     # lists the additional fields that are required when creating a user account. In this case, the user_name field is required

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        """
        custom method that can be used to send an email to the user
        """
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.user_name
