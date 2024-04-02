from django.forms import ModelForm
from .models import Expense,CustomUser,Budget
from django.contrib.auth.forms import UserCreationForm

class AddExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"


class EditExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["username", "email", "minimum_salary"]

class setBudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = "__all__"