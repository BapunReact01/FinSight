from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'companies'
    
    def __str__(self):
        return self.company_name