from django.contrib import admin

# Register your models here.
from .models import LipaNaMpesaOnline


class LipaNaMpesaOnlineAdmin(admin.ModelAdmin):
    list_display = ("PhoneNumber", "Amount", "MpesaReceiptNumber", "TransactionDate")

admin.site.register(LipaNaMpesaOnline,LipaNaMpesaOnlineAdmin)


