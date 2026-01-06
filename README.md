# Advanced-OOPS-Based-Banking-System
A console-based banking system built using Python OOPS concepts, featuring multiple banks, account types, transaction history, and runtime polymorphism via an ATM service layer.

Objectives

Demonstrate core OOPS principles clearly
Model real banking behavior
Show runtime polymorphism
Follow clean design and separation of responsibilities
Be suitable for interviews and GitHub portfolio

OOPS Concepts Used
1. Abstraction
Bank and Account are abstract base classes
They define what operations must exist, not how they are implemented

2. Inheritance
SBI, HDFC inherit from Bank
SavingsAccount, CurrentAccount inherit from Account

3. Polymorphism
Same ATM code works for:
Different banks
Different account types
Method calls behave differently at runtime based on the object

4. Encapsulation
Balance, PIN, and transaction data are internally managed
User interacts only through defined methods

Technologies Used

1. Python 3.x

2. abc module (Abstract Base Classes)

3. Object-Oriented Programming



How to Run


Navigate to the project directory:
cd banking-oops-python


Run the program:
python main.py

🧪 Sample Flow

1. User selects bank and account type
2. User enters PIN
3. ATM menu appears:
  Check balance
  Withdraw
  Deposit
  View transaction history
4. Same ATM works for all banks without modification
