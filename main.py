import os
from dotenv import load_dotenv
import requests

load_dotenv() # Load environment variables from .env file

client_id = os.getenv('AMADEUS_CLIENT_ID')
client_secret = os.getenv('AMADEUS_CLIENT_SECRET')

token_url = 'https://test.api.amadeus.com/v1/security/oauth2/token' # URL to get the access token
headers = {
    'Content-Type': 'application/x-www-form-urlencoded' # Content type for the request
}
data = { # Data to be sent in the request
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
}

response = requests.post(token_url, headers=headers, data=data) # Makes a POST request to get the access token

if response.status_code == 200:
    access_token = response.json().get('access_token') # Get the access token from the response
    print("Access token retrieved successfully!")
    token_status = response.json().get('state') # Get the token status from the response
    print(f"Token Status: {token_status}")
    print("Welcome to the Flight Search App!")
else:
    print("Failed to retrieve access token")
    exit()

# Ask user for flight details
origin = input("Where would you like to depart, please enter airport code (ex: DAL): ").strip().upper() #strip() is used to remove any leading or trailing whitespace
destination = input("Where would you like to go? Please enter airport code (ex: LAX): ").strip().upper() #upper() is used to convert the input to uppercase
date = input("Enter departure date (YYYY-MM-DD): ").strip()
adults = input("How many adults will be flying?: ").strip()

print(f"Searching flights from {origin} to {destination} on {date} for {adults} adults")

# Searches Flights
headers = {
    'Authorization': f'Bearer {access_token}', # Bearer token for authorization
    'Accept': 'application/json' # Accept header to specify the response format
}

params = {
    'originLocationCode': origin,
    'destinationLocationCode': destination,
    'departureDate': date,
    'adults': adults,
    'currencyCode': 'USD',
}

search_url = 'https://test.api.amadeus.com/v2/shopping/flight-offers' # URL to search for flight offers
search_response = requests.get(search_url, headers=headers, params=params)

if search_response.status_code == 200:
    flight_offers = search_response.json().get('data')
    print(f" Flights {(flight_offers)}") # Displays the flight offers
else:
    print("Failed to retrieve flight offers")
    exit()