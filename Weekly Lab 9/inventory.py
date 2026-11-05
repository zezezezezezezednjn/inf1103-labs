from product import PhysicalProduct, DigitalProduct, product_from_dict
import json


class Inventory:

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.get_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def get_product(self, product_id):
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def search_product(self, keyword):
        keyword = keyword.lower()
        return [
            p for p in self.__products
            if keyword in p.get_product_id().lower()
            or keyword in p.get_name().lower()
        ]

    def display_all(self):
        if not self.__products:
            print("The inventory is empty.")
            return
        print("\n--- Inventory ---")
        for product in self.__products:
            product.display_information()

    def to_list(self):
        return [product.to_dict() for product in self.__products]

    def save(self, filename):                      
        data = [product.to_dict() for product in self.__products]
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load(self, filename):                      
        with open(filename, "r") as file:
            data = json.load(file)
        self.__products = [product_from_dict(item) for item in data]