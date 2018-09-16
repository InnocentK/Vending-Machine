#File:    proj2.py
#Author   Innocent Kironji
#Date:    04/19/2017
#Section: CMSC201-22
#E-mail:  wambugu1@umbc.edu
#Description:
#    This program will display for the user a prototype
#    for a digital vending machine. The program will take in a card balance
#    (representing money) from the user and the contents of the machine from
#    a file. The program will then allow the user to purchase one of the
#    contents and then update the users balance and the contents of the
#    machine from the file the information was found.

MENU = " 1 - Display Vending Machine \n 2 - Make Selection \n 3 - Display Card Balance \n 4 - Add Money to Card \n 5 - Quit"
WELCOME_MSG = "This program simulates a vending machine. You may choose which vending machine you 'load' in, and may also specify how much money you have available for purchasing vending machine items."
NUM_INFO_TYPES = 3
ITEMS_PER_ROW = 3

#Choices
DISPLAY_MACHINE = 1
SELECTION = 2
DISPLAY_BALANCE = 3
ADD_MONEY = 4
QUIT = 5

#Prompts
CHOICE_PROMPT = "Enter a number between 1 and 5 (inclusive): "
BALANCE_PROMPT = "Please enter a decimal number (greater than or equal to zero): "
SELECTION_PROMPT = "Please enter one of the choice from the vending machine: "
MACHINE_PROMPT = "Please enter file to load machine from: "


# show_display() prints items in vending machine, their price & their code
#
# Input:         vending_machine; a string that has the name of the .txt
#                  file that contains information on the contents of the
#                  machine
# Output:        none; this function only prints
def show_display(vending_machine):

    #Defining some variables
    contents = []
    products = []
    prices = []
    codes = []

    display_items = open(vending_machine)
    for line in display_items:
        line = line.strip()
        #Directly assigns each token to a variable
        product, price, quantity, code = line.split()

        #Adds item information to a list
        if (int(quantity) > 0):
            item_info = [product, price, code]
            products.append(product + "\t")
            prices.append("$" + str(price))
            codes.append(code)

        #If there is no more of that candy it is stored as being empty
        else:
            item_info = ["{EMPTY}", "", ""]
            products.append("{EMPTY}")
            prices.append("")
            codes.append("")
        contents.append(item_info)

    display_items.close()
    
    #Some more variables
    first_column = 0
    second_column = 1
    third_column = 2
    
    #Prints a display with each candy (in sets of three per row) with information about it under the candy
    for counter in range(0, len(products), ITEMS_PER_ROW):
        print("\t", products[counter], products[second_column + counter], products[third_column + counter])
        print("\t", prices[counter], "\t", prices[second_column + counter], "\t", prices[third_column + counter])
        print("\t", codes[counter], "\t", codes[second_column + counter], "\t", codes[third_column + counter])
        print()


# make_selection() allows the user to purchase a candy if they have enough
#                  money and then updates the vending_machine file
# Input:           vending_machine; a string that contains the name of the
#                                   file that will be used for the contents
#                                   of the machine
#                  balance; a float variable for the user's card balance
# Output:          new_balance; a float variable for updated card balance
#                               after purchases have been accounted for
def make_selection(vending_machine, balance):

    #Defining some variables
    products = []
    prices = []
    codes = []
    quantities = []
    counter = 0
    valid_choice = False

    #Runs through the .txt file that represents the vending machine
    machine_items = open(vending_machine)
    for line in machine_items:
        line = line.strip()

        #Directly assigns each token to a variables
        product, price, quantity, code = line.split()

        #Adds each item and their information to different lists in corresponding positions
        products.append(str(product))
        prices.append(float(price))
        codes.append(code)
        quantities.append(int(quantity))

    machine_items.close()
    selection = input(SELECTION_PROMPT)

    #Repromts the user until they make a valid candy selection
    while (valid_choice == False):

        counter = 0
        #Checks if code entered by users matches code for candy in machine
        while (counter < len(codes)):

            #Once a valid choice is made, that choice is saved
            if (selection == codes[counter]):
                valid_choice = True
                choice = counter

                #The choice is also invalid if there are no more of that candy left
                if (quantities[choice] == 0):
                    valid_choice = False

            counter += 1

        #Updates the selection if it is not contained in machine
        if (valid_choice == False):
            print("That is not a valid choice, please try again")
            selection = input(SELECTION_PROMPT)

    #Checks to see if user has enough money for purchase
    if (balance >= prices[choice]):
        quantities[choice] -= 1

        #Lets the user know their purchase succeded and how much money they have after the purchase
        print("Congrats, you bought a " + products[choice] + "!")
        new_balance = check_balance(balance, prices[choice])
        
        #Updates the .txt file with the new candy quantities
        machine_items = open(vending_machine, "w")
        for count in range(0, len(products)):
            machine_items.write(products[count] + "\t" + str(prices[count]) + "  " + str(quantities[count]) + "  " + codes[count] + "\n")

        machine_items.close()

    #If you do not have enough money to make a purchase
    else:
        print("Sorry, you do not have enough money for that.")
        new_balance = balance

    return new_balance


# check_balance() displays user's current card balance (after acounting for
#                  change in said balance)
# Input:          balance; a float that contains user's card balance
#                 reduction; a float that contains the change in the users
#                            balance after a purchase
# Output:         current_balance; a float that contains user's updated card
#                              balance
def check_balance(balance, reduction):

    current_balance = balance - reduction
    print("You now have $" + str(current_balance) + " left on your card")
    return current_balance


# add_balance() allows user to add money to their existing card balance and
#                will reprompt user if they try to add an invalid amount
# Input:        balance; a float that contains user's card balance
# Output:       new_balance; a float with the user's updated card balance
def add_balance(balance):

    print("Please enter the amount of money you want to add to your card.")

    #Priming read
    new_money = float(input(BALANCE_PROMPT))

    #Checks to make sure money added is a positive number
    while (new_money < 0):
        print("The decimal number must be positive. Please try again!")
        new_money = float(input(BALANCE_PROMPT))

    #Because check_balance() takes in a reduction new_money needs to be made a negative so that it is added rather than subtracted
    new_balance = check_balance(balance, -(new_money))
    return new_balance


# choice_runner() uses the user response to figure out what function to run
# Input:          choice; a integer that is the user's choice for what mode
#                         of the vending machine to use
#                 vending_machine; a string variable that contains the name
#                                  of the file used to distinguish contents
#                                  of the vending machine
#                 new_balance; a float that holds the user's card balance
# Output:
def choice_runner(choice, vending_machine, balance):

    new_balance = balance
    
    if (choice == DISPLAY_MACHINE):
        show_display(vending_machine)

    elif (choice == SELECTION):
       new_balance =  make_selection(vending_machine, balance)

    elif (choice == DISPLAY_BALANCE):
        check_balance(balance, 0)

    elif (choice == ADD_MONEY):
        new_balance = add_balance(balance)

    return new_balance

 
def main():

    print(WELCOME_MSG)
    print()

    machine = input(MACHINE_PROMPT)

    #Gets initial balance from user
    print("Please enter the amount of money you have on your card")
    balance = float(input(BALANCE_PROMPT))

    #Reprompts the user if they input invalid balance
    while (balance < 0):
        print("The decimal number must be positive. Please try again!")
        balance = float(input(BALANCE_PROMPT))

    print(MENU)
    print()
    
    #Priming Read
    choice = int(input(CHOICE_PROMPT))

    #Allows the user to run through the different options in the machine if they don't want to quit
    while (choice != QUIT):
        balance = choice_runner(choice, machine, balance)
        print()
        print(MENU)
        choice = int(input(CHOICE_PROMPT))

main()
