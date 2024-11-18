import time


class ATM:
    def __init__(self, id, location, cash_available):
        self.id = id
        self.location = location
        self.cash_available = cash_available
        self.screen = Screen()
        self.keypad = Keypad()
        self.receipt_printer = ReceiptPrinter()
        self.current_card = None

    def insert_card(self, card):
        if self.current_card:
            self.screen.display_message("A card is already inserted.")
        else:
            self.current_card = card
            self.screen.display_message("Card inserted. Please enter your PIN.")

    def eject_card(self):
        if self.current_card:
            self.screen.display_message("Ejecting card...")
            self.current_card = None
        else:
            self.screen.display_message("No card to eject.")

    def validate_pin(self, pin):
        if self.current_card and self.current_card.validate_pin(pin):
            self.screen.display_message("PIN validated. Select a transaction.")
            return True
        else:
            self.screen.display_message("Invalid PIN.")
            return False

    def show_withdrawal_options(self):
        self.screen.display_message(
            "Choose an amount to withdraw:\n"
            "1. $20\n"
            "2. $50\n"
            "3. $100\n"
            "4. $200\n"
            "5. Enter custom amount"
        )
        choice = self.keypad.get_input("Enter your choice: ")
        if choice == "1":
            self.withdraw_cash(20)
        elif choice == "2":
            self.withdraw_cash(50)
        elif choice == "3":
            self.withdraw_cash(100)
        elif choice == "4":
            self.withdraw_cash(200)
        elif choice == "5":
            custom_amount = float(self.keypad.get_input("Enter custom amount: "))
            self.withdraw_cash(custom_amount)
        else:
            self.screen.display_message("Invalid choice. Returning to menu.")

    def check_balance(self):
        if self.current_card:
            balance = self.current_card.get_linked_account().get_balance()
            self.screen.display_message(f"Your balance is ${balance:.2f}")
        else:
            self.screen.display_message("No card inserted.")

    def withdraw_cash(self, amount):
        if not self.current_card:
            self.screen.display_message("No card inserted.")
            return

        account = self.current_card.get_linked_account()
        if amount > account.get_balance():
            self.screen.display_message("Insufficient funds in your account.")
        elif amount > self.cash_available:
            self.screen.display_message("ATM does not have enough cash.")
        else:
            account.withdraw(amount)
            self.cash_available -= amount
            self.screen.display_message(f"Dispensing ${amount:.2f}")
            self.screen.display_message("Thank you for your transaction.")
            self.ask_for_receipt(amount)

    def ask_for_receipt(self, amount):
        choice = self.keypad.get_input("Do you want a receipt? (yes/no): ").lower()
        if choice == "yes":
            self.print_receipt(amount)
        else:
            self.screen.display_message("Thank you for banking with us.")
        self.eject_card()

    def print_receipt(self, amount):
        account = self.current_card.get_linked_account()
        transaction = Transaction("withdrawal", amount)
        receipt = transaction.generate_receipt(self.location, account)
        self.receipt_printer.print(receipt)


class Account:
    def __init__(self, account_number, account_holder, balance, currency="USD"):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.currency = currency

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def deposit(self, amount):
        self.balance += amount

    def get_balance(self):
        return self.balance


class Card:
    def __init__(self, card_number, pin, account):
        self.card_number = card_number
        self.pin = pin
        self.account = account

    def validate_pin(self, pin):
        return self.pin == pin

    def get_linked_account(self):
        return self.account


class Transaction:
    def __init__(self, transaction_type, amount):
        self.transaction_id = str(int(time.time() * 1000))  # Unique ID
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    def generate_receipt(self, location, account):
        return (
            f"Bank: Home Bank\n"
            f"Branch: {location}\n"
            f"Date: {self.timestamp.split()[0]}\n"
            f"Time: {self.timestamp.split()[1]}\n"
            f"Amount: ${self.amount:.2f}\n"
            f"Currency: {account.currency}\n"
            f"Account Holder: {account.account_holder}\n"
            f"Account Number: ****{account.account_number[-4:]}"
        )


class Screen:
    def display_message(self, message):
        print(f"SCREEN: {message}")


class Keypad:
    def get_input(self, prompt):
        return input(prompt)


class ReceiptPrinter:
    def print(self, receipt):
        print("\n=== Receipt ===")
        print(receipt)
        print("================")


# Example Usage
if __name__ == "__main__":
    # Create an account and card
    account = Account("1234567890", "John Doe", 1000.0)
    card = Card("1234-5678-9101-1121", "3333", account)

    # Initialize ATM
    atm = ATM("ATM01", "Cyprus Branch", 5000.0)

    # Simulate ATM operations
    atm.insert_card(card)
    pin = atm.keypad.get_input("Enter your PIN: ")
    if atm.validate_pin(pin):
        atm.screen.display_message("1. Check Balance\n2. Withdraw Cash\n3. Exit")
        choice = atm.keypad.get_input("Choose a transaction: ")
        if choice == "1":
            atm.check_balance()
        elif choice == "2":
            atm.show_withdrawal_options()
        elif choice == "3":
            atm.eject_card()
        else:
            atm.screen.display_message("Invalid choice.")