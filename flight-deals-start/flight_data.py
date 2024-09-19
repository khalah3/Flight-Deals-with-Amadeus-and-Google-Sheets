import requests
from pprint import pprint
class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        self.sheety_url='https://api.sheety.co/597b94e0d98c07162041e0f82fc2f52a/copyOfFlightDeals/prices'
        self.flight_data=requests.get(url=self.sheety_url, headers={'Authorization':'Basic Z2VvcmdlaHVmZmluZ3RvbnNAZ21haWwuY29tOktoYTFpZmVoNzg='})

    def get_data(self):
        return self.flight_data.json()