from flask import jsonify
from flask import request
from flask import abort
from flask_restful import Resource
from services.strapi import strapi
import requests

## /recipes routes
class RecipesAPI(Resource):
    def get(self):
        recipes = strapi.get('/recipes')
        return jsonify(recipes)
    def post(self):
        body = request.json
        try:
            new_recipe = strapi.post('/recipes', {**body})
            return jsonify(new_recipe)
        except requests.exceptions.HTTPError as err:
            return {'error': 'Could not create recipe : %s' % err}, 400
        

## /users/<userId> routes
class RecipeAPI(Resource):
    def get(self, recipeId):
        try:
            recipe = strapi.get('/recipes/' + recipeId)
            return jsonify(recipe)
        except requests.exceptions.HTTPError as err:
            return {'error': 'Recipe not found : %s' % err}, 404
        except Exception as e:
            print(e)
            return {'error': 'Internal error : %s' % e}, 500
        