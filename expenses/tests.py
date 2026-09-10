from datetime import date
from django.test import TestCase
from django.urls import reverse
from .models import Expense

class ExpenseTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("expense-list"))
        self.assertEqual(response.status_code, 200)

    def test_create_expense(self):
        response = self.client.post(reverse("expense-list"), {
            "description": "Lunch", "amount": "75000",
            "category": "food", "spent_on": "2026-09-10",
        })
        self.assertRedirects(response, reverse("expense-list"))
        self.assertEqual(Expense.objects.count(), 1)

    def test_filter_and_total(self):
        Expense.objects.create(description="Lunch", amount=75000, category="food", spent_on=date(2026, 9, 10))
        Expense.objects.create(description="Taxi", amount=100000, category="transport", spent_on=date(2026, 9, 9))
        response = self.client.get(reverse("expense-list"), {"category": "food"})
        self.assertContains(response, "Lunch")
        self.assertNotContains(response, "Taxi")
        self.assertEqual(response.context["total"], 75000)

