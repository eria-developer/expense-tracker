from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Budget
from .forms import AddExpenseForm, EditExpenseForm, CustomUserCreationForm, setBudgetForm
from django.db.models import Sum, F, ExpressionWrapper, fields
from django.db.models.functions import TruncMonth
from datetime import timedelta, date
from django.contrib import messages
from django.contrib.auth import login
from django.http import JsonResponse
from django.core import serializers


from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from datetime import date, timedelta
from collections import OrderedDict

from datetime import datetime, timedelta
from django.utils import timezone

def chart_data(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=365)  # Get the date 1 year ago
    end_date = today + timedelta(days=1)  # Add 1 day to include today
    months = OrderedDict() 
    months = OrderedDict([(start_date.replace(day=1) + timedelta(days=(i * 30)), 0) for i in range(12)])

    data = Expense.objects.filter(date__gte=start_date, date__lt=end_date) \
                          .values('date__month') \
                          .annotate(total_expenses=Sum(F('quantity') * F('unit_amount'))) \
                          .order_by('date__month')

    for item in data:
        month = datetime(today.year, item['date__month'], 1)
        months[month] = item['total_expenses']

    # Extracting labels and values
    labels = [month.strftime('%b %Y') for month in months.keys()]
    values = list(months.values())

    return JsonResponse({'labels': labels, 'data': values})


# def chart_data(request):
#     today = timezone.now().date()
#     start_month = (today - timedelta(days=today.day - 1)).replace(day=1) - timedelta(days=1) 

#     data = Expense.objects.filter(date__gte=start_month) \
#                           .values('date__month') \
#                           .annotate(total_expenses=Sum(F('quantity') * F('unit_amount'))) \
#                           .order_by('date__month')

#     months = OrderedDict()  # Initialize empty OrderedDict
#     for item in data:
#         month = date(item['date__month'], 1, 1) 
#         months[month] = item['total_expenses'] 

#     # Extract labels and values
#     labels = [month.strftime('%b %Y') for month in months.keys()]
#     values = list(months.values())

#     return JsonResponse({'labels': labels, 'data': values})


def home(request):
    """manages the homepage"""
    budget = Budget.objects.all()

    recent_expenses = Expense.objects.order_by("-date")[:5]

    # Calculate the date 12 months ago from today
    twelve_months_ago = date.today() - timedelta(days=365)

    # Calculate total expenses for each month in the last 12 months
    expenses_by_month = Expense.objects.filter(date__gte=twelve_months_ago).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum(F('quantity') * F('unit_amount'))
    ).order_by('month')

    expenses_by_month_list = list(expenses_by_month)

    context = {
        "budget": budget,
        "expenses_by_month": expenses_by_month_list,
        "recent_expenses": recent_expenses,
    }
    return render(request, "home.html", context)

def add_expense(request):
    """handles adding new expense"""
    if request.method == "POST":
        form = AddExpenseForm(request.POST)
        if form.is_valid():
             print(form)
             form.save() 
             messages.success(request, "Expense added successfully!!")
             return redirect("expenses")
    else:
        form = AddExpenseForm()
        context = {
             "form": form,
        }
        return render(request, "expenses/add_expense.html", context)

    

def expenses(request):
    """handles display of expenses"""
    expenses = Expense.objects.annotate(expense_total_quantity=F("quantity") * F("unit_amount"))
    
    context = {
        "expenses": expenses,
    }

    return render(request, "expenses/expenses.html", context)


def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == "POST":
        form = EditExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!!")
            return redirect("expenses")
        else:
            context = {
                "form": form,
            }
            return render(request, "expenses/edit_expense.html", context)
    else:
        print(expense)
        form = EditExpenseForm(instance=expense)
        context = {
            "form": form,
        }

        return render(request, "expenses/edit_expense.html", context)
    

def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect("expenses")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        # print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have successfully loged in!!")
            return redirect("home")
    else:
        form = CustomUserCreationForm()
        context = {
            "form": form
        }
    return render(request, "expenses/signup.html", context)


def set_budget(request):
    if request.method == "POST":
        form = setBudgetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your monthly budget has been set successfully!!")
            return redirect("home")
    else:
        form = setBudgetForm()
        context = {
            "form": form,
        }
        return render(request, "expenses/setbudget.html", context)