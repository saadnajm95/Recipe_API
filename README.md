# Projet final pour Déploiement API Docker&Cloud

# Recipes API

## Install API without Docker

1. Activate a conda or a virtualenv for the project

2. Install dependecies :
```
pip install -r requirements.txt
```
For windows users, if you have issues with the pip install command, you can try :
```
pip install -r requirements.txt --user
```

3. Launch the API :
```
flask run --port=3000
```

## Install with Docker

1. Build the docker image of the API :
```
docker build --tag recipes-api .
```

2. Create a Docker network that will be shard by your containers : 
```
docker network create --driver=bridge db-network
```

3. Create a Docker volume that will be used by your database container :
```
docker volume create mg-data
```

4. Launch the container of your database with the network and volume options :
```
docker run --name mongo-recipe -p 27017:27017 --rm --network db-network -v mg-data:/data/db -d mongo 
```

5. Run the API container with the network option and the environnement variable to connect to your database container : 
```
docker run --name recipes-api -p 3000:3000 --rm -d --network db-network -e MONGO_URI=mongodb://mongo-recipe:27017/app md4-recipe
```

6. Test your setup with a curl command or directly in your browser, it should return an array of users:
```
curl localhost:3000/users
```

## Install with docker-compose

1. Launch your solution:
```
docker-compose up
```

2. Test your setup with a curl command or directly in your browser, it should return an array of users:
```
curl localhost:3000/users
```

## API Structure

* API initialization in app.py
* Routes logic in `/resources`
* Database initialization and models in `/database`
* Services defined in `/services`

## Environment

You must set these different variables in a .env file :
```
JWT_SECRET_KEY=
MONGO_URI=
STRAPI_HOST=
```

## For development

When you are adding new features to the API, it's easier to work directly with flask to reload your code changes, so you can just launch the mongodb database service with :
```
docker-compose up -d mongodb
```

And afterwards, launch your API with Flask : 
```
flask run --port=3000
```
## Use mongo-express to manage MongoDB

* Launch the mono-express service with :
```
docker-compose up -d mongo-express
```

* Open http://localhost:8081 in your browser and login with :
```
username: admin
password: password
```

