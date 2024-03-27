from django.shortcuts import render, redirect
from .models import Expense

def home(request):
    """manages the homepage"""
    return render(request, "home.html")

def add_expense(request):
    """handles adding new expense"""
    if request.method == "POST":
        # getting values from the form 
        name = request.POST.get("name")
        category = request.POST.get("category")
        quantity = request.POST.get("quantity")
        unit_amount = request.POST.get("unit_amount")
        date = request.POST.get("date")

        # saving the values into expense variable
        expense = Expense(name=name, category=category, quantity=quantity, unit_amount=unit_amount, date=date)

        # if form not valid, we render it back with its data preserved
        if not expense.clean():
            return render(request, "expenses/add_expense.html", {"form_data": request.POST})
        
        # if the form is valid, we save it 
        expense.save()
        return redirect()
    else:
        return render(request, "expenses/add_expense.html")