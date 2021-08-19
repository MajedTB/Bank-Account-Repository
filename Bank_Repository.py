# This work is done by group: 10 , Section: 66
# Saeed Adel Bawazeer, 201945830, (50%) 
# Majed Talal Bamardouf, 201918870, (50%)

from time import sleep
from datetime import datetime

def main():
    # ask the user to login or signup and validate the input
    operation = input("Please enter (L) for login, or (S) for signup: ").upper()
    while operation != "L" and operation != "S":
        print("Invalid input. Please try again. ❌")
        operation = input("Please enter (L) for login, or (S) for signup: ").upper()
        
    # call function depending on user input and assign current pin to a variable for later use
    if operation == "L":
        cardNumber, pin = login()
    else:
        create()
        cardNumber, pin = login()
        
    # show menu and ask user to choose feature
    terminate = False
    transactionsSession = 0  # set the number of transactions during the session to 0
    while not terminate:
        printMenu()
        # ask user to choose feature and validate
        feature = input("Enter your feature: ")
        while feature not in "1234567" or len(feature) != 1:
            print("Invalid input. Please try again. ❌")
            feature = input("Enter your feature: ")

        # call function depending on user input
        if feature == "1":
            show(cardNumber + ".txt")
        elif feature == "2":
            pin = changePINFun(pin, cardNumber)  # assign new pin to pin in main()
        elif feature == "3":
            withdrawFun(cardNumber)
            transactionsSession += 1  # add 1 to transactionsSession
        elif feature == "4":
            depositFun(cardNumber)
            transactionsSession += 1
        elif feature == "5":
            payBillFun(cardNumber)
            transactionsSession += 1
        elif feature == "6":
            viewTransactionsFun(cardNumber)
        elif feature == "7":
            terminate = True
            terminateFun(cardNumber, transactionsSession)


def printMenu():  # print the menu for the user
    print()
    print("=" * 36)
    print("Bank Account Program")
    print("=" * 36)
    print("1.   Show account information")
    print("2.   Change PIN number")
    print("3.   Withdraw amount of money")
    print("4.   Deposit amount of money")
    print("5.   Pay bills")
    print("6.   View the last transactions")
    print("7.   Terminate the program")
    print("=" * 36)


def printHeader(message):  # print a header for a function
    print()
    print("=" * (len(message) + 2))
    print(" " + message + " ")
    print("=" * (len(message) + 2))
    
    
def isValidNumber(num):  # check if the number is valid as a card number or PIN
    # if it is not 4 characters long or the characters are not all digits then the number is not valid
    if len(num) != 4 or not num.isdigit():
        return False
    else:
        # check if there is a number repeated in the string
        for i in num:
            if num.count(i) > 1:  # if any character is present more than once then the number is not valid
                return False
    return True  # if the number passes all tests then it is valid

def create():  # creates an account file for the user
    # print a header for the sign up feature
    printHeader("Create New Account")

    # Step 1 : taking card number from user and validating it
    cardNumber = input("(1) Please enter a new 4-digit card number (no repeated numbers): ")

    cardNumberExists = True  # assume card number exists in the system
    while not isValidNumber(cardNumber) or cardNumberExists:  # repeat until input is valid
        cardNumberExists = True
        # check if card number is valid
        if not isValidNumber(cardNumber):  
            print("Invalid input. Please follow the guidelines and try again. ❌")
            cardNumber = input("(1) Please enter a new 4-digit card number (no repeated numbers): ")
            
        # then check if card number is not occupied   
        else:
            try:  # try opening a file with the provide card number
                open(cardNumber + ".txt", "r") # if the card number is not occupied it will exit from the loop
                print("Card number already exists. Please try again. ❌")
                cardNumber = input("(1) Please enter a new 4-digit card number (no repeated numbers): ")
            except:  # if there is no file then the card number is not occupied
                cardNumberExists = False

    print("Card number accepted. ✅ \n")

    # Step 2 : taking PIN number from user and validating it
    pin = input("(2) Please enter a new 4-digit PIN (no repeated numbers): ")

    while not isValidNumber(pin):  # repeat until input is valid
        print("Invalid input. Please follow the guidelines and try again. ❌")
        pin = input("Please enter a new 4-digit PIN (no repeated numbers): ")

    print("PIN accepted. ✅\n")

    # Step 3: taking kfupm email from user and validating it
    validEmail = False  # we assume the email is not valid

    while not validEmail:  # repeat until the email entered by the user is valid
        email = input("(3) Enter your KFUPM email: ").lower()  # since email is case insensitive we take the lowercase

        # if the email is KFUPM email then it is valid
        if email[1:].endswith("@kfupm.edu.sa"):
            validEmail = True
        else:  # if the email is not valid then print a message to the user
            print("The email is not a KFUPM email, please try again. ❌")
    print("Email accepted. ✅\n")

    # Step 4 : allow user to choose an extra service
    print("(4) Please choose an extra service: ")
    print("1. Student Account.")
    print("2. Business Account.")
    # verify the input
    choice = input("Enter the number of service (1 or 2): ")
    while choice != "1" and choice != "2":
        choice = input("Invalid input. ❌ Please try again (1 or 2): ")
    # store the extra service in a variable
    if choice == "1":
        extraService = "Student Account"
    else:
        extraService = "Business Account"

    # show the user the card number and PIN
    print("\nYour account has been created.")
    print("=" * 22)  # header
    print("Sign in Information:")
    print("Card number is:", cardNumber)
    print("PIN is:", pin)
    print("=" * 22, "\n")  # footer

    accountFile = open(cardNumber + ".txt", "w")  # create the account file

    # store the account details
    accountFile.write("Card number: " + cardNumber + "\n")
    accountFile.write("PIN: " + pin + "\n")
    accountFile.write("Email: " + email + "\n")
    accountFile.write("Balance: " + "0.00" + "\n")
    accountFile.write("Extra service: " + extraService + "\n")

    # close the file
    accountFile.close()
    # wait for 2 seconds before login in
    sleep(2)


def login():  # allow the user to login to an existing account
    # print a header for the function
    printHeader("Login To Your Account")

    # Step 1 : taking the card number from the user and checking if it exist
    cardNumberFound = False
    while not cardNumberFound:  # repeat until card number is found
        cardNumberInput = input("(1) Please enter your card number: ")
        try:  # try opening the file using the number provided
            account = open(cardNumberInput + ".txt", "r")
            cardNumberFound = True
        except FileNotFoundError:  # if the file is not found inform the user
            print("Card number not found. Please try again. ❌")
    print("Card number accepted. ✅\n")

    # taking the PIN number from the file to use it in step 2
    lines = account.readlines()     # store the lines in the file
    pinLine = lines[1].rstrip("\n") # take the line that contains the PIN and remove the new line character
    correctPin = pinLine[-4:]       # take the final 4 characters, those will be the correct pin

    # Step 2 : taking the PIN number from the user and checking if it's correct
    pinCorrect = False
    while not pinCorrect:  # repeat until the user enters the correct pin
        pin = input("(2) Please enter your PIN: ")
        if pin == correctPin:  # if the pin is correct change pinCorrect to True
            pinCorrect = True
        else:  # if it's not correct inform the user
            print("Incorrect PIN. Please try again. ❌")
    print("PIN is correct. ✅")
    print("\nLogin successful. ✅")

    # close the file
    account.close()
    # wait for 2 seconds before exiting
    sleep(2)
    # return the card number and the pin for use in main()
    return (cardNumberInput, pin)


def show(file):  # shows the user his account details
    # print a header for the function
    printHeader("Account Details")

    # open the account file to print the details
    accountFile = open(file, "r")
    lines = accountFile.readlines()
    for i in range(0, 5):  # only print the lines that contain account information
        print(lines[i].rstrip("\n"))

    # close the file
    accountFile.close()

    # wait for 3 seconds before exiting
    sleep(3)


def changePINFun(currentPIN, cardNumber):  # lets the user change his PIN
    # print a header for the function
    printHeader("Change Your PIN")

    # step 1 : ask the user for his card number for verification
    cardCorrect = False
    while not cardCorrect:
        cardNumberIn = input("(1) To change your PIN, please enter your card number: ")
        if cardNumberIn == cardNumber:
            cardCorrect = True
        else:
            print("Incorrect card number, please try again. ❌")
    print("Card number is correct. ✅\n")

    # step 2 : ask the user for his old PIN for verification
    pinCorrect = False
    while not pinCorrect:
        oldPin = input("(2) Please Enter your (old) PIN: ")
        if oldPin == currentPIN:
            pinCorrect = True
        else:
            print("Incorrect PIN, please try again. ❌")
    print("PIN is correct. ✅\n")

    # step 3 : ask the user for the new PIN
    newPin = input("(3) Please enter your (new) 4-digit PIN (no repeated numbers): ")
    while not isValidNumber(newPin):
        print("Invalid input. Please follow the guidelines and try again. ❌")
        newPin = input("(3) Please enter your (new) 4-digit PIN (no repeated numbers): ")

    # open and store all lines in the old file
    oldFile = open(cardNumber + ".txt", "r")
    data = oldFile.readlines()
    data[1] = "PIN: " + newPin + "\n"  # change the PIN in the data list to the new PIN

    # write the data into a new file
    newFile = open(cardNumber + ".txt", "w")
    newFile.writelines(data)

    # close the files
    oldFile.close()
    newFile.close()

    # wait for 2 seconds before exiting
    print("Your PIN has been changed. ✅")
    sleep(2)

    return newPin


def withdrawFun(cardNumber):  # allow user to withdraw money from account
    # print a header for the function
    printHeader("Withdraw Money")

    # open and store all lines in the old file
    oldFile = open(cardNumber + ".txt", "r")
    data = oldFile.readlines()
    oldFile.close()

    # split the line that contains the balance and read it's value
    balanceLine = data[3].split(": ")
    balance = float(balanceLine[1].rstrip("\n"))

    # check that input is positive float and that user has enough balance
    notValidInput = True
    while notValidInput:
        try:
            withdrawAmount = float(input("Enter the amount you would like to withdraw: "))
            if balance >= withdrawAmount and withdrawAmount >= 0:
                notValidInput = False
            else:
                print("Not enough balance in your account. Please try again. ❌")
        except ValueError:
            print("Invalid input. Please try again. ❌")

    # deduct the withdraw amount
    balance = balance - round(withdrawAmount, 2)
    data[3] = "Balance: " + str(balance) + "\n"  # change the balance line in the file

    # update balance line in the account file
    newFile = open(cardNumber + ".txt", "w")
    newFile.writelines(data)

    # add the transaction and date and time to the file
    transactionDateTime = datetime.now().strftime("%c")
    transactionLine = "Withdraw: " + ("%.2f SAR on (" % withdrawAmount) + transactionDateTime + ")\n"
    newFile.write(transactionLine)

    # print success message to user
    print("You have successfully withdrawn %.2f SAR. ✅" % withdrawAmount)

    # close the file and sleep for few seconds
    newFile.close()
    sleep(2)


def depositFun(cardNumber):  # allow user to deposit money to account
    # print a header for the function
    printHeader("Deposit Money")

    # open and store all lines in the old file then close the file
    oldFile = open(cardNumber + ".txt", "r")
    data = oldFile.readlines()
    oldFile.close()

    # split the line that contains the balance and read it's value
    balanceLine = data[3].split(": ")
    balance = float(balanceLine[1].rstrip("\n"))

    # check that input is positive float
    notValidInput = True
    while notValidInput:
        try:
            depositAmount = float(input("Enter the amount you would like to deposit: "))
            if depositAmount >= 0:
                notValidInput = False
            else:
                print("Invalid input. Please try again. ❌")
        except ValueError:
            print("Invalid input. Please try again. ❌")

    # add the deposited amount to the balance
    balance = balance + round(depositAmount, 2)
    data[3] = "Balance: " + str(balance) + "\n"  # change the balance line

    # update balance line in the account file
    newFile = open(cardNumber + ".txt", "w")
    newFile.writelines(data)

    # add the transaction and date and time to the file
    transactionDateTime = datetime.now().strftime("%c")
    transactionLine = "Deposit: " + ("%.2f SAR on (" % depositAmount) + transactionDateTime + ")\n"
    newFile.write(transactionLine)

    # print success message to user
    print("You have successfully deposited %.2f SAR. ✅" % depositAmount)

    # close the file and sleep for few seconds
    newFile.close()
    sleep(2)


def payBillFun(cardNumber):  # allow user to pay bills using money from account
    # print a header for the function
    printHeader("Pay bills")

    # open and store all lines in the old file then close the file
    oldFile = open(cardNumber + ".txt", "r")
    data = oldFile.readlines()
    oldFile.close()

    # split the line that contains the balance and read it's value
    balanceLine = data[3].split(": ")
    balance = float(balanceLine[1].rstrip("\n"))

    # step 1 & 2 : ask the user to enter the bill name and account number
    billName = input("(1) Enter the name of the bill: ")
    billAccount = input("(2) Enter the account number of the bill: ")
    while not billAccount.isdigit():
        print("Invalid input please try again. ❌")
        billAccount = input("(2) Enter the account number of the bill: ")

    # step 3 : ask for the bill amount and check that input is positive float and that user has enough balance
    notValidInput = True
    while notValidInput:
        try:
            billAmount = float(input("(3) Enter the bill amount: "))
            if balance >= billAmount and billAmount >= 0:
                notValidInput = False
            else:
                print("Not enough balance in your account. Please try again. ❌")
        except ValueError:
            print("Invalid input. Please try again. ❌")

    # deduct the withdraw amount
    balance = balance - round(billAmount, 2)
    data[3] = "Balance: " + str(balance) + "\n"  # change the balance line in the file

    # update balance line in the account file
    newFile = open(cardNumber + ".txt", "w")
    newFile.writelines(data)

    # add the transaction and date and time to the file
    transactionDateTime = datetime.now().strftime("%c")
    transactionLine = ("Payment: %.2f SAR to %s (%s) on (" % (billAmount, billName, billAccount)) + transactionDateTime + ")\n"
    newFile.write(transactionLine)

    # print success message to user
    print("You have successfully paid %s bill of %.2f SAR to account: %s. ✅" % (billName, billAmount, billAccount))

    # close the file and sleep for few seconds
    newFile.close()
    sleep(2)


def viewTransactionsFun(cardNumber):  # show user all transactions on the account
    # print a header for the function
    printHeader("View Transactions")

    # open file and read data then close the file
    accountFile = open(cardNumber + ".txt", "r")
    fileList = accountFile.readlines()
    balanceLine = fileList[3].rstrip("\n")
    transactionLines = fileList[5:]
    accountFile.close()

    # print message to user if there are no transactions
    if transactionLines == []:
        print("No transactions.")
        sleep(2)
        return None  # get out of the function since there are no transactions
    # print a header for the transactions list
    print("\n" + balanceLine + " SAR")
    print("-" * 50)
    print("Transaction:  Description       (Date/Time)")
    print("-" * 50)

    # print the transactions
    for line in transactionLines:
        print(line.rstrip("\n"))

    # sleep for few seconds
    sleep(4)


def terminateFun(cardNumber, numOfTransactions):
    # print header for termination
    printHeader("Terminating Program")
    
    # if no transactions were made by the user print a message and exit the function
    if numOfTransactions == 0:
        print("No transactions were made during the session.")
        printHeader("Thank You")
        return None
    
    # open file and read data then close the file
    accountFile = open(cardNumber + ".txt", "r")
    fileList = accountFile.readlines()
    balanceLine = fileList[3].rstrip("\n")
    transactionLines = fileList[5:]
    accountFile.close()

    transactionsDuringSession = transactionLines[-numOfTransactions:]  # list of transactions during the session

    # print a header for the transactions list
    print("\n" + balanceLine + " SAR")
    print("-" * 50)
    print("The following are the transactions during this session:")
    print("Transaction:  Description       (Date/Time)")
    print("-" * 50)

    # print the transactions
    for line in transactionsDuringSession:
        print(line.rstrip("\n"))

    # print thank you message for the user
    printHeader("Thank You")

# Run the program
main()
