from app.database import get_db
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class MockKeyword:
    def __init__(self, keyword, category_id, category_name):
        self.keyword = keyword
        self.category_id = category_id
        self.category = type("Category", (), {"name": category_name})

class MockDB:
    def query(self, model):
        return self
    
    def join(self, *args, **kwargs):
        return self
    
    def filter(self, *args, **kwargs):
        return self
    
    def all(self):
        return [
            MockKeyword("spotify", 1, "Subscription"),
            MockKeyword("lidl", 2, "Croceries"),
        ]
    
def override_get_db():
    yield MockDB()

app.dependency_overrides[get_db] = override_get_db

def test_autocategorize_endpoint():
    response = client.post("/categorize/", json={"description": "Spotify family plan"})
    assert response.status_code == 200
    data = response.json()
    assert data["category_id"] == 1
    assert data["category_name"] == "Subscription"