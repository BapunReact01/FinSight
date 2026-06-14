from django.contrib import admin
from .models import FinancialTransaction

@admin.register(FinancialTransaction)
class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = ('company', 'transaction_date', 'category', 'amount', 'transaction_type', 'created_at')
    list_filter = ('transaction_type', 'category', 'company', 'transaction_date')
    search_fields = ('category', 'description', 'company__company_name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'transaction_date'