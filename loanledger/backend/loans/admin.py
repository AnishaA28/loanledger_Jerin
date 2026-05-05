from django.contrib import admin
from .models import Loan, Repayment


class RepaymentInline(admin.TabularInline):
    model = Repayment
    extra = 0


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'given_to', 'amount_given', 'total_returned', 'pending_amount', 'status')
    search_fields = ('given_to',)
    list_filter = ('status',)
    inlines = [RepaymentInline]


@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan', 'amount_returned', 'return_date')
    search_fields = ('loan__given_to',)