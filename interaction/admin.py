from interaction.models import Transaction
from django.contrib import admin

# Register your models here.


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'merchantId')
    search_fields = ('id', 'create_date', 'merchantId')


admin.site.register(Transaction, TransactionAdmin)
