import traceback
import numpy as np

# Define a class to represent a Bank Account with name, account type, ID, and balance attributes
class BankAccount(object):
    def __init__(self, name, accountType, ID, balance=0):
        # Initialize the account attributes (name, account type, balance, ID)
        self.__name = name
        self.__accountType = accountType
        self.__balance = balance
        self.__filename = str(ID) + "_" + accountType + "_" + name + ".txt"
        self.__ID = ID

    def Balance_update(self, update):
        # Update the balance of the account
        self.__balance = update

    def get_name(self):
        return self.__name

    def get_balance(self):
        return self.__balance

    def get_account_type(self):
        return self.__accountType

    def get_ID(self):
        return self.__ID

    def get_Filename(self):
        return self.__filename

    def Display_info(self):
        # Display account information
        print("The name is: ", self.__name)
        print("The Account Type is: ", self.__accountType)
        print("The Balance is: ", self.__balance)
        print("The ID is: ", self.__ID)


# Define a class to represent the bank system that contains a list of bank accounts
class BankSystem:
    def __init__(self):
        # Initialize the system with some bank accounts
        self.acounts = [BankAccount("refaat", "chequing", 343, 20)]
        self.acounts.append(BankAccount("mohamed", "saving", 3343, 10))
        self.acounts.append(BankAccount("ali", "chequing", 534, 50))
        self.acounts.append(BankAccount("ahmed", "saving", 565, 25))
        self.__current_account = self.acounts[0]

    def Send_money(self, name, amount):
        try:
            name_flag = False
            if len(self.acounts) >= 1:
                for account in self.acounts:
                    if account.get_name() == name:
                        if self.__current_account.get_balance() >= amount:
                            name_flag = True
                            account.Balance_update(account.get_balance() + amount)
                            self.__current_account.Balance_update(self.__current_account.get_balance() - amount)

                            # Log the transaction to the files
                            with open(account.get_Filename(), "a") as file:
                                file.write("You received: " + str(amount) + " $ from: " + self.__current_account.get_name() + "\n")
                            with open(self.__current_account.get_Filename(), "a") as file:
                                file.write("You sent: " + str(amount) + " $ to: " + account.get_name() + "\n")
                        else:
                            print("Sorry, you do not have enough money.")
                if not name_flag:
                    print("You entered a wrong name.")
        except Exception as e:
            # Handle any exceptions that occur during the transfer
            exception_handling(e)

    def WithDraw(self, amount):
        try:
            if len(self.acounts) >= 1:
                if self.__current_account.get_balance() >= amount:
                    self.__current_account.Balance_update(self.__current_account.get_balance() - amount)
                    # Log the transaction to the file
                    with open(self.__current_account.get_Filename(), "a") as file:
                        file.write("You withdrew: " + str(amount) + " $\n")
                else:
                    print("Sorry, you do not have enough money.")
        except Exception as e:
            # Handle any exceptions that occur during the withdrawal
            exception_handling(e)

    def Deposite(self, amount):
        try:
            if len(self.acounts) >= 1:
                self.__current_account.Balance_update(self.__current_account.get_balance() + amount)
                # Log the transaction to the file
                with open(self.__current_account.get_Filename(), "a") as file:
                    file.write("You deposited: " + str(amount) + " $\n")
        except Exception as e:
            # Handle any exceptions that occur during deposit
            exception_handling(e)

    def display(self):
        # Display the current account information
        self.__current_account.Display_info()

    def Logging(self, name):
        try:
            log_flag = False
            if len(self.acounts) >= 1:
                for account in self.acounts:
                    if account.get_name() == name:
                        self.__current_account = account
                        log_flag = True
            return log_flag
        except Exception as e:
            # Handle any exceptions that occur during login
            exception_handling(e)

    def display_history(self):
        try:
            # Display the transaction history from the file
            with open(self.__current_account.get_Filename(), "r") as file:
                print(file.read())
        except Exception as e:
            # Handle any exceptions that occur during history display
            exception_handling(e)

# Define an exception handling function to catch and handle specific exceptions
def exception_handling(ex):
    # Handle different types of exceptions and provide appropriate messages
    if isinstance(ex, FileNotFoundError):
        print("Please make sure you have a file to save.")
        main_program()
    elif isinstance(ex, PermissionError):
        print("Please make sure you have permission to open and write in this file.")
        main_program()
    elif isinstance(ex, IndexError):
        print("Please make sure you chose a correct line index.")
        main_program()
    elif isinstance(ex, ValueError):
        print("Please make sure you enter an integer number as a choice.")
        main_program()
    else:
        print(f"An unexpected error occurred: {str(ex)}")
        main_program()

# Main function where the user interacts with the bank system
def main_program():
    try:
        # Create a new bank system instance
        bank = BankSystem()

        # Prompt the user to enter their name and log in
        user_name = input("Please enter your user name: ")
        if not bank.Logging(user_name):
            raise ZeroDivisionError("Invalid username. Please try again.")

        while True:
            print("Please enter the option:\n1 - Display info\n2 - Withdraw")
            print("3 - Deposit\n4 - Transfer money")
            print("5 - Log in as another user\n6 - Terminate the program\n7 - Print the history")
            user_in = int(input("Your choice: "))

            # Use match-case to handle different user choices
            match user_in:
                case 1:
                    bank.display()  # Display account info
                case 2:
                    amount = int(input("Enter the amount to withdraw: "))  # Get the amount to withdraw
                    bank.WithDraw(amount)  # Withdraw money
                case 3:
                    amount = int(input("Enter the amount to deposit: "))  # Get the amount to deposit
                    bank.Deposite(amount)  # Deposit money
                case 4:
                    name = input("Please enter the recipient's name: ")
                    amount = int(input("Please enter the amount to transfer: "))  # Transfer money
                    bank.Send_money(name, amount)
                case 5:
                    user_name = input("Please enter the new user name to log in: ")
                    if not bank.Logging(user_name):
                        print("Invalid username.")
                case 6:
                    break  # Exit the program
                case 7:
                    bank.display_history()  # Print transaction history
                case _:
                    print("Please enter a valid choice.")  # Invalid choice
    except Exception as e:
        # If an exception occurs, handle it by calling exception_handling
        exception_handling(e)

# Start the program
main_program()
