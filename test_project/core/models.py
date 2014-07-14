from django.db import models


class ModelMockup(models.Model):

    name = models.CharField(max_length=20)
