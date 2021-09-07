from flask import jsonify
from flask import request
from flask import abort
from flask_restful import Resource
from database.models import User, Product, ProductQuantity, DailyIntake
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from resources.products import getProductByCode
## /users routes
class UsersApi(Resource):
    def get(self):
        users = User.objects()
        return jsonify(users)

    def delete(self):
        users = User.objects().delete()
        return jsonify({message: "all users deleted" % userId})

## /users/<userId> routes
class UserApi(Resource):
    def get(self, userId):
        try:
            user = User.objects.get(id=userId)
            return jsonify(user)
        except Exception as e:
            print(e)
            return {'error': 'User not found : %s' % e}, 404
    
    def put(self, userId):
        body = request.json
        try:
            User.objects.get(id=userId).update(**body)
            return jsonify(User.objects.get(id=userId))
        except Exception as e:
            print(e)
            return {'error': 'User update failed : %s' % e}, 400  

    def delete(self, userId):
        try:
            User.objects.get(id=userId).delete()
            return jsonify({message: "user %s deleted" % userId})
        except Exception as e:
            print(e)
            return {'error': 'Couldnt delete user : %s' % e}, 400

## /users/me
class UserMeApi(Resource):
    @jwt_required()
    def get(self):
        try:
            # extract info from the jwt token
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            return jsonify(user)
        except Exception as e:
            print(e)
            return {'error': 'Internal error : %s' % e}, 500     

## /users/recipes
class UserRecipesApi(Resource):
    @jwt_required()
    def put(self):
        body = request.json
        try:
            # extract info from the jwt token
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            for r in body["recipes"]:
                ## appeller strapi pour récupérer la recette
                user.recipes.append(r)
            user.save()
            return jsonify(user)
        except Exception as e:
            print(e)
            return {'error': 'Internal error : %s' % e}, 500 

## PUT /users/me/goal
class UserMeGoalApi(Resource):
    @jwt_required()
    def put(self):
        body = request.json
        try:
            # extract info from the jwt token
            user_id = get_jwt_identity()           
            user = User.objects.get(id=user_id)
            user.dailyGoal = body["goal"]
            user.save()
            return jsonify(user)
        except Exception as e:
            print(e)
            return {'error': 'Internal error : %s' % e}, 500 
    

##PUT /users/manual/product
class UserManualProductApi(Resource):
    @jwt_required()
    def put(self):
        body = request.json
        product = Product(**body)
        productQuantity = ProductQuantity()
        try:         
            product.name = body['name']
            product.description = body['description']
            product.caloriesByPortion = body['caloriesByPortion']
            product.caloriesBy100gr = body['caloriesBy100gr']
            product.save()

            productQuantity.productId = product
            productQuantity.unit = body['unit']
            productQuantity.quantity = body['amount']

        except Exception as e:
            print(e)
            return {'error': 'Internal error : %s' % e}, 500
        if body.get('date') != None:
            return jsonify(createDailyIntake(productQuantity, datetime.strptime(body.get('date'), '%Y-%m-%d').date()))
        else:
            return jsonify(createDailyIntake(productQuantity))


def createDailyIntake(productQuantity, date=datetime.now().date()):
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if DailyIntake.objects.filter(userId=user, date=date):
            dailyIntake = DailyIntake.objects.get(userId=user, date=date)
            dailyIntake.products.append(productQuantity)
        else:
            dailyIntake = DailyIntake()
            dailyIntake.userId = user
            dailyIntake.date = date
            dailyIntake.products.append(productQuantity)
        dailyIntake.save()
    except Exception as err:
        print(err)
        return {'error': 'Internal error : %s' % err}, 500
    return dailyIntake


class UserProductCodeApi(Resource):
    @jwt_required()
    def put(self):
        body = request.json
        productByCode = None
        productQuantity = ProductQuantity()
        try:
            productByCode = getProductByCode(bar_code)
            product = ProproductByCode(**productByCode)
            product.save()
            return jsonify(product)
        except AttributeError as err:
            return {'error': 'Product not found.'}, 404
            # extract info from the jwt token
            user_id = get_jwt_identity()           
            user = User.objects.get(id=user_id)

            productQuantity.productId = product
            productQuantity.unit = body['unit']
            productQuantity.quantity = body['amount']

            user.save()
            return jsonify(user)
        except Exception as e:
            print(e)
            return {'error': 'Internal error : %s' % e}, 500
        if body.get('date') != None:
            return jsonify(createDailyIntake(productQuantity, datetime.strptime(body.get('date'), '%Y-%m-%d').date()))
        else:
            return jsonify(createDailyIntake(productQuantity))



class UserMeStatsApi(Resource):
    @jwt_required()
    def get(self):
        daily_result = None
        daily_goal = None
        daily_intake =None
        try:
            # extract info from the jwt token
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            daily_goal = User.objects.get(dailyGoal)
            daily_intake = DailyIntake.objects.get(daily_intake)
            daily_result = User.objects.get(daily_intake - daily_goal)
            return jsonify(daily_goal, daily_intake, daily_result)
        except Exception as e:
            print(e)
            return {'error': 'Internal error : %s' % e}, 500 


