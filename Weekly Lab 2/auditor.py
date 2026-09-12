Inventory = 0
Failed_Entry = 0

while True:
    stock = input ("Enter the stock quantity or type 'quit' to exit: ")
    if stock == "quit":
        print ("Exiting system...")
        print("Total Units Proccessed: ",Inventory)
        print("Failed Entries: ",Failed_Entry)
        break

    elif stock.startswith("-"):
        print ("ERROR: No negative numbers allowed.")
        Failed_Entry += 1
        continue

    elif stock.isdigit() == False:
            print ("ERROR: Please enter a valid number.")
            Failed_Entry += 1
            continue
    
    stock = int(stock)
    Inventory += int(stock)

    if Inventory > 500:
         print ("ALERT: Inventory exceeds 500 units.")
         break

        
