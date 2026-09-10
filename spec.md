# Personal Expense Tracker Specification

## Goal
Build a small Django web application that lets one user record and review personal expenses.

## Features
1. Add an expense with description, amount, category, and date.
2. View all expenses in reverse chronological order.
3. Filter the expense list by category.
4. Display the total amount for the current list or selected category.

## Out of scope
Authentication, editing, deleting, budgets, recurring expenses, and charts.

## Acceptance criteria
- Valid form submissions create a persistent expense and redirect to the list.
- The default page lists every saved expense.
- Choosing a category shows only matching expenses.
- The displayed total equals the sum of the currently visible expenses.

