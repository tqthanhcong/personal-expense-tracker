import os
os.environ["DATABASE_URL"] = "sqlite:///./test_spliteasy.db"

from fastapi.testclient import TestClient
from app.database import Base, engine
from app.main import app

client = TestClient(app)

def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def teardown_module():
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test_spliteasy.db"):
        os.remove("test_spliteasy.db")

def add_person(name):
    response = client.post("/people", json={"name": name})
    assert response.status_code == 201
    return response.json()["id"]

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_people_reject_duplicates():
    add_person("An")
    assert client.post("/people", json={"name": "An"}).status_code == 409

def test_expense_and_summary():
    an = add_person("An"); binh = add_person("Binh")
    response = client.post("/expenses", json={"description":"Dinner", "amount":100, "payer_id":an, "participant_ids":[an, binh]})
    assert response.status_code == 201
    assert len(client.get("/expenses").json()) == 1
    summary = client.get("/summary").json()
    assert summary["balances"] == [{"person_id":an,"name":"An","balance":50.0},{"person_id":binh,"name":"Binh","balance":-50.0}]
    assert summary["settlements"] == [{"from_name":"Binh","to_name":"An","amount":50.0}]

