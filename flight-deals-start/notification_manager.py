from smtplib import SMTP
import os

class NotificationManager:

    def __init__(self):
        pass

    #This code will initiate email with the message in main.py
    def send_emails(self,message,destination_address):
        with SMTP("smtp.gmail.com") as connection:
            password = os.environ['gmail_connection_password']
            connection.starttls()
            connection.login(user='georgehuffingtons@gmail.com', password=password)
            connection.sendmail(from_addr='georgehuffingtons@gmail.com', to_addrs=destination_address,msg=f"{message}")
