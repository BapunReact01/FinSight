from django.db import models
from companies.models import Company

class FinancialTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'financial_transactions'
    
    def __str__(self):
        return f"{self.company.company_name} - {self.category} - {self.amount}"