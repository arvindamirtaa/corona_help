from django.db import models


# Create your models here.
class Organisation(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    description = models.TextField()
    name_of_contact = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=200)
    city = models.CharField(max_length=40)


class AskingOrg(Organisation):
    work_description = models.TextField()
    requirements = models.TextField()


class HelpingOrg(Organisation):
    resource_description = models.TextField()
