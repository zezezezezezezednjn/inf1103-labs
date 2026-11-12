import os
import tempfile

from Inventory import Inventory
from Order import Order
from Product import Product, PhysicalProduct, DigitalProduct, CanBeShipped
from Supplier import Supplier

FILENAME = "inventory.json"


def ask_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value != "":
            return value
        print("Input cannot be empty.")


def ask_float(prompt: str, minimum: float = 0.0) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value >= minimum:
                return value
            print(f"Value must be at least {minimum}.")
        except ValueError:
            print("Please enter a number.")


def ask_int(prompt: str, allow_negative: bool = False) -> int:
    while True:
        try:
            value = int(input(prompt))
            if allow_negative or value >= 0:
                return value
            print("Value cannot be negative.")
        except ValueError:
            print("Please enter a whole number.")


def ask_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    supplier_id = ask_text("Supplier ID: ")
    if supplier_id in suppliers:
        print("Using existing supplier:")
        suppliers[supplier_id].display_information()
        return suppliers[supplier_id]
    name = ask_text("Supplier name: ")
    email = ask_text("Supplier email: ")
    suppliers[supplier_id] = Supplier(supplier_id, name, email)
    return suppliers[supplier_id]


def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nProduct type: 1) Physical  2) Digital")
    choice = input("Choose type: ").strip()
    if choice not in ("1", "2"):
        print("Invalid type.")
        return

    product_id = ask_text("Product ID: ")
    name = ask_text("Name: ")
    price = ask_float("Price: ")
    stock = ask_int("Stock quantity: ")
    supplier = ask_supplier(suppliers)

    if choice == "1":
        weight = ask_float("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        file_size = ask_float("File size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, supplier, file_size)

    if inventory.add_product(product):
        print("Product added.")
    else:
        print("A product with that ID already exists.")


def update_stock(inventory: Inventory) -> None:
    product_id = ask_text("Product ID: ")
    quantity = ask_int("Quantity to add (negative to remove): ", allow_negative=True)
    if inventory.update_stock(product_id, quantity):
        print("Stock updated.")
    else:
        print("Product not found, or not enough stock.")


def remove_product(inventory: Inventory) -> None:
    product_id = ask_text("Product ID to remove: ")
    if inventory.remove_product(product_id):
        print("Product removed from inventory.")
    else:
        print("Product not found.")


def search_product(inventory: Inventory) -> None:
    keyword = ask_text("Search by ID or name: ")
    results = inventory.search_product(keyword)
    if len(results) == 0:
        print("No products found.")
        return
    for product in results:
        print("\n" + "-" * 30)
        product.display_information()
        print(product.get_fulfilment_info())
        product.display_supplier()
        if isinstance(product, CanBeShipped):
            print(f"Shipping cost: ${product.calculate_shipping_cost():.2f}")


# test

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def run_lab8_tests() -> None:
    print("=== 2. ASSOCIATION: Supplier <-> Product ===")
    supplier = Supplier("S001", "M", "email")
    guitar = PhysicalProduct("P001", "Guitar", 450.0, 3, supplier, 2.5)
    eSIM = DigitalProduct("D001", "eSIM", 30.0, 100, supplier, 5.5)
    guitar.display_supplier()
    eSIM.display_supplier()

    del supplier
    print("-- after 'del supplier' --")
    guitar.display_supplier()
    eSIM.display_supplier()
    print("Same Supplier object shared:", guitar.get_supplier() is eSIM.get_supplier())

    print("\n=== 3. AGGREGATION: Inventory <> Product ===")
    inv_a, inv_b = Inventory(), Inventory()
    inv_a.add_product(guitar)
    inv_a.add_product(eSIM)
    inv_a.display_all()

    inv_a.remove_product("P001")
    print("Still in A?", inv_a.find_product("P001"))
    guitar.display_information()
    guitar.update_stock(2)
    print("Guitar stock after update:", guitar.get_stock())
    inv_b.add_product(guitar)
    print("Same object in B:", inv_b.find_product("P001") is guitar)

    print("\n=== 4. COMPOSITION: Order <>-- OrderLine ===")
    order1 = Order("O001")
    order1.add_order_line(guitar, 1)
    order1.add_order_line(eSIM, 3)
    order1.display_order()

    order2 = Order("O002")
    order2.add_order_line(eSIM, 2)
    line1 = order1.get_order_lines()[1]
    line2 = order2.get_order_lines()[0]
    print("Different OrderLine objects:", line1 is not line2)
    print("Same Product object:", line1.get_product() is line2.get_product())
    order2.display_order()

    order1.remove_order_line("P001")
    order1.display_order()
    print("Guitar still exists:", guitar.get_name())

    print("\n=== 6/7. LSP & POLYMORPHISM ===")
    show_product_details(guitar)
    show_product_details(eSIM)

    inventory = Inventory()
    inventory.add_product(guitar)
    inventory.add_product(eSIM)
    for product in inventory.get_products():       
        product.display_information()
        print(product.get_fulfilment_info())

    for product in inventory.get_products():       
        before = product.get_stock()
        product.update_stock(5)
        print(f"{product.get_name()}: {before} -> {product.get_stock()}")

    print("\n=== Save / load round trip (incl. supplier) ===")
    path = os.path.join(tempfile.gettempdir(), "lab8_test.json")
    inventory.save(path)
    loaded = Inventory()
    loaded.load(path)
    loaded.display_all()
    loaded.find_product("D001").display_supplier()
    os.remove(path)


def main() -> None:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}

    def remember_suppliers() -> None:
        for product in inventory.get_products():
            supplier = product.get_supplier()
            suppliers.setdefault(supplier.get_supplier_id(), supplier)

    if inventory.load(FILENAME):
        remember_suppliers()
        print("Inventory loaded from file.")

    while True:
        print("\n===== Inventory Management System =====")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Load inventory")
        print("7. Remove a product")
        print("8. Exit")
        print("9. test")
        option = input("Choose an option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product(inventory, suppliers)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            inventory.save(FILENAME)
            print("Inventory saved.")
        elif option == "6":
            if inventory.load(FILENAME):
                remember_suppliers()
                print("Inventory loaded.")
            else:
                print("No saved file found.")
        elif option == "7":
            remove_product(inventory)
        elif option == "8":
            break
        elif option == "9":
            run_lab8_tests()
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()