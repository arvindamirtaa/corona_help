from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import EmailMultiAlternatives
from django.db import models

from .vars import CATEGORY_CHOICES, ORG_TYPE_CHOICES


class UserManager(BaseUserManager):
    """ Manager class for the custom User model"""

    def create_user(self, email, password=None, is_active=True, is_admin=False,
                    is_staff=False):
        """Create a new User object, validate fields and save"""
        if not email:
            raise ValueError("Email field cannot be empty")
        if not password:
            raise ValueError("Password field cannot be empty")
        user_object = self.model(
            email=self.normalize_email(email)
        )
        user_object.set_password(password)
        user_object.is_active = is_active
        user_object.staff = is_staff
        user_object.admin = is_admin
        user_object.save(using=self._db)
        return user_object

    def create_staff_user(self, email, password=None):
        """ Set staff flag to true"""
        user = self.create_user(email, password=password, is_staff=True)
        return user

    def create_superuser(self, email, password=None):
        """ Set superuser flag to true"""
        user = self.create_user(email, password=password,
                                is_admin=True, is_staff=True)
        return user


# Custom User Model
class User(AbstractBaseUser):
    """Class that represents Users, extends AbstractBaseUser"""
    email = models.EmailField(max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)  # can login
    staff = models.BooleanField(default=False)  # Staff, non super user
    admin = models.BooleanField(default=False)  # Super User
    email_confirmed = models.BooleanField(
        default=False)  # Email One Time Link Confirmation
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # For later

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

    def email_user(self, subject, text_message, html_message,
                   from_email=None, **kwargs):
        msg = EmailMultiAlternatives(
            subject, text_message, from_email, [self.email])
        msg.attach_alternative(html_message, "text/html")
        msg.send()

    def set_active(self):
        self.is_active = True
        self.save()

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def active(self):
        return self.is_active

    def __unicode__(self):
        return self.email


class OrganisationProfile(models.Model):
    # TODO Add FK to User model.
    name = models.CharField(max_length=200)
    description = models.TextField()
    website = models.URLField()
    category = models.IntegerField(choices=ORG_TYPE_CHOICES)
    address = models.CharField(max_length=200)
    # TODO Use django-cities to select City from list.
    city = models.CharField(max_length=40)
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=200)


class Requirement(models.Model):
    organisation = models.ForeignKey(
        OrganisationProfile, related_name='requirements', on_delete=models.CASCADE)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    what = models.TextField()
    why = models.TextField()
    # TODO Configure static & media files and change to FileField.
    supporting_document = models.URLField()


class Resource(models.Model):
    organisation = models.ForeignKey(
        OrganisationProfile, related_name='resources', on_delete=models.CASCADE)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    description = models.TextField()
    availability = models.TextField()
    eligibility = models.TextField()
    # TODO Configure static & media files and change to FileField.
    supporting_document = models.URLField()


class UserInvitation(models.Model):
    """ Class represents invitations sent for users to sign up."""
    inviting_user = models.ForeignKey(
        OrganisationProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_invited = models.DateTimeField(auto_now_add=True)
    invitation_accepted = models.BooleanField(default=False)
