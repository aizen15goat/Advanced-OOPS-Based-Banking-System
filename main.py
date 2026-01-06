from abc import ABC, abstractmethod
import time

class Transaction:
    def __init__(self, ttype, amt, bal):
        self.ttype = ttype
        self.amt = amt
        self.bal = bal
        self.time = time.strftime("%H:%M")

    def show(self):
        return f"{self.ttype}: ${self.amt} at {self.time} | Balance: ${self.bal}"


class Account(ABC):
    def __init__(self, startbal):
        self.balance = startbal
        self.translist = []
    
    @abstractmethod
    def takeout(self, money):
        pass

    def putin(self, money):
        if money < 1:
            raise ValueError("Need positive amount")
        self.balance = self.balance + money
        trans = Transaction("Deposit", money, self.balance)
        self.translist.append(trans)

    def seebalance(self):
        return self.balance

    def seehistory(self):
        if not self.translist:
            print("Empty history")
        else:
            for item in self.translist:
                print(item.show())


class SavingsAcc(Account):
    def __init__(self, startbal):
        super().__init__(startbal)
        self.limitday = 5000
        self.keepmin = 2000
    
    def takeout(self, money):
        if money > self.limitday:
            raise ValueError("Over daily limit")
        if self.balance - money < self.keepmin:
            raise ValueError("Below minimum requirement")
        self.balance = self.balance - money
        self.translist.append(Transaction("Withdraw", money, self.balance))


class CurrentAcc(Account):
    def takeout(self, money):
        if money > self.balance:
            raise ValueError("Not enough funds")
        self.balance = self.balance - money
        self.translist.append(Transaction("Withdraw", money, self.balance))


class BankCard:
    def __init__(self, pincode, accobj):
        self.pincode = pincode
        self.accobj = accobj
        self.blockedflag = False
        self.failcount = 0

    def checkpin(self, pininput):
        if self.blockedflag:
            raise ValueError("Card blocked - go to bank")
        
        if pininput != self.pincode:
            self.failcount = self.failcount + 1
            if self.failcount >= 3:
                self.blockedflag = True
                raise ValueError("Card blocked after 3 fails")
            raise ValueError("Wrong pin code")
        
        self.failcount = 0

    def changepin(self, oldpin, newpin):
        if self.blockedflag:
            raise ValueError("Card blocked")
        
        if oldpin != self.pincode:
            self.failcount += 1
            if self.failcount >= 3:
                self.blockedflag = True
                raise ValueError("Card blocked")
            raise ValueError("Old pin wrong")
        
        if len(str(newpin)) != 4:
            raise ValueError("Need 4 digits")
        
        self.pincode = newpin
        print("Pin changed")

    def withdrawmoney(self, amount):
        self.accobj.takeout(amount)

    def depositmoney(self, amount):
        self.accobj.putin(amount)

    def getbalance(self):
        return self.accobj.seebalance()

    def gethistory(self):
        self.accobj.seehistory()


class SBIcard(BankCard):
    pass


class HDFCcard(BankCard):
    pass


def atmprocess(card):
    while True:
        print("\nATM Menu")
        print("1. Balance")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. History")
        print("5. Change PIN")
        print("6. Exit")

        try:
            option = int(input("Pick option (1-6): "))

            if option == 1:
                print(f"Balance: ${card.getbalance()}")

            elif option == 2:
                money = float(input("Withdraw amount: "))
                card.withdrawmoney(money)
                print("Done")

            elif option == 3:
                money = float(input("Deposit amount: "))
                card.depositmoney(money)
                print("Done")

            elif option == 4:
                card.gethistory()

            elif option == 5:
                oldpin = int(input("Current PIN: "))
                newpin = int(input("New PIN (4 digits): "))
                card.changepin(oldpin, newpin)

            elif option == 6:
                print("Goodbye")
                break

            else:
                print("Bad choice")

        except ValueError as err:
            print(f"Error: {err}")
            if "blocked" in str(err):
                break


print("ATM System Start")

trycount = 0
mycard = None

while trycount < 3:
    print("\nChoose Bank")
    print("1. SBI Savings")
    print("2. HDFC Current")
    
    try:
        bankpick = int(input("Enter 1 or 2: "))
        
        if bankpick == 1:
            acc = SavingsAcc(10000)
            mycard = SBIcard(1234, acc)
            break
        elif bankpick == 2:
            acc = CurrentAcc(20000)
            mycard = HDFCcard(5678, acc)
            break
        else:
            trycount += 1
            print(f"Wrong choice, tries left: {3 - trycount}")
    except:
        trycount += 1
        print(f"Bad input, tries left: {3 - trycount}")

if trycount >= 3:
    print("Too many fails")
    exit()

while True:
    try:
        pinenter = int(input("Enter PIN: "))
        mycard.checkpin(pinenter)
        print("PIN correct")
        break
    except ValueError as err:
        print(err)
        if "blocked" in str(err):
            exit()

atmprocess(mycard)
