class Transaction:
    def __init__(self, t, a, b):
        self.t = t        # type
        self.a = a        # amount
        self.b = b        # balance after transaction

    def __str__(self):
        return f"{self.t} | Amount: {self.a} | Balance: {self.b}"
    

from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, bal):
        self._bal = bal
        self._tx = []

    @abstractmethod
    def withdraw(self, a):
        pass

    def deposit(self, a):
        self._bal += a
        self._tx.append(Transaction("Deposit", a, self._bal))

    def balance(self):
        return self._bal

    def history(self):
        for t in self._tx:
            print(t)
class SavingsAccount(Account):
    def __init__(self, bal):
        super().__init__(bal)
        self._limit = 5000

    def withdraw(self, a):
        if a > self._limit:
            raise ValueError("Daily limit exceeded")
        if a > self._bal:
            raise ValueError("Insufficient balance")

        self._bal -= a
        self._tx.append(Transaction("Withdraw", a, self._bal))

    def add_interest(self):
        i = self._bal * 0.04
        self._bal += i
        self._tx.append(Transaction("Interest", i, self._bal))
class CurrentAccount(Account):
    def withdraw(self, a):
        self._bal -= a
        self._tx.append(Transaction("Withdraw", a, self._bal))
class Bank(ABC):
    def __init__(self, pin, acc):
        self._pin = pin
        self._acc = acc

    def auth(self, p):
        if p != self._pin:
            raise ValueError("Wrong PIN")

    def withdraw(self, a):
        self._acc.withdraw(a)

    def deposit(self, a):
        self._acc.deposit(a)

    def balance(self):
        return self._acc.balance()

    def history(self):
        self._acc.history()
class SBI(Bank):
    pass

class HDFC(Bank):
    pass
def atm(b):
    try:
        p = int(input("Enter PIN: "))
        b.auth(p)
    except ValueError as e:
        print(e)
        return

    while True:
        print("\n1.Balance 2.Withdraw 3.Deposit 4.History 5.Exit")
        c = int(input("Choice: "))

        try:
            if c == 1:
                print("Balance:", b.balance())
            elif c == 2:
                a = int(input("Amount: "))
                b.withdraw(a)
            elif c == 3:
                a = int(input("Amount: "))
                b.deposit(a)
            elif c == 4:
                b.history()
            elif c == 5:
                break
        except ValueError as e:
            print(e)
print("1.SBI Savings  2.HDFC Current")
c = int(input("Choice: "))

if c == 1:
    acc = SavingsAccount(10000)
    bank = SBI(1234, acc)
elif c == 2:
    acc = CurrentAccount(20000)
    bank = HDFC(5678, acc)
else:
    exit()

atm(bank)
