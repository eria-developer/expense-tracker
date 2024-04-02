from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import AddExpenseForm, EditExpenseForm, CustomUserCreationForm
from django.db.models import F
from django.contrib import messages
from django.contrib.auth import login


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