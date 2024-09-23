#import libraries
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
from flight_search import FlightSearch

#load env
load_dotenv()
MY_ENV_VAR = os.getenv('MY_ENV_VAR')
print(MY_ENV_VAR)

#create objects from classes to be used in this code
flight_search=FlightSearch()


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.url='https://api.sheety.co/597b94e0d98c07162041e0f82fc2f52a/copyOfFlightDeals/prices'
        self.users_url= 'https://api.sheety.co/597b94e0d98c07162041e0f82fc2f52a/copyOfFlightDeals/users'
        self.username = os.environ["SHEETY_USRERNAME"]
        self.password = os.environ["SHEETY_PASSWORD"]
        self.authentication=HTTPBasicAuth(self.username,self.password)
        self.new_cityCode=[]
        self.new_iataCode=[]
        self.is_direct = self.direct_indirect_flights()




    #Add data to users sheet as users input their first name , last name, and email when you run main.py
    def post_data(self, new_user):
        response = requests.post(url=self.users_url, json=new_user, auth=self.authentication)
        if response.status_code == 200:  # Created
            print("User added successfully.")
        else:
            print(f"Failed to add user: {response.status_code}, {response.text}")
        return response


    #This will look at the number of segments in each flight but have not helped much in the final code (it was part of exercise)
    def new_data(self):

        segments = flight_search.flight_data['data'][0]['itineraries'][0]['segment']
        for segment in segments:
            arrival_iata = segment['arrival']['iataCode']
            departure_iata = segment['departure']['iataCode']
            # Get city codes from dictionaries
            arrival_city_code = flight_search.flight_data['dictionaries']['locations'][arrival_iata]['cityCode']
            departure_city_code = flight_search.flight_data['dictionaries']['locations'][departure_iata]['cityCode']

            # Append city codes to the list
            self.new_cityCode.append(arrival_city_code)
            self.new_iataCode.append(arrival_iata)


    #This will get customer emails from the sheet
    def get_Customer_emails(self,id):
        response=requests.get(url=f"{self.users_url}", headers={'Authorization': 'Basic Z2VvcmdlaHVmZmluZ3RvbnNAZ21haWwuY29tOktoYTFpZmVoNzg='})
        data1=response.json()
        print(data1)
        if 'users' in data1:
            self.email = data1['users'][0]['emailAddress']
            print(f"Customer email: {self.email}")
        else:
            print("Warning: 'users' key not found in data.")



    def direct_indirect_flights(self):
        if not hasattr(flight_search, 'flight_data') or not flight_search.flight_data.get("data"):
            return True  # Default to direct if no flight data is available

        segments = flight_search.flight_data["data"][0].get('itineraries', [{}])[0].get('segments', [])

        self.num_of_stops = len(segments)  # Count stops

        if self.num_of_stops == 1:  # True if direct, False if indirect
            self.is_direct=True
        else:
            self.is_direct=False
        return self.is_direct
