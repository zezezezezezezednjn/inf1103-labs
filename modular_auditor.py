Inventory = 0
failed_entries = 0
def get_valid_input():
    delivery = input("Enter amount of items: ")

    if delivery == "quit":
        print("Exiting syetem...")
        return "quit"

    elif delivery.startswith("-"):
        print("ERROR: NO NEGATIVE NUMBERS")

    elif delivery.isdigit() == False:
        print("ERROR: INVALID INPUT")

    return delivery

while True:
    stock = get_valid_input()

    if stock == "quit":
        break

        