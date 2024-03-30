from django.shortcuts import render, redirect
from .models import Expense
from .forms import AddExpenseForm

def home(request):
    """manages the homepage"""
    return render(request, "home.html")

def add_expense(request):
    """handles adding new expense"""
    if request.method == "POST":
        form = AddExpenseForm(request.POST)
        if form.is_valid():
             print(form)
             form.save() 
             return redirect("expenses")
    else:
        form = AddExpenseForm()
        context = {
             "form": form,
        }
        return render(request, "expenses/add_expense.html", context)

    

def expenses(request):
    """handles display of expenses"""
    expenses = Expense.objects.all()
    context = {
        "expenses": expenses,
    }

    return render(request, "expenses/expenses.html", context)