# #This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

#import methods from objects and libraries
from flight_data import FlightData
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager
from pprint import pprint
import requests


#Create objects from different Classes
flightdata=FlightData()
flightsearch=FlightSearch()
datamanager=DataManager()
#flightsearch_data={}
notification_manager=NotificationManager()
IATA_CODE_LIST=[]


# pprint entire google sheet data (prices, users)
sheet_data_prices=flightdata.get_price_data()['prices']
pprint(sheet_data_prices)
sheet_data_users=flightdata.get_users_data()['users']
pprint(sheet_data_users)

#input user data
print('what is your first name')
First_Name = input()
print('what is your last name')
Last_Name = input()
print('what is your email')
Email_Address = input()
new_user={'user': {'firstName':First_Name,'lastName':Last_Name,'emailAddress':Email_Address}}

#add created user to google sheet
if new_user['user']['emailAddress'] not in [user['emailAddress'] for user in sheet_data_users]:
    datamanager.post_data(new_user)

#state your origin airport
origin='LHR'

#Create a list of messages to email cheapest prices to users listed on sheet
message=[]


#find cheapest prices
for row in sheet_data_prices:
    if row['iataCode'] != '':
        lowest_target_price = row['lowestPrice']
        flight_data=flightsearch.cheapest_price(origin=origin,destination=row['iataCode'])
        if flight_data is None:
            print(f"No flights to {row['city']}")
        elif flight_data < lowest_target_price:
            message.append((f"The cheapest price we're sending you by email to {row['city']} is {flight_data}."))
            final_message = "\n".join(message)
        #optional: print(f"The cheapest price we're sending you by email to {row['city']} is {flight_data}")


for row in sheet_data_users:
    customer_email=row['emailAddress']
    notification_manager.send_emails(message=final_message, destination_address=customer_email)
