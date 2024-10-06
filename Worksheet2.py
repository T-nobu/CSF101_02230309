import random

class BankAccount:
    def __init__(self, account_number, passcode, account_type, balance=0):
        self.account_number = account_number
        self.passcode = passcode
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"{amount} deposited successfully! New balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds!")
        else:
            self.balance -= amount
            print(f"{amount} withdrawn successfully! Remaining balance: {self.balance}")

    def transfer(self, amount, recipient_account):
        if amount > self.balance:
            print("Insufficient funds for transfer!")
        else:
            self.withdraw(amount)
            recipient_account.deposit(amount)
            print(f"{amount} transferred successfully!")



class PersonalAccount(BankAccount):
    def __init__(self, account_number, passcode, balance=0):
        super().__init__(account_number, passcode, "Personal", balance)

class BusinessAccount(BankAccount):
    def __init__(self, account_number, passcode, balance=0):
        super().__init__(account_number, passcode, "Business", balance)



class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()

    def load_accounts(self):
        try:
            with open("accounts.txt", "r") as f:
                for line in f.readlines():
                    acc_number, passcode, acc_type, balance = line.strip().split(", ")
                    if acc_type == "Personal":
                        self.accounts[acc_number] = PersonalAccount(acc_number, passcode, float(balance))
                    elif acc_type == "Business":
                        self.accounts[acc_number] = BusinessAccount(acc_number, passcode, float(balance))
        except FileNotFoundError:
            print("No existing accounts found. Starting fresh.")

    def save_accounts(self):
        with open("accounts.txt", "w") as f:
            for acc in self.accounts.values():
                f.write(f"{acc.account_number}, {acc.passcode}, {acc.account_type}, {acc.balance}\n")

    def create_account(self, account_type):
        account_number = str(random.randint(10000, 99999))
        passcode = str(random.randint(1000, 9999))
        if account_type == "Personal":
            self.accounts[account_number] = PersonalAccount(account_number, passcode)
        elif account_type == "Business":
            self.accounts[account_number] = BusinessAccount(account_number, passcode)
        self.save_accounts()
        print(f"Account created! Account Number: {account_number}, Passcode: {passcode}")

    def login(self, account_number, passcode):
        account = self.accounts.get(account_number)
        if account and account.passcode == passcode:
            return account
        else:
            print("Invalid login details.")
            return None

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            self.save_accounts()
            print(f"Account {account_number} deleted.")
        else:
            print("Account not found.")



def main():
    system = BankingSystem()
    while True:
        print("\n--- Banking System Menu ---")
        print("1. Open Account")
        print("2. Login to Account")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            account_type = input("Enter account type (Personal/Business): ").capitalize()
            if account_type in ["Personal", "Business"]:
                system.create_account(account_type)
            else:
                print("Invalid account type.")
        
        elif choice == "2":
            account_number = input("Enter your account number: ")
            passcode = input("Enter your passcode: ")
            account = system.login(account_number, passcode)

            if account:
                while True:
                    print("\n--- Account Menu ---")
                    print(f"Logged in as: {account.account_number} ({account.account_type})")
                    print("1. Check Balance")
                    print("2. Deposit Funds")
                    print("3. Withdraw Funds")
                    print("4. Transfer Funds")
                    print("5. Delete Account")
                    print("6. Logout")
                    account_choice = input("Choose an option: ")

                    if account_choice == "1":
                        print(f"Your balance is: {account.balance}")
                    elif account_choice == "2":
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                        system.save_accounts()
                    elif account_choice == "3":
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                        system.save_accounts()
                    elif account_choice == "4":
                        recipient_number = input("Enter recipient account number: ")
                        recipient = system.accounts.get(recipient_number)
                        if recipient:
                            amount = float(input("Enter amount to transfer: "))
                            account.transfer(amount, recipient)
                            system.save_accounts()
                        else:
                            print("Recipient account not found.")
                    elif account_choice == "5":
                        system.delete_account(account.account_number)
                        break
                    elif account_choice == "6":
                        print("Logged out.")
                        break
                    else:
                        print("Invalid option.")
        
        elif choice == "3":
            print("Exiting the system.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
