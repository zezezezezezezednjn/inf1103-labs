import json
import os

newproduct = {}

def DisplayAll(): #1
    print("\nCurrent Inventory: ")
    print("-----------------------------")
    for product in inventory:
        print(f"ID: {product['ID']} | Name: {product['Name']} | Price: {product['Price']} | Stock: {product['Stock']}")
    print("-----------------------------\n")

def AddProduct(): #2
    print("\nAdd New Product")
    id = input("Product ID: ")
    if any(product['ID'] == id for product in inventory):
        print("\nProduct ID already exists. Please enter a different ID.\n")
        return {}
    name = input("Product Name: ")
    price = input("Product Price: ")
    stock = input("Product Stock: ")
    new_product = {"ID": id, "Name": name, "Price": price, "Stock": stock}
    print("\nProduct added successfully!\n")
    return new_product

def UpdateStock(): #3
    print("\nUpdate Stock")
    id = input("Enter Product ID: ")
    for product in inventory:
        if product['ID'] == id:
            print(f"\nProduct Found:\nName: {product['Name']}\nCurrent Stock: {product['Stock']}")
            new_stock = input("\nNew Stock Quantity: ")
            if not new_stock.isdigit() or int(new_stock) < 0:
                print("\nInvalid stock quantity. Please enter a non-negative integer.\n")
                return inventory
            else:
                new_stock = int(new_stock)
                product['Stock'] = new_stock
                SaveInventory(inventory)
                print("\nStock updated successfully!\n")
    if not any(product['ID'] == id for product in inventory):
        print("\nProduct ID not found. Please try again.\n")
    return inventory

def SearchProduct(): #4
    print("\nSearch Product")
    id = input("Enter Product ID: ")
    for product in inventory:
        if product ['ID'] == id:
            print("\nProduct Found")
            print("------------------------------")
            print(f"ID: {product['ID']}\nName: {product['Name']}\nPrice: {product['Price']}\nStock: {product['Stock']}")
            print("------------------------------\n")
    if not any(product['ID'] == id for product in inventory):
        print("\nProduct ID not found. Please try again.\n")

def SaveInventory(inventory): #6
    with open('inventory.json', 'w') as f:
        json.dump(inventory, f, indent=4)

def LoadInventory(): #5
    with open('inventory.json', 'r') as f:
        inventory = json.load(f)
    return inventory    

inventory = LoadInventory()

print("==========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("===========================================\n")
if os.path.exists('inventory.json'):
    print("inventory.json found.")
else:
    print("inventory.json not found. Creating a new file.")
    with open('inventory.json', 'w') as f:
        json.dump([], f)
print("Inventory loaded successfully.\n")
print("--------MENU--------")
print("1. Display All Products")
print("2. Add New Product")
print("3. Update Stock")
print("4. Search Product")
print("5. Save Inventory")
print("6. Exit")
print("--------------------\n")

while True:
    option = input("Enter option: ")
    if option == "1":
        DisplayAll()
    elif option == "2":
        newproduct = AddProduct()
        inventory.append(newproduct)
    elif option == "3":
        UpdateStock()
    elif option == "4":
        SearchProduct()
    elif option == "5":
        SaveInventory(inventory)
        print("\nInventory saved successfully!\n")
    elif option == "6":
        SaveInventory(inventory)
        print("\nSaving inventory before exiting...")
        print("Inventory saved successfully.")
        print("\nThank you for using Inventory Management System.")
        print("program terminated.")
        break
    else:
        print("\nInvalid option. Please try again.\n")

