from abstract_beauty_product import AbstractBeautyProduct
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base

from makeup_product import MakeUp
from skincare_product import SkinCare
from repair_stats import RepairStats

class ProductManager:
    """ Manages products in a store """

    ID_LABEL = "Id"
    TYPE_LABEL = "Type"

    def __init__(self, db_filename):
        """ constructor for the product manager store """
        
        if db_filename is None or db_filename == "":
            raise ValueError("DB Name cannot be undefined")
        
        engine = create_engine("sqlite:///" + db_filename)

        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine

        self._db_session = sessionmaker(bind=engine)

    def add_product(self, product):
        """ adds a new product in for discount """

        if product is None or not isinstance(product, AbstractBeautyProduct):
            raise ValueError("Invalid Beauty Product")
        

        session = self._db_session()

        session.add(product)
        session.commit()

        product_id = product.id

        session.close()

        return product_id

   
    def delete_product(self, product_id):
        """ removes product by id """

        if product_id is None or not isinstance(product_id, int):
            raise ValueError("Invalid Id")
        
        session = self._db_session()

        existing_product = session.query(AbstractBeautyProduct).filter(AbstractBeautyProduct.id == product_id).first()

        if existing_product is None:
            session.close()
            raise ValueError("Product does not exist.")
        
        session.delete(existing_product)
        session.commit()

        session.close()

    def update_product(self, product):
        """ updates an existing product """

        if product is None or not isinstance(product, AbstractBeautyProduct):
            raise ValueError("Invalid Beauty Product")
        
        session = self._db_session()
        
        if product.type == MakeUp.TYPE:
            existing_product = session.query(MakeUp).filter(MakeUp.id == product.id).first()
        elif product.type == SkinCare.TYPE:
            existing_product = session.query(SkinCare).filter(SkinCare.id == product.id).first()
        else:
            existing_product is None

        existing_product.copy(product)

        session.commit()
        session.close()

    
    def get_product(self, product_id):
        """ returns a product by id """

        if product_id is None or not isinstance(product_id, int):
            raise ValueError("Invalid Product Id")
        
        session = self._db_session()
        
        existing_product = session.query(MakeUp).filter(MakeUp.id == product_id).first()
        
        if existing_product is None:
            existing_product = session.query(SkinCare).filter(SkinCare.id == product_id).first()
        
        session.close()
        
        return existing_product
    
    def get_product_details(self, product_type):
        """ Returns the details of each Product """

        if product_type is None or not isinstance(product_type, str):
            raise ValueError("Invalid Product Type.")
        
        session = self._db_session()

        if product_type == MakeUp.TYPE:
            products = session.query(MakeUp).filter(MakeUp.type == "Makeup").all()
        elif product_type == SkinCare.TYPE:
            products = session.query(SkinCare).filter(SkinCare.type == "Skincare").all()
        else:
            products = []
        
        session.close()

        product_details = []
        for product in products:
            if not product.is_on_sale():
                product_detail = product.get_details()
                product_details.append(product_detail)

        return product_details
    
    def get_product_details_by_id(self, id):
        """ Returns the details of each Product """

        if id is None or not isinstance(id, int):
            raise ValueError("Invalid Product Type.")
        
        session = self._db_session()
        
        product = session.query(MakeUp).filter(MakeUp.id == id).first()
        if product is None:
            product = session.query(SkinCare).filter(SkinCare.id == id).first()
    
        product_details = product.get_details()
        
        session.close()

        return product_details
    
    def get_repair_stats(self):
        """ Returns the current discount statistics for the shop """
        
        session = self._db_session()
        
        products = session.query(AbstractBeautyProduct).all()
        
        session.close()

        non_discounted_products = 0
        discounted_products = 0
        total_discounted_price = 0.0
        makeup_products = 0
        skincare_products = 0

        for product in products:
            if product.is_on_sale():
                discounted_products += 1
                total_discounted_price += product.calc_discounted_price()
            else:
                non_discounted_products += 1

            if product.type == MakeUp.TYPE:
                makeup_products += 1

            if product.type == SkinCare.TYPE:
                skincare_products += 1

        return RepairStats(makeup_products, skincare_products, discounted_products, non_discounted_products, round(total_discounted_price, 2))

    def get_all_products(self):
        """ returns a list of all products """

        session = self._db_session()
        
        existing_products = session.query(AbstractBeautyProduct).all()                                                     

        session.close()

        return existing_products

    
    def get_all_products_by_type(self, type):
        """ returns a list of products by type """

        if type is None or not isinstance(type, str):
            raise ValueError("Invalid Product Type")
        
        session = self._db_session()

        if type == SkinCare.TYPE:
            products = session.query(SkinCare).filter(SkinCare.type == "Skincare").all()
        elif type == MakeUp.TYPE:
            products = session.query(MakeUp).filter(MakeUp.type == "Makeup").all()
        else:
            products = []
        
        session.close()

        return products

    def apply_discount_to_prod(self, id, discount):
        """ Marks a device as repaired """

        if id is None or not isinstance(id, int):
            raise ValueError("Invalid Id")
        
        if discount is None or not isinstance(discount, float):
            raise ValueError("Invalid discount")
        
        session = self._db_session()
        
        product = session.query(MakeUp).filter(MakeUp.id == id).first()
        
        if product is None:
            product = session.query(SkinCare).filter(SkinCare.id == id).first()
        
        if product is None:
            session.close()
            raise ValueError("Could not find product by id")
        
        product.apply_discount(discount)
        session.commit()

        session.close()

    @staticmethod
    def _validate_string_method(display_name, value):
        """ Private helper to validate values """

        if value is None:
            raise ValueError(display_name + " cannot be undefined." )
        
        if value == '':
            raise ValueError(display_name + " cannot be empty." )
        
        if not isinstance(value, str):
            raise ValueError(display_name + " is invalid.")
        
    @staticmethod
    def _validate_integer_method(display_name, value):
        """ Private helper to validate values """

        if value is None:
            raise ValueError(display_name + " cannot be undefined." )
        
        if value < 0 :
            raise ValueError(display_name + " must be positive." )
        
        if not isinstance(value, int):
            raise ValueError(display_name + " must be an integer." )