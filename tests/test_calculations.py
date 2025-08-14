import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount

@pytest.mark.parametrize("a, b, expected",[(1,2,3),(4,5,9),(9,10,19)])
def test_add(a, b, expected):
    assert add(a,b) == expected

def test_subtract():
    assert subtract(3,5) == -2

def test_multiply():
    assert multiply(3,5) == 15

def test_divide():
    assert divide(6,3) == 2


def test_bank_ac_init():
    joe = BankAccount(50)
    assert joe.balance == 50

def test_bank_ac_default():
    joe = BankAccount()
    assert joe.balance == 0

def test_withdraw():
    joe = BankAccount(50)
    joe.withdraw(20)
    assert joe.balance == 30

def test_deposit():
    joe = BankAccount(50)
    joe.deposit(30)
    assert joe.balance == 80

def test_collect_interect():
    joe = BankAccount(50)
    joe.collect_interest()
    assert round(joe.balance,5) == 55
