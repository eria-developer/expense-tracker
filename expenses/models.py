from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    minimum_salary = models.IntegerField(blank=True, null=True)

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
    

class Budget(models.Model):
    budget = models.IntegerField()

    def __str__(self):
        return f"Current Budget: {self.budget}"