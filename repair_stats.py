class RepairStats:
    """ Statistics on a Beauty Product Store Inventory """

    def __init__(self, makeup_products, skincare_products, discounted_products, non_discounted_products, total_discounted_price):
        """ Initialize the data values """

        if makeup_products is None or type(makeup_products) != int:
            raise ValueError("Invalid number of makeup products value")
        self._makeup_products = makeup_products

        if skincare_products is None or type(skincare_products) != int:
            raise ValueError("Invalid number of skincare products value")
        self._skincare_products = skincare_products

        if total_discounted_price is None or type(total_discounted_price) != float:
            raise ValueError("Invalid discount value")
        self._total_discounted_price = total_discounted_price

        if discounted_products is None or type(discounted_products) != int:
            raise ValueError("Invalid number of discounted products value")
        self._discounted_products = discounted_products

        if non_discounted_products is None or type(non_discounted_products) != int:
            raise ValueError("Invalid number of non-discounted products value")
        self._non_discounted_productss = non_discounted_products

    def get_num_makeup_products(self):
        """ Returns the number of makeup products """
        return self._makeup_products

    def get_num_skincare_products(self):
        """ Returns the number of skincare products """
        return self._skincare_products

    def get_total_discount(self):
        """ Returns the total discount of discounted products """
        return self._total_discount

    def get_num_discounted_products(self):
        """ Returns the number of discounted products """
        return self._discounted_products

    def get_num_non_discounted_products(self):
        """ Returns the number of non-discounted products """
        return self._non_discounted_productss

    def to_dict(self):
        """ Returns a dictionary representation of repair stats """

        dict={}

        dict['num_makeup_products']= self._makeup_products
        dict['num_skincare_products']= self._skincare_products
        dict['num_discounted_products']= self._discounted_products
        dict['num_non_discounted_products']= self._non_discounted_productss
        dict['total_discounted_price']=self._total_discounted_price
        
        return dict
    
    
