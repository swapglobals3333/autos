from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100, unique=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.DurationField(help_text="Estimated time to complete the service")

    def __str__(self):
        return self.name