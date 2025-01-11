from django.db import models

# Create your models here.
class Candidate(models.Model):
    name = models.CharField(max_length=100, default="default name")
    email = models.EmailField(max_length=500, default="def@mail.com")
    phone = models.CharField(max_length=100, default="9999999")
    file = models.FileField(upload_to="resumes/", max_length=1000)
    def __str__(self):
        return self.name