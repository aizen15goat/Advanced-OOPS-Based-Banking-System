from abc import ABC, abstractmethod

class Transaction:
    def __init__(self, t, a, b):
        self.t = t
        self.a = a
        self.b = b

    def __str__(self):
        return f"{self.t} | Amount: {self.a} | Balance: {self.b}"


class Account(ABC):
    def __init__(self, bal):
        self._bal = bal
        self._tx = []

    @abstractmethod
    def withdraw(self, a):
        pass

    def deposit(self, a):
        if a <= 0:
            raise ValueError("Deposit must be positive")
        self._bal += a
        self._tx.append(Transaction("Deposit", a, self._bal))

    def balance(self):
        return self._bal

    def history(self):
        if not self._tx:
            print("No transactions yet.")
        for t in self._tx:
            print(t)


class SavingsAccount(Account):
    def __init__(self, bal):
        super().__init__(bal)
        self._limit = 5000
        self._min_balance = 2000

    def withdraw(self, a):
        if a > self._limit:
            raise ValueError("Daily withdrawal limit exceeded")
        if self._bal - a < self._min_balance:
            raise ValueError("Minimum balance of 2000 must be maintained")
        self._bal -= a
        self._tx.append(Transaction("Withdraw", a, self._bal))

class CurrentAccount(Account):
    def withdraw(self, a):
        if a > self._bal:
            raise ValueError("Insufficient balance")
        self._bal -= a
        self._tx.append(Transaction("Withdraw", a, self._bal))


class Bank(ABC):
    def __init__(self, pin, acc):
        self._pin = pin
        self._acc = acc
        self._blocked = False
        self._pin_attempts = 0

    def auth(self, p):
        if self._blocked:
            raise ValueError("Card is blocked. Visit your bank.")

        if p != self._pin:
            self._pin_attempts += 1
            if self._pin_attempts >= 3:
                self._blocked = True
                raise ValueError("Card blocked due to 3 wrong PIN attempts")
            raise ValueError("Wrong PIN")

        self._pin_attempts = 0

    def change_pin(self, old_pin, new_pin):
        if self._blocked:
            raise ValueError("Card is blocked. Visit your bank.")

        if old_pin != self._pin:
            self._pin_attempts += 1
            if self._pin_attempts >= 3:
                self._blocked = True
                raise ValueError("Card blocked due to 3 wrong PIN attempts")
            raise ValueError("Old PIN is incorrect")

        if len(str(new_pin)) != 4:
            raise ValueError("PIN must be exactly 4 digits")

        self._pin = new_pin
        self._pin_attempts = 0
        print("PIN changed successfully")

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
    while True:
        print("\nATM Menu:")
        print("1. Balance  2. Withdraw  3. Deposit  4. History  5. Exit  6. Change PIN")

        try:
            choice = int(input("Enter your choice (1-6): "))

            if choice == 1:
                print("Balance:", b.balance())

            elif choice == 2:
                amount = float(input("Enter amount to withdraw: "))
                b.withdraw(amount)
                print("Withdrawal successful")

            elif choice == 3:
                amount = float(input("Enter amount to deposit: "))
                b.deposit(amount)
                print("Deposit successful")

            elif choice == 4:
                print("Transaction History:")
                b.history()

            elif choice == 6:
                old = int(input("Enter current PIN: "))
                new = int(input("Enter new 4-digit PIN: "))
                b.change_pin(old, new)

            elif choice == 5:
                print("Thank you for using the ATM!")
                break

            else:
                print("Invalid choice. Enter 1-6 only.")

        except ValueError as e:
            print("Error:", e)
            if "blocked" in str(e):
                break


print("Welcome to the ATM!")

bank_attempts = 0
while bank_attempts < 4:
    print("\nSelect your bank:")
    print("1. SBI Savings  2. HDFC Current")

    try:
        bank_choice = int(input("Enter choice (1 or 2): "))

        if bank_choice == 1:
            account = SavingsAccount(10000)
            bank = SBI(1234, account)
            break
        elif bank_choice == 2:
            account = CurrentAccount(20000)
            bank = HDFC(5678, account)
            break
        else:
            bank_attempts += 1
            print("Invalid choice. Attempts left:", 4 - bank_attempts)
    except ValueError:
        bank_attempts += 1
        print("Invalid input. Attempts left:", 4 - bank_attempts)
else:
    print("Too many wrong bank selections. Exiting...")
    exit()

while True:
    try:
        pin = int(input("Enter your PIN: "))
        bank.auth(pin)
        print("Authentication successful!")
        break
    except ValueError as e:
        print(e)
        if "blocked" in str(e):
            exit()

atm(bank)
