from django.db import models

# Create your models here.

class DNSLog(models.Model):
    source_ip = models.CharField(max_length=100)
    content = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content