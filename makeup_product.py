from abstract_beauty_product import AbstractBeautyProduct
from sqlalchemy import Column, String, Integer

class MakeUp(AbstractBeautyProduct):
    """ Represents a Makeup product """

    TYPE = "Makeup"

    shade = Column(String(100))
    waterproof = Column(Integer)

    def __init__(self, name, brand, price, packaging, rating, shade, waterproof):
        """ initializes the makeup product """
        super().__init__(name, brand, price, packaging, rating, MakeUp.TYPE)

        MakeUp._validate_string_input("Shade", shade)
        self.shade = shade

        if waterproof is None or not isinstance(waterproof, bool):
            raise ValueError("Waterproof must be a boolean")
        self.waterproof = waterproof

    def get_shade(self):
        """ returns shade of the MakeUp Product """
        return self.shade

    def get_waterproof_status(self):
        """ returns True if the MakeUp Product is waterproof and False otherwise """
        return self.waterproof

    def get_details(self):
        """ Returns makeup product specific details"""
        detail = "" 
        
        if self.waterproof ==  True:
            detail = f'{self.brand} {self.name} packed in a {self.packaging}' \
                        f'has a rating of {self.rating} and original price of ${self.price}'
            return detail
            
        else:
            detail = f'{self.brand} {self.name} packed in a {self.packaging}' \
                        f' has a rating of {self.rating} and original price of ${self.price}' 
            return detail


    def get_type(self):
        """ Returns makeup product type"""
        return MakeUp.TYPE
    
    def copy(self, object):
        """ copies data from a MakeUp object to this MakeUp Object """

        if isinstance(object, MakeUp):
            self.id = object.id
            self.name = object.name
            self.brand = object.brand
            self.price = object.price
            self.packaging = object.packaging
            self.rating = object.rating
            self.type = object.type
            self.shade = object.shade
            self.waterproof = object.waterproof
    
    def to_dict(self):
        """ Returns a dictionary representation of a MakeUp Product """
        dict = {}

        dict['id'] = self.id
        dict['name'] = self.name
        dict['brand'] = self.brand
        dict['packaging'] = self.packaging
        dict['price'] = self.price
        dict['rating'] = self.rating
        dict['type'] = MakeUp.TYPE
        dict['shade'] = self.shade
        dict['waterproof'] = self.waterproof
        
        return dict
    
    