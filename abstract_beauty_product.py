from sqlalchemy import Column, String, Integer, Float
from base import Base

class AbstractBeautyProduct(Base):
    """ Represents a Beauty Product (MakeUp or SkinCare) for discount check in a store """

    BOOLEAN_TRUE = 1

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    brand = Column(String(100))
    price = Column(Float)
    packaging = Column(String(100))
    rating = Column(Float)
    type = Column(String(8))
    discount = Column(Float)
    is_on_discount = Column(Integer)

    def __init__(self, name, brand, price, packaging, rating, type):
        """ initializes name, brand, price, packaging, rating that must be set on the product"""

        AbstractBeautyProduct._validate_string_input("Name", name)
        self.name = name

        AbstractBeautyProduct._validate_string_input("Brand", brand)
        self.brand = brand

        AbstractBeautyProduct._validate_float_input("Price", price)
        self.price = price

        AbstractBeautyProduct._validate_string_input("Packaging", packaging)
        self.packaging= packaging

        AbstractBeautyProduct._validate_float_input("Rating", rating)
        self.rating = rating

        AbstractBeautyProduct._validate_string_input("Type", type)
        self.type = type

        self.discount = 0.0
        self.is_on_discount = 0

    def apply_discount(self, discount):
        """ returns boolean True if discount is available and False otherwise """
        AbstractBeautyProduct._validate_float_input("Discount", discount)

        self.is_on_discount = AbstractBeautyProduct.BOOLEAN_TRUE
        self.discount = discount

    
    def is_on_sale(self):
        """ Returns whether or not the device is repaired """
        if self.is_on_discount == AbstractBeautyProduct.BOOLEAN_TRUE:
            return True

        return False
    
    def calc_discounted_price(self):
        """ calculates the discounted price of the beauty product """
        discounted_price = self.price * (1 - self.discount)
        return round(discounted_price,2)
    
    def get_details(self):
        """ Abstract method for the beauty product's details """
        raise NotImplementedError("Child class must override this method")
    
    def get_type(self):
        """ Abstract method for the beauty product's type """
        raise NotImplementedError("Child class must override this method")
    
    def to_dict(self):
        """ Gets the dictionary representation of Beauty Product """
        raise NotImplementedError("Child class must override this method")
    
    @staticmethod
    def _validate_string_input(display_name, value):
        """ Private helper to validate values """

        if value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if value == "":
            raise ValueError(display_name + " cannot be empty.")
        
        if not isinstance(value, str):
            raise ValueError(display_name + " is invalid.")
        
    @staticmethod
    def _validate_integer_input(display_label, value):
        """ Private helper to validate values """

        if value is None:
            raise ValueError(display_label + " cannot be undefined.")

        if value =="":
            raise ValueError(display_label + " must be positive.")
        
        if not isinstance(value, int):
            raise ValueError(display_label + " must be an integer.")
        
    @staticmethod
    def _validate_float_input(display_label, value):
        """ Private helper to validate values """

        if value is None:
            raise ValueError(display_label + " cannot be undefined.")

        if value=="" :
            raise ValueError(display_label + " must be positive.")
        
        if not isinstance(value, float):
            raise ValueError(display_label + " must be a float.")
        
