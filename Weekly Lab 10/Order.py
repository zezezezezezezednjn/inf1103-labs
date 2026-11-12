from Product import Product


class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a whole number above 0.")
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display(self) -> None:
        print(f"  {self.__product.get_name()} x {self.__quantity} "
              f"= ${self.calculate_subtotal():.2f}")


class Order:
    """Composition: the Order creates and manages its own OrderLines."""

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__order_lines)      # read-only view

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.__order_lines:
            if line.get_product().get_product_id().lower() == product_id.lower():
                self.__order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_order(self) -> None:
        print(f"Order {self.__order_id}:")
        for line in self.__order_lines:
            line.display()
        print(f"  TOTAL: ${self.calculate_total():.2f}")