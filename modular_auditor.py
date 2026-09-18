Inventory = 0
def get_valid_input():
    delivery = input("Enter amount of items: ")

    if delivery == "quit":
        print("Exiting syetem...")
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
    return current_total + new_value

while True:
    stock = get_valid_input()

    if stock == "quit":
        break
    elif stock == None:
        continue
    else:
        Inventory = processed_delivery(Inventory, stock)
print(Inventory)

        