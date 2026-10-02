import json

def DisplayAll(): #1
    print("Current Inventory: ")
    print("-----------------------------")
    for product in LoadInventory():
        print(f"ID: {product['ID']} | Name: {product['Name']} | Price: {product['Price']} | Stock: {product['Stock']}")

#def AddProduct(): #2

#def UpdateStock(): #3

#def SearchProduct(): #4

def SaveInventory(inventory): #6
    with open('inventory.json', 'w') as f:
        json.dump(inventory, f, indent=4)

def LoadInventory(): #5
    with open('inventory.json', 'r') as f:
        inventory = json.load(f)
    return inventory        

while True:
    DisplayAll()
    break