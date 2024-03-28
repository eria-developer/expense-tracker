from django.shortcuts import render, redirect
from .models import Expense

def home(request):
    """manages the homepage"""
    return render(request, "home.html")

def add_expense(request):
    """handles adding new expense"""
    errors = {}
    category_choices = Expense.CATEGORY_CHOICES
    if request.method == "POST":
        # getting values from the form 
        name = request.POST.get("name")
        category = request.POST.get("category")
        quantity = request.POST.get("quantity")
        unit_amount = request.POST.get("unit_amount")
        date = request.POST.get("date")

        # manual validation of the form 
        if not name:
            errors["name"] = "Please insert the expense name!"
        if not category:
            errors["category"] = "Please insert the expense category!"
        if not quantity:
            errors["quantity"] = "Please insert the expense quantity!"
        if not unit_amount:
            errors["unit_amount"] = "Please insert the expense unit_amount!"

        if not errors:
        # saving the values into expense variable
            expense = Expense(name=name, category=category, quantity=quantity, unit_amount=unit_amount, date=date)

            context = {
                "form_data": request.POST,
                "category_choices": category_choices,
                "errors": errors,
            }
            # if form not valid, we render it back with its data preserved
            if not expense.clean():
                return render(request, "expenses/add_expense.html", context)
            
            # if the form is valid, we save it 
            expense.save()
            return redirect()
    else:
        context = {
            "category_choices": category_choices,
        }
        return render(request, "expenses/add_expense.html", context)