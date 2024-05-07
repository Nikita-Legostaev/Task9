from django.db import models


class CheckedFile(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    pep8_compliant = models.BooleanField(default=False)
