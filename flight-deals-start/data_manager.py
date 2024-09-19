import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()
MY_ENV_VAR = os.getenv('MY_ENV_VAR')

print(MY_ENV_VAR)
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.url='https://api.sheety.co/597b94e0d98c07162041e0f82fc2f52a/copyOfFlightDeals/prices'
        self.username = os.environ["SHEETY_USRERNAME"]
        self.password = os.environ["SHEETY_PASSWORD"]
        self.authentication=HTTPBasicAuth(self.username,self.password)




    def put_data(self,data,id):
        requests.put(url=f"{self.url}/{id}",json=data, auth=self.authentication)
        response=  requests.put(url=f"{self.url}/{id}",json=data,auth=self.authentication)
        #print(f"Response Status Code: {response.status_code}")
        #print(f"Response JSON: {response.json()}")
        return response  # Return the response object for further debugging




