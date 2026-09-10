from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from .database import Base, engine, get_db
from .models import Expense, Person
from .schemas import ExpenseCreate, ExpenseOut, PersonCreate, PersonOut, SummaryOut

Base.metadata.create_all(bind=engine)
app = FastAPI(title="SplitEasy API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/people", response_model=list[PersonOut])
def list_people(db: Session = Depends(get_db)):
    return db.scalars(select(Person).order_by(Person.id)).all()

@app.post("/people", response_model=PersonOut, status_code=201)
def add_person(payload: PersonCreate, db: Session = Depends(get_db)):
    person = Person(name=payload.name.strip())
    if not person.name:
        raise HTTPException(422, "Name cannot be blank")
    db.add(person)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Name already exists")
    db.refresh(person)
    return person

@app.get("/expenses", response_model=list[ExpenseOut])
def list_expenses(db: Session = Depends(get_db)):
    query = select(Expense).options(selectinload(Expense.payer), selectinload(Expense.participants)).order_by(Expense.id.desc())
    return db.scalars(query).all()

@app.post("/expenses", response_model=ExpenseOut, status_code=201)
def add_expense(payload: ExpenseCreate, db: Session = Depends(get_db)):
    ids = list(dict.fromkeys(payload.participant_ids))
    people = db.scalars(select(Person).where(Person.id.in_(ids))).all()
    payer = db.get(Person, payload.payer_id)
    if payer is None or len(people) != len(ids):
        raise HTTPException(404, "Payer or participant not found")
    expense = Expense(description=payload.description.strip(), amount=payload.amount, payer=payer, participants=people)
    db.add(expense); db.commit(); db.refresh(expense)
    return db.scalar(select(Expense).options(selectinload(Expense.payer), selectinload(Expense.participants)).where(Expense.id == expense.id))

@app.get("/summary", response_model=SummaryOut)
def summary(db: Session = Depends(get_db)):
    people = db.scalars(select(Person).order_by(Person.id)).all()
    expenses = db.scalars(select(Expense).options(selectinload(Expense.payer), selectinload(Expense.participants))).all()
    balances = {p.id: 0.0 for p in people}
    names = {p.id: p.name for p in people}
    for expense in expenses:
        share = expense.amount / len(expense.participants)
        balances[expense.payer_id] += expense.amount
        for participant in expense.participants:
            balances[participant.id] -= share
    creditors = [[pid, value] for pid, value in balances.items() if value > 0.005]
    debtors = [[pid, -value] for pid, value in balances.items() if value < -0.005]
    settlements = []
    i = j = 0
    while i < len(debtors) and j < len(creditors):
        amount = min(debtors[i][1], creditors[j][1])
        settlements.append({"from_name": names[debtors[i][0]], "to_name": names[creditors[j][0]], "amount": round(amount, 2)})
        debtors[i][1] -= amount; creditors[j][1] -= amount
        if debtors[i][1] < 0.005: i += 1
        if creditors[j][1] < 0.005: j += 1
    return {"balances": [{"person_id": p.id, "name": p.name, "balance": round(balances[p.id], 2)} for p in people], "settlements": settlements}

