import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("a, b, expected",[(1,2,3),(4,5,9),(9,10,19)])
def test_add(a, b, expected):
    assert add(a,b) == expected

def test_subtract():
    assert subtract(3,5) == -2

def test_multiply():
    assert multiply(3,5) == 15

def test_divide():
    assert divide(6,3) == 2


def test_bank_ac_init(bank_account):
    assert bank_account.balance == 50

def test_bank_ac_default(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_interect(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,5) == 55

@pytest.mark.parametrize("dep, withd, expected",[(3,2,1),(200,100,100),(10000,1,9999),(55555,5,55550)])
def test_stuff(zero_bank_account, dep, withd, expected):
    zero_bank_account.deposit(dep)
    zero_bank_account.withdraw(withd)
    assert zero_bank_account.balance == expected