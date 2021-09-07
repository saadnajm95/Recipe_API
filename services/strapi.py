
import requests

class Strapi:
    url= ""
    def get_headers(self):
        payload = {
            "identifier": "hetic@test.com",
            "password": "Hetic2022"
        }
        response = requests.post(url = self.url + "/auth/local", data=payload)
        user_info = response.json()
        token = user_info["jwt"]
        return {
            "Authorization": "Bearer " + token
        }

    def get(self, route):
        try:
            response = requests.get(url = self.url + route)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err
        return response.json()

    def post(self, route, payload):
        try:
            response = requests.post(url = self.url + route, data=payload, headers=self.get_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err
        return response.json()
    
    def put(self, route, payload):
        try:
            response = requests.put(url = self.url + route, data=payload, headers=self.get_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err
        return response.json()

strapi = Strapi()

def initialize_strapi(app):
    strapi.url = app.config["STRAPI_HOST"]
