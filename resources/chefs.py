from flask import jsonify
from flask import request
from flask import abort
from flask_restful import Resource
from services.strapi import strapi
import requests
from flask import current_app

## /chefs routes
class ChefsAPI(Resource):
    def get(self):
        chefs = strapi.get('/chefs')
        return jsonify(chefs)
    def post(self):
        body = request.json
        try:
            new_chef = strapi.post('/chefs', {**body})
            return jsonify(new_chef)
        except requests.exceptions.HTTPError as err:
            return {'error': 'Could not create chef : %s' % err}, 400

## /chefs/<chefId> routes
class ChefAPI(Resource):
    def get(self, chefId):
        try:
            chef = strapi.get('/chefs/' + chefId)
            return jsonify(chef)
        except requests.exceptions.HTTPError as err:
            return {'error': 'Chef not found : %s' % err}, 404
        except Exception as e:
            print(e)
            return {'error': 'Internal error : %s' % e}, 500

class ChefUpdateAPI(Resource):
    def put(self, chefId, recipeId):
        api_key = request.headers.get('API_KEY')
        print(api_key)
        print(current_app.config["API_KEY"])
        if api_key != current_app.config["API_KEY"]:
            return {'error': 'API key invalid : %s' % api_key}, 401
        try:
            chef = strapi.get('/chefs/' + chefId)
            recipe = strapi.get('/recipes/' + recipeId)
        except requests.exceptions.HTTPError as err:
            return {'error': 'Chef or recipe not found : %s' % err}, 404
        print(chef["recipes"])
        recipes = chef["recipes"]
        recipes.append(recipe["id"])
        try:
            updated_chef = strapi.put('/chefs/' + chefId, { "recipes": recipes})
        except requests.exceptions.HTTPError as err:
            return {'error': 'Couldnt update chef : %s' % err}, 400
        return jsonify(updated_chef)
        