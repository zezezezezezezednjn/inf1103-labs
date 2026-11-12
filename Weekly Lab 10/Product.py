from abc import ABC, abstractmethod

from Supplier import Supplier


class Product(ABC):

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("Stock must be a whole number that is 0 or more.")
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock: int = stock
        # Association: the Product knows about its Supplier but does not own it.
        self.__supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be a whole number.")
        if self.__stock + quantity < 0:
            raise ValueError("Not enough stock.")
        self.__stock += quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id:<6} | Name: {self.__name:<15} | "
              f"Price: ${self.__price:>9.2f} | Stock: {self.__stock}")

    def display_supplier(self) -> None:
        self.__supplier.display_information()

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict(),
        }


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = float(weight)

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return 10 + 3 * self.__weight

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data


class DigitalProduct(Product):

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, file_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__file_size: float = float(file_size)

    def get_file_size(self) -> float:
        return self.__file_size

    def display_information(self) -> None:
        super().display_information()
        print(f"File Size: {self.__file_size} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["file_size"] = self.__file_size
        return data


def product_from_dict(data: dict) -> Product:
    if "supplier" in data:
        supplier = Supplier.from_dict(data["supplier"])
    else:  # older save files (before Lab 8) have no supplier
        supplier = Supplier("S000", "Unknown Supplier", "unknown@example.com")

    if data["type"] == "physical":
        return PhysicalProduct(data["id"], data["name"], data["price"],
                               data["stock"], supplier, data["weight"])
    if data["type"] == "digital":
        size = data.get("file_size", data.get("download_size"))
        return DigitalProduct(data["id"], data["name"], data["price"],
                              data["stock"], supplier, size)
    raise ValueError(f"Unknown product type: {data['type']}")