import requests


class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        self.sheety_url = 'https://api.sheety.co/597b94e0d98c07162041e0f82fc2f52a/copyOfFlightDeals/prices'
        self.flight_prices = requests.get(url=self.sheety_url, headers={
            'Authorization': 'Basic Z2VvcmdlaHVmZmluZ3RvbnNAZ21haWwuY29tOktoYTFpZmVoNzg='})
        self.sheety_url_users = 'https://api.sheety.co/597b94e0d98c07162041e0f82fc2f52a/copyOfFlightDeals/users'
        self.flight_users = requests.get(url=self.sheety_url_users, headers={
            'Authorization': 'Basic Z2VvcmdlaHVmZmluZ3RvbnNAZ21haWwuY29tOktoYTFpZmVoNzg='})

    def get_price_data(self):
        return self.flight_prices.json()

    def get_users_data(self):
        return self.flight_users.json()
