from abstract_beauty_product import AbstractBeautyProduct
from sqlalchemy import Column, String

class SkinCare(AbstractBeautyProduct):
    """ Represents skincare product"""

    TYPE = "Skincare"

    skin_type = Column(String(100))
    skin_concern = Column(String(100))

    def __init__(self, name, brand, price, packaging, rating, skin_type, skin_concern):
        """ Initializes skincare product"""
        super().__init__(name, brand, price, packaging, rating, SkinCare.TYPE)

        SkinCare._validate_string_input("Skin Type", skin_type)
        self.skin_type = skin_type

        SkinCare._validate_string_input("Skin Concern", skin_concern)
        self.skin_concern = skin_concern

    def get_skin_type(self):
        """ returns skin type for which SkinCare product is suitable """
        return self.skin_type
    
    def get_skin_concern(self):
        """ returns skin concern for which SkinCare product is used """
        return self.skin_concern
    
    def get_details(self):
        """ Returns skincare product specific details """

        detail = ""
        f'{self.brand} {self.name} packed in a {self.packaging}' \
                        f'has a rating of {self.rating} and original price of ${self.price}'
        return detail
    
    def get_type(self):
        """ Returns skincare product specific type """
        return SkinCare.TYPE
    
    def copy(self, object):
        """ copies data from a SkinCare object to this SkinCare Object """

        if isinstance(object, SkinCare):
            self.id = object.id
            self.name = object.name
            self.brand = object.brand
            self.price = object.price
            self.packaging = object.packaging
            self.rating = object.rating
            self.type = object.type
            self.skin_type = object.skin_type
            self.skin_concern = object.skin_concern
    
    def to_dict(self):
        """ Returns a dictionary representation of a SkinCare Product """
        dict = {}

        dict['id'] = self.id
        dict['name'] = self.name
        dict['brand'] = self.brand
        dict['packaging'] = self.packaging
        dict['price'] = self.price
        dict['rating'] = self.rating
        dict['type'] = self.type
        dict['skin_type'] = self.skin_type
        dict['skin_concern'] = self.skin_concern
        
        return dict
    
    