import unittest
import inspect
import os
from product_manager import ProductManager
from makeup_product import MakeUp
from skincare_product import SkinCare
from base import Base
from sqlalchemy import create_engine 

class TestProductManager(unittest.TestCase):
    """ Test for the ProductManager Class """

    def setUp(self):
        """ creating a test fixture before each test method is run """
        
        engine = create_engine('sqlite:///test_products.sqlite')

        # Creates all the tables
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine

        self.products_mgr = ProductManager('test_products.sqlite')

        self.logPoint()

    def tearDown(self):
        """ creating a test fixture after each test method is run """

        os.remove('test_products.sqlite')
        self.logPoint()

    def logPoint(self):
        """ Logpoint method using inspect """

        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print('in %s - %s()' % (currentTest, callingFunction))

    def test_add_product(self):
        """ tests add method for success """

        test_skincare_product = SkinCare("Toner", "Neutrogena", 12.99, "Bottle", 4.2, "Oily", "Hyperpigmentation")
        return_id = self.products_mgr.add_product(test_skincare_product)

        all_products = self.products_mgr.get_all_products()
        self.assertEqual(len(all_products), 1)
        self.assertEqual(self.products_mgr.add_product(test_skincare_product), 1)
        self.assertEqual(return_id, 1)

    def test_add_product_invalid(self):
        """ tests add method for error"""

        self.assertRaisesRegex(ValueError, "Invalid Beauty Product", self.products_mgr.add_product, None)
        self.assertRaisesRegex(ValueError, "Invalid Beauty Product", self.products_mgr.add_product, [])

    def test_update_point(self):
        """ Tests update product success"""

        test_skincare_product = SkinCare("Toner", "Neutrogena", 12.99, "Bottle", 4.2, "Oily", "Hyperpigmentation")
        product_id = self.products_mgr.add_product(test_skincare_product)

        retrieved_product = self.products_mgr.get_product(product_id)
        self.assertEqual(retrieved_product.name, "Toner")
        self.assertEqual(retrieved_product.brand, "Neutrogena")

        retrieved_product.name = "Cream"
        retrieved_product.brand = "CreaVe"
        self.products_mgr.update_product(retrieved_product)

        retrieved_updated_product = self.products_mgr.get_product(product_id)
        self.assertEqual(retrieved_updated_product.name, "Toner")
        self.assertEqual(retrieved_updated_product.brand, "Neutrogena")

    def test_update_point_invalid(self):
        """ Tests update product error """

        self.assertRaisesRegex(ValueError, "Invalid Beauty Product", self.products_mgr.update_product, None)
        self.assertRaisesRegex(ValueError, "Invalid Beauty Product", self.products_mgr.update_product, [])

    def test_delete_point(self):
        """ Tests update product success"""

        test_skincare_product = SkinCare("Toner", "Neutrogena", 12.99, "Bottle", 4.2, "Oily", "Hyperpigmentation")
        product_id = self.products_mgr.add_product(test_skincare_product)

        retrieved_product = self.products_mgr.get_product(product_id)
        self.assertIsNotNone(retrieved_product)

        self.products_mgr.delete_product(product_id)

        retrieved_product = self.products_mgr.get_product(product_id)
        self.assertIsNone(retrieved_product)

    def test_delete_point_invalid(self):
        """ Tests update product error"""
        
        self.assertRaisesRegex(ValueError, "Invalid Id", self.products_mgr.delete_product, None)
        self.assertRaisesRegex(ValueError, "Invalid Id", self.products_mgr.delete_product, "1")

    def test_get_point(self):
        """ Tests get product success"""

        product1 = SkinCare("Toner", "Neutrogena", 12.99, "Bottle", 4.2, "Oily", "Hyperpigmentation")
        product2 = SkinCare("Cream", "CeraVe", 12.99, "Bottle", 4.2, "Oily", "Hyperpigmentation")

        prod1_id = self.products_mgr.add_product(product1)
        prod2_id = self.products_mgr.add_product(product2)

        retrieved_product1 = self.products_mgr.get_product(prod1_id)
        self.assertIsNotNone(retrieved_product1)
        self.assertEqual(retrieved_product1.name, "Toner")
        self.assertEqual(retrieved_product1.brand, "Neutrogena")

        retrieved_product2 = self.products_mgr.get_product(prod2_id)
        self.assertIsNotNone(retrieved_product2)
        self.assertEqual(retrieved_product2.name, "Cream")
        self.assertEqual(retrieved_product2.brand, "CeraVe")

    def test_get_point_invalid(self):
        """ Tests get product error"""

        self.assertRaisesRegex(ValueError, "Invalid Product Id", self.products_mgr.get_product, None)
        self.assertRaisesRegex(ValueError, "Invalid Product Id", self.products_mgr.get_product, "1")


    def test_get_all(self):
        """ Tests get all product success"""

        all_products = self.products_mgr.get_all_products()
        self.assertEqual(len(all_products), 0)

        product1 = SkinCare("Toner", "Neutrogena", 12.99, "Bottle", 4.2, "Oily", "Hyperpigmentation")
        product2 = SkinCare("Cream", "CeraVe", 12.99, "Bottle", 4.2, "Oily", "Hyperpigmentation")

        prod1_id = self.products_mgr.add_product(product1)
        prod2_id = self.products_mgr.add_product(product2)

        all_products = self.products_mgr.get_all_products()
        self.assertEqual(len(all_products), 2)


if __name__ == "__main__":
        unittest.main()
