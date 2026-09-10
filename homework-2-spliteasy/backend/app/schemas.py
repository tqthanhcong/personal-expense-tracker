from pydantic import BaseModel, Field

class PersonCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)

class PersonOut(PersonCreate):
    id: int
    model_config = {"from_attributes": True}

class ExpenseCreate(BaseModel):
    description: str = Field(min_length=1, max_length=120)
    amount: float = Field(gt=0)
    payer_id: int
    participant_ids: list[int] = Field(min_length=1)

class ExpenseOut(BaseModel):
    id: int
    description: str
    amount: float
    payer: PersonOut
    participants: list[PersonOut]
    model_config = {"from_attributes": True}

class BalanceOut(BaseModel):
    person_id: int
    name: str
    balance: float

class SettlementOut(BaseModel):
    from_name: str
    to_name: str
    amount: float

class SummaryOut(BaseModel):
    balances: list[BalanceOut]
    settlements: list[SettlementOut]

