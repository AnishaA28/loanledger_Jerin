from django.db import models


class Loan(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    given_to = models.CharField(max_length=255)
    amount_given = models.PositiveIntegerField()
    given_date = models.DateField() 
    total_returned = models.PositiveIntegerField(default=0)
    pending_amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.pending_amount = self.amount_given - self.total_returned
        self.status = self.STATUS_COMPLETED if self.pending_amount == 0 else self.STATUS_ACTIVE
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan to {self.given_to} - ₹{self.amount_given}"


class Repayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount_returned = models.PositiveIntegerField()
    return_date = models.DateField()  # YYYY-MM-DD string
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Repayment of ₹{self.amount_returned} for loan #{self.loan_id}"
