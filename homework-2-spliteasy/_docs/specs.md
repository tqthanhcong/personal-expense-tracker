# SplitEasy Product Specification

## Goal
Help a small group record shared expenses and see the simplest current settlement summary.

## User stories
- As a user, I can add people to a group.
- As a user, I can record an expense with a payer, amount, description, and participants.
- As a user, I can see all recorded expenses.
- As a user, I can see each person's net balance and suggested payments.

## Acceptance criteria
- A person with a non-empty unique name can be added.
- An expense must have a positive amount, one payer, and at least one participant.
- The expense amount is split equally between its selected participants.
- Balances always sum to zero, allowing for cent-level rounding.
- Data remains available after the backend restarts.

## Non-goals
Authentication, multiple groups, unequal splits, multiple currencies, payment processing, and real-time collaboration.

