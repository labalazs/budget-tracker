import pytest
from app.services.learning import extract_candidate_keyword

@pytest.mark.parametrize(
    "description,expected",
    [
        ("Spotify subscriptien December", "spotify"),
        ("Tesco weekly shopping", "tesco"),
        ("12/2025 electricity bill", "electricity"),
        ("ab cd ef gh", None),
    ],
)
def test_extract_candidate_keyword(description, expected):
    assert extract_candidate_keyword(description=description) == expected