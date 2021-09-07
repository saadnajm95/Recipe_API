from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Document):
  email = db.EmailField(required=True, unique=True)
  password = db.StringField(required=True, min_length=6)
  firstName = db.StringField()
  lastName = db.StringField()
  #recipes = db.ListField(db.IntField())
  dailyGoal = db.IntField(min_value=0) 
  def hash_password(self):
   self.password = generate_password_hash(self.password).decode('utf8')
 
  def check_password(self, password):
   return check_password_hash(self.password, password)

class Product(db.Document):
  name = db.StringField(required=True)
  description = db.StringField(required=False)
  barCode = db.StringField(unique=True, sparse=True)
  caloriesByPortion=db.IntField(required=True,min_value=0)
  caloriesBy100gr=db.IntField(required=True,min_value=0)


class ProductQuantity(db.EmbeddedDocument):
  productId=db.ReferenceField(Product)#
  unit=db.StringField()#
  quantity=db.IntField(min_value=0)
  def get_calories_total(self):
    return self.quantity*self.productId.caloriesByPortion



class DailyIntake(db.Document): 
  userId = db.ReferenceField(User)
  date = db.DateTimeField(default=datetime.now().date())
  products = db.ListField(db.EmbeddedDocumentField(ProductQuantity))
  def getTotalDailyIntake(self):
    list_total_dailyintake_portion = [i.quantity*i.productId.caloriesByPortion for i in self.products if i.unit=='portion']
    list_total_dailyintake_gram = [i.quantity/100*i.productId.caloriesBy100gr for i in self.products if i.unit=='gram']
    return sum(list_total_dailyintake_portion + list_total_dailyintake_gram)