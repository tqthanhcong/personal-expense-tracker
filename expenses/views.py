from django.db.models import Sum
from django.shortcuts import redirect, render
from .forms import ExpenseForm
from .models import Expense

def expense_list(request):
    selected_category = request.GET.get("category", "")
    expenses = Expense.objects.all()
    if selected_category:
        expenses = expenses.filter(category=selected_category)
    total = expenses.aggregate(total=Sum("amount"))["total"] or 0
    form = ExpenseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("expense-list")
    return render(request, "expenses/expense_list.html", {
        "expenses": expenses,
        "form": form,
        "total": total,
        "categories": Expense.CATEGORY_CHOICES,
        "selected_category": selected_category,
    })

