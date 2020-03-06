from django.db import models

from .vars import ORG_TYPE_CHOICES

# Create your models here.


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
        OrganisationProfile, related_name='requirements')
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    what = models.TextField()
    why = models.TextField()
    # TODO Configure static & media files and change to FileField.
    supporting_document = models.URLField()


class Resource(models.Model):
    organisation = models.ForeignKey(
        OrganisationProfile, related_name='resources')
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    description = models.TextField()
    availability = models.TextField()
    eligibility = models.TextField()
    # TODO Configure static & media files and change to FileField.
    supporting_document = models.URLField()
