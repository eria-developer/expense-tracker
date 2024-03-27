from django.db import models
from datetime import date

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("Food", "Food"),
        ("Housing", "Housing"),
        ("Transportation", "Transportation"),
        ("Health", "Health"),
        ("Entertainment", "Entertainment"),
        ("Other", "Other"),
    ]
    name = models.CharField(max_length=100, null=False, blank=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.DecimalField(max_digits=15, decimal_places=2)
    unit_amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.name.title()} Qnt: {self.quantity} UnitAmount: {self.unit_amount}"