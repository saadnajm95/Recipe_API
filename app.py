from flask import Flask
from flask import jsonify
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from database.db import initialize_db
from services.strapi import initialize_strapi
from resources.users import UsersApi, UserApi, UserMeApi, UserRecipesApi, UserMeGoalApi, UserManualProductApi, UserProductCodeApi, UserMeStatsApi
from resources.auth import SignupApi, LoginApi
from resources.recipes import RecipesAPI, RecipeAPI
from resources.chefs import ChefsAPI, ChefAPI, ChefUpdateAPI
from resources.products import ProductsAPI, ProductAPI

app = Flask(__name__, instance_relative_config=True)



app.config['PROPAGATE_EXCEPTIONS'] = True

# Loads configuration from config.py
app.config.from_object('config')

app.config['MONGODB_SETTINGS'] = {
    'host': app.config['MONGO_URI']
}

## Initialisation des modules 

initialize_db(app)
initialize_strapi(app)
bcrypt = Bcrypt(app)
api = Api(app)
jwt = JWTManager(app)

## Declaration of API routes

api.add_resource(UsersApi, '/users')
api.add_resource(UserMeApi, '/users/me')
api.add_resource(UserRecipesApi, '/users/recipes')
api.add_resource(UserApi, '/users/<userId>')

api.add_resource(SignupApi, '/auth/signup')
api.add_resource(LoginApi, '/auth/login')

api.add_resource(RecipesAPI, '/recipes')
api.add_resource(RecipeAPI, '/recipes/<recipeId>')

api.add_resource(ChefsAPI, '/chefs')
api.add_resource(ChefAPI, '/chefs/<chefId>')
api.add_resource(ChefUpdateAPI, '/chefs/<chefId>/recipe/<recipeId>')


api.add_resource(UserMeGoalApi, '/users/me/goal')
api.add_resource(UserManualProductApi, '/users/manual/product')
api.add_resource(UserProductCodeApi, '/users/product/<bar_code>')
api.add_resource(UserMeStatsApi, '/users/me/stats/<date>')

api.add_resource(ProductsAPI, '/products')
api.add_resource(ProductAPI, '/products/<bar_code>')



@app.route('/')
def hello_world():
    return jsonify({"message": "Hello World from Python"})



