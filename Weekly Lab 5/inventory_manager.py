import json

def DisplayAll(): #1
    print("Current Inventory: ")
    print("-----------------------------")
    for product in LoadInventory():
        print(f"ID: {product['ID']} | Name: {product['Name']} | Price: {product['Price']} | Stock: {product['Stock']}")
    print("-----------------------------")

def AddProduct(): #2
    print("Add New Product")
    id = input("Product ID: ")
    name = input("Product Name: ")
    price = input("Product Price: ")
    stock = input("Product Stock: ")
    new_product = {"ID": id, "Name": name, "Price": price, "Stock": stock}
    inventory = LoadInventory()
    inventory.append(new_product)


def UpdateStock(): #3
    print("Update Stock")
    id = input("Enter Product ID: ")
    inventory = LoadInventory()
    for product in inventory:
        if product['ID'] == id:
            print(f"\nProduct Found:\nName: {product['Name']}\nCurrent Stock:{product['Stock']}")
            new_stock = input("New Stock Quantity: ")
            product['Stock'] = new_stock
            SaveInventory(inventory)
            print("\nStock updated successfully!")
    print("\nProduct ID not found. Please try again.")

#def SearchProduct(): #4

def SaveInventory(inventory): #6
    with open('inventory.json', 'w') as f:
        json.dump(inventory, f, indent=4)

def LoadInventory(): #5
    with open('inventory.json', 'r') as f:
        inventory = json.load(f)
    return inventory        

UpdateStock()
