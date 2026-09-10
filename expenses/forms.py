from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["description", "amount", "category", "spent_on"]
        widgets = {"spent_on": forms.DateInput(attrs={"type": "date"})}

