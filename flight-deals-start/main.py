# #This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import json
import os
from smtplib import *
from flight_data import FlightData
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager

flightdata=FlightData()
flightsearch=FlightSearch()
datamanager=DataManager()
flightsearch_data={}
IATA_CODE_LIST=[]

sheet_data=flightdata.get_data()['prices']
pprint(sheet_data)
origin='AUS'
#pprint(sheet_data)
message=[]
for row in sheet_data:
    if row['iataCode'] != '':
        lowest_target_price = row['lowestPrice']
        flight_data=flightsearch.cheapest_price(origin=origin,destination=row['iataCode'])

        if flight_data is None:
            print(f"No flights to {row['city']}")
        elif flight_data < lowest_target_price:
            message.append((f"The cheapest price we're sending you by email to {row['city']} is {flight_data}"))


with SMTP("smtp.gmail.com") as connection:
    password=os.environ['gmail_connection_password']
    connection.starttls()
    connection.login(user='georgehuffingtons@gmail.com', password=password)
    connection.sendmail(from_addr='georgehuffingtons@gmail.com',to_addrs='georgehuffingtons@gmail.com',msg=f"{message}")
