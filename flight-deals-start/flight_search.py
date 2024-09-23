import os
import requests
import dotenv
from pprint import pprint
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pprint import pprint

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        load_dotenv()
        self.API_KEY=os.environ['new_API_KEY']
        self.API_SECRET=os.environ['new_API_SECRET']

        self.tomorrow = datetime(2024, 9, 25)

    def get_new_token(self):
        header={'content-type':'application/x-www-form-urlencoded'}
        body= {"grant_type": "client_credentials",
               'client_id':self.API_KEY,
                    'client_secret':self.API_SECRET,}
        TOKEN_ENDPOINT="https://test.api.amadeus.com/v1/security/oauth2/token"
        response = requests.post(url=TOKEN_ENDPOINT, data=body)

        if response.status_code == 200:
            token = response.json()['access_token']
            return token


    def get_destination_code(self,keyword):
        CODE_ENDPOINT="https://test.api.amadeus.com/v1"
        body={"keyword":keyword,  "max": "2",
            "include": "AIRPORTS",}
        header={"Authorization":f"Bearer {self.get_new_token()}"}
        response=requests.get(url=f"{CODE_ENDPOINT}/reference-data/locations/cities",params=body,headers=header)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching destination code: {response.status_code} {response.text}")
            return None

    #This will search for all flights from origin to destination on amadeus using their api
    def flight_search(self,origin,destination,date):

        self.origin=origin
        FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2"
        FLIGHT_URL=f"{FLIGHT_ENDPOINT}/shopping/flight-offers"
        FLIGHT_BODY={"originLocationCode":self.origin,"destinationLocationCode":destination,"departureDate":date,
                     "adults":1,"currencyCode":"USD","max":1}
        FLIGHT_HEADER={"Authorization":f"Bearer {self.get_new_token()}"}

        flight_search_response = requests.get(url=FLIGHT_URL, params=FLIGHT_BODY, headers=FLIGHT_HEADER)

        if flight_search_response.status_code == 200:
            self.flight_data = flight_search_response.json()
            #pprint(self.flight_data)

        try:
            flight_price = flight_search_response.json()["data"][0]["price"]["total"]
            return float(flight_price)
        except (KeyError, IndexError) as e:
            print(f"Error retrieving flight for {destination} on {date}: {e}")
            return None

    #This will find the cheapest price for next x number of days
    def cheapest_price(self,origin,destination):
        self.days=1
        self.cityflights=[]
        self.origin = origin
        num_days=2

        while self.days < num_days:
            new_Date = (self.tomorrow + timedelta(days=self.days)).strftime("%Y-%m-%d")
            flight_price=self.flight_search(origin=self.origin,destination=destination,date=new_Date)

            if flight_price:
                self.cityflights.append(flight_price)
            self.days+=1

        print(f"The prices on the given dates from {self.origin} to {destination} between {self.tomorrow} and {new_Date} are : {self.cityflights}")

        if self.cityflights:
            cheapest = min(self.cityflights)  # Find the cheapest price
            print(f"Cheapest flight: {cheapest}")
            return cheapest
        else:
            print("No flights found in the given range.")
            return None

























































