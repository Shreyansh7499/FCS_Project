from django.contrib import admin
from .models import Wallet,Transaction,Add_Money_Transaction,Transaction_Log

admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Transaction_Log)
admin.site.register(Add_Money_Transaction)