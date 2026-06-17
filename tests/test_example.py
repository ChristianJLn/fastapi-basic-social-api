""" import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("x, y, expected", [
                         (3, 2, 5),
                         (10, 10 , 20),
                         (1, 1, 2)])
def test_something(x, y, expected):
    assert x + y == expected

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_inefficient_funds(zero_bank_account):
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(200) """