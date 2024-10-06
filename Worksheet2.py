import random  # use random module to generate an account number and account password.

# various types of bank accounts related classes.
class BankAccount:
    def __init__(self, account_number, passcode, account_type, balance=0):
        # define the bank account with an account number, password, account type and balance.
        self.account_number = account_number
        self.passcode = passcode
        self.account_type = account_type
        self.balance = balance

    # method to deposit money.
    def deposit(self, amount):
        self.balance += amount  # add the deposited amount to the balance.
        print(f"{amount} deposited successfully! New balance: {self.balance}")

    # method of withdrawing money from account if funds present.
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds!")  # display an "insufficient funds" error message.
        else:
            self.balance -= amount  # subtract the amount withdrawn from the account balance.
            print(f"{amount} withdrawn successfully! Remaining balance: {self.balance}")

    # information on sending money to another account.
    def transfer(self, amount, recipient_account):
        if amount > self.balance:
            print("Insufficient funds for transfer!")  # output an "insufficient funds" error when not enough funds are in the account.
        else:
            self.withdraw(amount)  # Withdraw the money from the current account
            recipient_account.deposit(amount)  # Deposit the money into the recipient's account
            print(f"{amount} transferred successfully!")

# Class for personal accounts, inherits from BankAccount
class PersonalAccount(BankAccount):
    def __init__(self, account_number, passcode, balance=0):
        # Initialize personal account with the account type set to "Personal"
        super().__init__(account_number, passcode, "Personal", balance)

# Class for business accounts, inherits from BankAccount
class BusinessAccount(BankAccount):
    def __init__(self, account_number, passcode, balance=0):
        # Initialize business account with the account type set to "Business"
        super().__init__(account_number, passcode, "Business", balance)

# Class to manage the entire banking system
class BankingSystem:
    def __init__(self):
        self.accounts = {}  # Dictionary to store all the accounts
        self.load_accounts()  # Load existing accounts from a file

    # Load accounts from a file when the system starts
    def load_accounts(self):
        try:
            with open("accounts.txt", "r") as f:
                # Read each line and create accounts from the data
                for line in f.readlines():
                    acc_number, passcode, acc_type, balance = line.strip().split(", ")
                    if acc_type == "Personal":
                        self.accounts[acc_number] = PersonalAccount(acc_number, passcode, float(balance))
                    elif acc_type == "Business":
                        self.accounts[acc_number] = BusinessAccount(acc_number, passcode, float(balance))
        except FileNotFoundError:
            # If file does not exist, it will start fresh
            print("No existing accounts found. Starting fresh.")

    # Save all accounts to a file
    def save_accounts(self):
        with open("accounts.txt", "w") as f:
            # Write each account's details to the file
            for acc in self.accounts.values():
                f.write(f"{acc.account_number}, {acc.passcode}, {acc.account_type}, {acc.balance}\n")

    # Create a new account (either Personal or Business)
    def create_account(self, account_type):
        # Generate random account number and passcode
        account_number = str(random.randint(10000, 99999))
        passcode = str(random.randint(1000, 9999))
        
        # Create the account based on the type
        if account_type == "Personal":
            self.accounts[account_number] = PersonalAccount(account_number, passcode)
        elif account_type == "Business":
            self.accounts[account_number] = BusinessAccount(account_number, passcode)
        
        # Save the new account to the file
        self.save_accounts()
        print(f"Account created! Account Number: {account_number}, Passcode: {passcode}")

    # Login to an account by checking account number and passcode
    def login(self, account_number, passcode):
        account = self.accounts.get(account_number)  # Get account by account number
        if account and account.passcode == passcode:
            return account  # Return the account if login is successful
        else:
            print("Invalid login details.")  # Error message for wrong login
            return None

    # Delete an account from the system
    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]  # Remove the account from the dictionary
            self.save_accounts()  # Save the updated account list
            print(f"Account {account_number} deleted.")
        else:
            print("Account not found.")

# Main function that provides the menu and handles user input
def main():
    system = BankingSystem()  # Create an instance of BankingSystem
    while True:
        # Display the main menu options
        print("\n--- Banking System Menu ---")
        print("1. Open Account")
        print("2. Login to Account")
        print("3. Exit")
        choice = input("Choose an option: ")

        # Handle the user's choice
        if choice == "1":
            # Open a new account
            account_type = input("Enter account type (Personal/Business): ").capitalize()
            if account_type in ["Personal", "Business"]:
                system.create_account(account_type)
            else:
                print("Invalid account type.")
        
        elif choice == "2":
            # Login to an existing account
            account_number = input("Enter your account number: ")
            passcode = input("Enter your passcode: ")
            account = system.login(account_number, passcode)

            if account:
                # Once logged in, show account options
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

                    # Check balance
                    if account_choice == "1":
                        print(f"Your balance is: {account.balance}")
                    
                    # Deposit money
                    elif account_choice == "2":
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                        system.save_accounts()  # Save the updated balance
                    
                    # Withdraw money
                    elif account_choice == "3":
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                        system.save_accounts()  # Save the updated balance
                    
                    # Transfer money to another account
                    elif account_choice == "4":
                        recipient_number = input("Enter recipient account number: ")
                        recipient = system.accounts.get(recipient_number)
                        if recipient:
                            amount = float(input("Enter amount to transfer: "))
                            account.transfer(amount, recipient)
                            system.save_accounts()  # Save the updated balances
                        else:
                            print("Recipient account not found.")
                    
                    # Delete the logged-in account
                    elif account_choice == "5":
                        system.delete_account(account.account_number)
                        break  # Exit to the main menu after account is deleted
                    
                    # Logout from the account
                    elif account_choice == "6":
                        print("Logged out.")
                        break
                    
                    else:
                        print("Invalid option.")
        
        # Exit the program
        elif choice == "3":
            print("Exiting the system.")
            break
        else:
            print("Invalid option.")

# Run the main function when the program starts
if __name__ == "__main__":
    main()
