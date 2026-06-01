from auth.utils import hash_password, verify_password
import pytest

@pytest.fixture
def hashed_password():
    return hash_password("secret123")

def test_verify_password_accepts_correct_password(hashed_password):
    # hashed = hash_password("secret123")
    assert verify_password("secret123", hashed_password) is True


def test_verify_password_rejects_wrong_password():
    hashed = hash_password("secret123")
    assert verify_password("wrong-pass", hashed) is False