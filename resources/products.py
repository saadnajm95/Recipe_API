from flask import jsonify
from flask import request
from flask import abort
from flask_restful import Resource
from services.strapi import strapi
from database.models import Product, ProductQuantity, DailyIntake
import requests
from flask import current_app
from flask import json, Response

## /products routes
class ProductsAPI(Resource):
    def get(self):
        products = Product.objects()
        return jsonify(products)
    def post(self):
        body = request.json
        try:
            new_product = Product.post('/products', {**body})
            return jsonify(new_product)
        except requests.exceptions.HTTPError as err:
            return {'error': 'Could not create product : %s' % err}, 400   

## /products/<bar_code> routes
class ProductAPI(Resource):
    def get(self, bar_code):
        result = None
        try:
            result = getProductByCode(bar_code)
            product = Product(**result)
            product.save()
            return jsonify(product)
        except AttributeError as err:
            return {'error': 'Product not found.'}, 404
        except Exception as e:
            return {'error': 'Couldnt create product because : %s' % e}, 500


def getProductByCode(bar_code):
        response = requests.get(f'https://world.openfoodfacts.org/api/v0/product/{bar_code}.json')
        #response = requests.get(f'{current_app.config["OPENFOODFACT_URL"]}/api/v0/product/{bar_code}.json')
        product = response.json()
        return {
            "name" : product.get('product').get('product_name'),
            "description" : product.get('product').get('generic_name_fr'),
            "barCode": product.get('code'),               
            "caloriesByPortion" : float(product.get('product').get('nutriments').get('energy-kcal_serving')) if product.get('product').get('nutriments').get('energy-kcal_serving') else None,
            "caloriesBy100gr" : int(product.get('product').get('nutriments').get('energy-kcal_100g')) if product.get('product').get('nutriments').get('energy-kcal_100g') else None
            }    
       