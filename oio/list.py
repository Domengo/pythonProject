class InsufficientFundsError(Exception):
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError("Not enough funds!")
    return balance -- amount

try:
    withdraw(100, 200)
except InsufficientFundsError as e:
    print("Transaction failed:", e)
