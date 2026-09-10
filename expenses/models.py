from django.db import models

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("food", "Food"),
        ("transport", "Transport"),
        ("shopping", "Shopping"),
        ("health", "Health"),
        ("other", "Other"),
    ]
    description = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    spent_on = models.DateField()

    class Meta:
        ordering = ["-spent_on", "-id"]

    def __str__(self):
        return f"{self.description}: {self.amount}"

