import json
import os

from Product import Product, product_from_dict


class Inventory:

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def update_stock(self, product_id: str, quantity: int) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        try:
            product.update_stock(quantity)
        except ValueError:
            return False
        return True

    def search_product(self, keyword: str) -> list[Product]:
        keyword = keyword.lower()
        return [
            p for p in self.__products
            if keyword in p.get_product_id().lower()
            or keyword in p.get_name().lower()
        ]

    def get_products(self) -> tuple[Product, ...]:
        return tuple(self.__products)

    def display_all(self) -> None:
        if not self.__products:
            print("The inventory is empty.")
            return
        print("\n--- Inventory ---")
        for product in self.__products:
            product.display_information()      # polymorphic, no isinstance

    def to_list(self) -> list[dict]:
        return [product.to_dict() for product in self.__products]

    def save(self, filename: str) -> None:
        with open(filename, "w") as file:
            json.dump(self.to_list(), file, indent=4)

    def load(self, filename: str) -> bool:
        if not os.path.exists(filename):
            return False
        with open(filename, "r") as file:
            data = json.load(file)
        self.__products = [product_from_dict(item) for item in data]
        return True