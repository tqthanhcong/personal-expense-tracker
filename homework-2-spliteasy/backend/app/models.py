from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

expense_participants = Table(
    "expense_participants", Base.metadata,
    Column("expense_id", ForeignKey("expenses.id", ondelete="CASCADE"), primary_key=True),
    Column("person_id", ForeignKey("people.id", ondelete="CASCADE"), primary_key=True),
)

class Person(Base):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)

class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(120))
    amount: Mapped[float] = mapped_column(Float)
    payer_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    payer: Mapped[Person] = relationship(foreign_keys=[payer_id])
    participants: Mapped[list[Person]] = relationship(secondary=expense_participants)

