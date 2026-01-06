import pytest
from app.services.categorizer import suggest_category

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
    
def test_suggest_category():
    db = MockDB()
    result = suggest_category("Spotify family plan", db)
    assert result["category_id"] == 1
    assert result["category_name"] == "Subscription"