from flask_mongoengine import MongoEngine

# MongoEngine documentation : 
# http://docs.mongoengine.org/guide/index.html
db = MongoEngine()

def initialize_db(app):
    db.init_app(app)