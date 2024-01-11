from flask import Flask, request
from product_manager import ProductManager
from skincare_product import SkinCare
from makeup_product import MakeUp
import json

app = Flask(__name__)

product_manager = ProductManager("products.sqlite")

@app.route("/productshop/products", methods=["POST"])
def add_product():
    """ Add a product to the shop - either SkinCare or MakeUp """

    content = request.json

    try:
        if content["type"] == SkinCare.TYPE:
            product = SkinCare(content['name'], content['brand'], content['price'], content['packaging'], content['rating'], content['skin_type'], content['skin_concern'])

        elif content["type"] == MakeUp.TYPE:
            product = MakeUp(content['name'], content['brand'], content['price'], content['packaging'], content['rating'], content['shade'], content['waterproof'])

        else:
            response = app.response_class(
                status=400,
                response="Invalid Product Type"
            )
            return response
        
        # Add the SkinCare or MakeUp object to the beauty shop
        id = product_manager.add_product(product)

        response = app.response_class(
            status=200,
            response = json.dumps(id),
            mimetype = 'application/json'
        )
        return response

    except ValueError as e:
        response = app.response_class(
            status=400,
            response=str(e)
        )
        return response
    
    except KeyError as e:
        response = app.response_class(
            status=400,
            response=str(e)
        )
        return response
    
@app.route("/productshop/products/<string:type>", methods=["GET"])
def get_descriptions(type):
    """ Gets the list of the Descriptions of the pending products """
    
    description = product_manager.get_product_details(type)
    json_description = json.dumps(description)
    response = app.response_class(
                   status=200,
                   response =  json_description,
                   mimetype="application/json")
    return response

@app.route("/productshop/products/details/<int:id>", methods=["GET"])
def get_product_details(id):
    """ Gets the details of a product """

    detail = product_manager.get_product_details_by_id(id)
    json_description = json.dumps(detail)
    response = app.response_class(
                   status=200,
                   response = json_description,
                   mimetype="application/json")
    return response


@app.route("/productshop/repairstats", methods=["GET"])
def get_stats():
    """ Returns the discount statistics for the store """

    stats = product_manager.get_repair_stats()

    json_stats = json.dumps(stats.to_dict())
    response = app.response_class(
                   status=200,
                   response=json_stats,
                   mimetype="application/json"
                )
    return response

@app.route("/productshop/products/<int:id>", methods=["PUT"])
def update_product(id):
    """ Updates the product based on id """

    content = request.json

    if id <= 0:
        response = app.response_class(
            status=400,
            response="Product Id is invalid."
        )
        return response
    
    try:
        if content["type"] == SkinCare.TYPE:
            product = SkinCare(content['name'], content['brand'], content['price'], content['packaging'], content['rating'], content['skin_type'], content['skin_concern'])

        elif content["type"] == MakeUp.TYPE:
            required_fields = {'name', 'brand', 'price', 'packaging', 'rating', 'shade', 'waterproof'}
            if not required_fields.issubset(content.keys()):
                raise ValueError("Missing required fields for MakeUp product.")
            
            product = MakeUp(content['name'], content['brand'], content['price'], content['packaging'], content['rating'], content['shade'], content['waterproof'])

        else:
            response = app.response_class(
                status=400,
                response="Invalid Product Type"
            )
            return response
        
        product.id = id

        # Update the SkinCare or MakeUp object
        product_manager.update_product(product)

        response = app.response_class(
            status=200
        )
        return response

    except ValueError as e:
        response = app.response_class(
            status=404,
            response=str(e)
        )
        return response
    
    except KeyError as e:
        response = app.response_class(
            status=404,
            response=str(e)
        )
        return response
    
@app.route("/productshop/products/<int:id>", methods=["GET"])
def get_product(id):
    """ Gets an existing SkinCare or MakeUp from the ProductManager (based on id) """
    
    if id <= 0:
            response = app.response_class(
                status=400,
                response="Product Id is invalid."
            )
            return response
    
    try:
        product = product_manager.get_product(id)
        
        response = app.response_class(
                status = 200,
                response = json.dumps(product.to_dict()),
                mimetype = 'application/json'
            )
        return response

    # Otherise, it the product isn't found, then return a 404 response
    except ValueError as e:
        response = app.response_class(
            status=404,
            response=str(e)
        )
        return response
    
    except KeyError as e:
        response = app.response_class(
            status=404,
            response=str(e)
        )
        return response
    
@app.route("/productshop/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    """ Deletes a SkinCare or MakeUp products from the ProductManager (based on id) """

    if id <= 0:
        response = app.response_class(
            status=400,
            response="Product Id is invalid."
        )
        return response

    try:
        product_manager.delete_product(id)
        response = app.response_class(
            status=200
        )
        return response

    # Otherise, it the product isn't found, then return a 404 response
    except ValueError as e:
        response = app.response_class(
            status=404,
            response=str(e)
        )
        return response

@app.route("/productshop/products/all", methods=["GET"])
def get_all_products():
    """ Returns a list of all products in a beauty shop """

    all_products = product_manager.get_all_products()

    
    for product in all_products:
        response = app.response_class(
                status = 200,
                response = json.dumps(product.to_dict()),
                mimetype = 'application/json'
            )
    return response


@app.route("/productshop/products/all/<string:type>", methods=["GET"])
def get_products_by_type(type):
    """ Returns a list of products of specific type where the type is
        either "Makeup" or “Skincare" """
    
    try:
        all_products = product_manager.get_all_products_by_type(type)
        
        products=[]

        for product in all_products:
            the_product = product.to_dict()
            products.append(the_product)

        response = app.response_class(
                status=200,
                response =  json.dumps(products),
                mimetype="application/json")
        return response
    
    except ValueError as e:
        response = app.response_class(
            status=400,
            response=str(e)
        )
        return response
    
@app.route("/productshop/products/discount/<int:id>", methods=["PUT"])
def apply_discount_to_prod(id):
    """ Get the product by ID and apply discount to it """

    content = request.json

    try:
        discount = content["discount"]
        product_manager.apply_discount_to_prod(id, discount)

        response = app.response_class(
                status=200
            )
        return response
        
        
    except ValueError as e:
        response = app.response_class(
            status=404,
            response=str(e)
        )
        return response

if __name__ == "__main__":
    app.run(port = 5001)

