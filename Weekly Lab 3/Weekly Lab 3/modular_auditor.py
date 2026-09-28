Inventory = 0
failed_entries = 0  
amount_entered = 0

def get_valid_input():
    delivery = input("Enter amount of items: ")

    if delivery == "quit":
        print("Exiting syetem...\n")
        return "quit"

    elif delivery.startswith("-"):
        print("ERROR: NO NEGATIVE NUMBERS")
        return None
    
    elif delivery.isdigit() == False:
        print("ERROR: INVALID INPUT")
        return None
    
    else:
        return int(delivery)

def processed_delivery(current_total, new_value):
    return current_total + new_value    #total inventory

def calculate_tax(amount):  #calculate tax for amount input by user
    after_tax = amount * 0.10
    return after_tax

def generate_report(total_units, failed_attempts, tax, amount_entered): #report
    print("====REPORT====")
    print("Total units: ", total_units)
    print("Failed attempts: ", failed_attempts)
    print("Total deliveries processed: ", amount_entered)
    print("Tax: ", tax)

#main code
while True:
    stock = get_valid_input()

    if stock == "quit":
        break

    elif stock == None:
        failed_entries += 1
        continue

    else:
        Inventory = processed_delivery(Inventory, stock)
        amount_entered += stock #calculate the amount user entered as total inventory not equal to delivery processed
        amount_taxed = calculate_tax(amount_entered)
        

#after user enter "quit" it will display:   
generate_report(Inventory,failed_entries, amount_taxed, amount_entered)





