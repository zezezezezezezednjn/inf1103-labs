Inventory = 0
failed_entries = 0  
amount_entered = 0
orders = []
initial = [
    "1001, Wireless Mouse, 2\n",
    "1002, Keyboard, 1\n",
    "1003, USB Cable, 3\n"
]
index = 1003

def get_valid_name():
    product_name = input("Enter Product Name:")
    if  product_name == "quit":
        return "quit"
    else:
        return product_name

def get_valid_quantity():
    product_quantity = input("Enter amount of items: ")

    if product_quantity == "quit":
        return "quit"

    elif product_quantity.startswith("-"):
        print("ERROR: NO NEGATIVE NUMBERS")
        return None
    
    elif product_quantity.isdigit() == False:
        print("ERROR: INVALID INPUT")
        return None
    
    else:
        return int(product_quantity)

def processed_delivery(current_total, new_value):
    return current_total + new_value    #total inventory

def calculate_tax(amount):  #calculate tax for amount input by user
    after_tax = amount * 0.10
    return after_tax

def generate_report(total_units, failed_attempts, tax, amount_entered): #report
    print("\n===Audit Report===")
    print("Total units:", total_units)
    print("Failed attempts:", failed_attempts)
    print("Total deliveries processed:", amount_entered)
    print("Tax: $"+str(tax))

def load_inventory():
    with open('inventory.txt', "r+") as file:
        read = file.read()
    return read

def save_inventory(order):
    with open('inventory.txt', "w+") as file:
        file.writelines(order)

#initial print for current orders        
print("Current Orders:\n")
print(load_inventory())

#main code
while True:
    name = get_valid_name()

    if name == "quit":
        break

    quantity = get_valid_quantity()

    if quantity == "quit":
        break

    elif quantity == None:
        failed_entries += 1
        continue

    else:
        Inventory = processed_delivery(Inventory, quantity)
        amount_entered += quantity #calculate the amount user entered as total inventory not equal to delivery processed

#saving user input into .txt file
    index += 1
    orders.append(f"{index}, {name}, {quantity}\n")
    save_inventory(initial+orders)

#after user enter 'quit'
print("\nNew Orders Added:")
for order in orders:
    print(order, end="")
print("\nOrder successfully saved to inventory.txt")

#audit report
generate_report(Inventory, failed_entries, calculate_tax(amount_entered), amount_entered)
#end 