from django.db import models

# Create your models here.

class APICalls(models.Model) :
    hospital_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    api_url = models.CharField(null=False, blank=False, max_length=500)

    def __str__(self):
        return (self.hospital_name)
