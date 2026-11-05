from inventory import Inventory
from product import Product, PhysicalProduct, DigitalProduct, CanBeShipped

FILENAME = "inventory.json"


def ask_text(prompt):
    while True:
        value = input(prompt).strip()
        if value != "":
            return value
        print("Input cannot be empty.")


def ask_float(prompt, minimum=0.0):
    while True:
        try:
            value = float(input(prompt))
            if value >= minimum:
                return value
            print(f"Value must be at least {minimum}.")
        except ValueError:
            print("Please enter a number.")


def ask_int(prompt, allow_negative=False):
    while True:
        try:
            value = int(input(prompt))
            if allow_negative or value >= 0:
                return value
            print("Value cannot be negative.")
        except ValueError:
            print("Please enter a whole number.")


def add_product(inventory):
    print("\nProduct type: 1) Physical  2) Digital")
    choice = input("Choose type: ").strip()
    if choice not in ("1", "2"):
        print("Invalid type.")
        return

    product_id = ask_text("Product ID: ")
    name = ask_text("Name: ")
    price = ask_float("Price: ")
    stock = ask_int("Stock quantity: ")

    if choice == "1":
        weight = ask_float("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        download_size = ask_float("Download size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, download_size)

    if inventory.add_product(product):
        print("Product added.")
    else:
        print("A product with that ID already exists.")


def update_stock(inventory):
    product_id = ask_text("Product ID: ")
    quantity = ask_int("Quantity to add (negative to remove): ", allow_negative=True)
    if inventory.update_stock(product_id, quantity):
        print("Stock updated.")
    else:
        print("Product not found, or not enough stock.")


def search_product(inventory):
    keyword = ask_text("Search by ID or name: ")
    results = inventory.search(keyword)
    if len(results) == 0:
        print("No products found.")
        return
    for product in results:
        print("\n" + "-" * 30)
        product.display_information()
        print(product.get_fulfilment_info())
        if isinstance(product, CanBeShipped):
            print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")


# ===== TEST CODE (comment out or delete when done) =====
guitar = PhysicalProduct("P1", "Guitar", 450, 3, 2.5)
book = PhysicalProduct("P2", "Book", 20, 5, 0.5)
os_license = DigitalProduct("D1", "Operating System", 99.9, 10, 800)

print("--- Physical shows weight ---")
guitar.display_information()

print("\n--- Digital shows download size ---")
os_license.display_information()

print("\n--- get_fulfilment_info ---")
print(guitar.get_fulfilment_info())
print(os_license.get_fulfilment_info())

print("\n--- Shipping cost (heavier costs more) ---")
print(book.calculate_shipping_cost())
print(guitar.calculate_shipping_cost())

print("\n--- Digital is not shippable ---")
print(isinstance(guitar, CanBeShipped))      # True
print(isinstance(os_license, CanBeShipped))  # False

print("\n--- Product cannot be created directly ---")
try:
    Product("X1", "Test", 10, 5)
except TypeError as error:
    print("TypeError:", error)
print("===== END TEST =====\n")
# ========================================================


inventory = Inventory()
if inventory.load(FILENAME):
    print("Inventory loaded from file.")

while True:
    print("\n===== Inventory Management System =====")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Load inventory")
    print("7. Exit")
    option = input("Choose an option: ").strip()

    if option == "1":
        inventory.display_all()
    elif option == "2":
        add_product(inventory)
    elif option == "3":
        update_stock(inventory)
    elif option == "4":
        search_product(inventory)
    elif option == "5":
        inventory.save(FILENAME)
        print("Inventory saved.")
    elif option == "6":
        if inventory.load(FILENAME):
            print("Inventory loaded.")
        else:
            print("No saved file found.")
    elif option == "7":
        print("Goodbye.")
        break
    else:
        print("Invalid option.")