import os
from dotenv import load_dotenv
import requests

# Dictionary to map airline codes to names
Airline_Codename = {
    "AA": "American Airlines",
    "DL": "Delta Air Lines",
    "UA": "United Airlines",
    "WN": "Southwest Airlines",
    "AS": "Alaska Airlines",
    "B6": "JetBlue Airways",
    "F9": "Frontier Airlines",
    "NK": "Spirit Airlines",
    "BA": "British Airways",
    "LH": "Lufthansa",
    "AF": "Air France",
    "KL": "KLM Royal Dutch Airlines",
    "CX": "Cathay Pacific",
    "EK": "Emirates",       
    "QR": "Qatar Airways",
    "SQ": "Singapore Airlines",
    "JL": "Japan Airlines",
    "NH": "All Nippon Airways", 
    "VA": "Virgin Australia",
    "NZ": "Air New Zealand",
    "AC": "Air Canada",
    "HA": "Hawaiian Airlines",
    "6X": "Air Odisha",
}

Airport_Codes = {
    "DAL": "Dallas Love Field",
    "LAX": "Los Angeles International Airport",
    "JFK": "John F. Kennedy International Airport", 
    "ORD": "O'Hare International Airport",
    "ATL": "Hartsfield-Jackson Atlanta International Airport",
    "DFW": "Dallas/Fort Worth International Airport",
    "SFO": "San Francisco International Airport",
    "SEA": "Seattle-Tacoma International Airport",
    "MIA": "Miami International Airport",
    "DEN": "Denver International Airport",
    "LAS": "McCarran International Airport",
    "PHX": "Phoenix Sky Harbor International Airport",
    "BOS": "Logan International Airport",
    "IAH": "George Bush Intercontinental Airport",
    "EWR": "Newark Liberty International Airport",
    "CLT": "Charlotte Douglas International Airport",
    "MSP": "Minneapolis-Saint Paul International Airport",
    "DTW": "Detroit Metropolitan Wayne County Airport",

}

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
    print("Access token retrieved!")
    token_status = response.json().get('state') # Get the token status from the response
    print(f"Token Status: {token_status}")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("Welcome to the Flight Planner!")
else:
    print("Failed to retrieve access token")
    exit()

# Ask user for flight details
origin = input("Where would you like to depart, please enter airport code (ex: DAL): ").strip().upper() #strip() is used to remove any leading or trailing whitespace
if origin not in Airport_Codes: # Check if the origin airport code is valid
    print(f" '{origin}' is an invalid airport code. Please try again.")
    origin = input("Where would you like to depart, please enter airport code (ex: DAL): ").strip().upper()

destination = input("Where would you like to go? Please enter airport code (ex: LAX): ").strip().upper() #upper() is used to convert the input to uppercase
if destination not in Airport_Codes: # Check if the destination airport code is valid
    print(f" '{destination}' is an invalid destination airport code. Please try again.")
    destination = input("Where would you like to go? Please enter airport code (ex: LAX): ").strip().upper()
date = input("Enter departure date (YYYY-MM-DD): ").strip()
if not date: # Check if the date is empty
    print("Date cannot be empty. Please try again.")
    date = input("Enter departure date (YYYY-MM-DD): ").strip()
adults = input("How many adults will be flying?: ").strip()
if int(adults) <= 0:
    print(f"'{adults}' number of adults cannot fly. Please try again.")
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

if search_response.status_code == 200: # Check if the request was successful
    flight_offers = search_response.json().get('data')
    if not flight_offers:
        print("No flights found.")
        exit()
    print("Available Flights:")
    print("")
    
    for i, offer in enumerate(flight_offers, 1): # Enumerate through the flight offers
        # Gets information from the flight offer
        itinerary = offer['itineraries'][0] # Get the first itinerary from the offer
        segments = itinerary['segments'] # Get the segments of the itinerary
        num_stops = len(segments) - 1  # 0 stops = direct, 1 = one stop, etc.

        airline_code = segments[0]['carrierCode'] # Get the airline code from the first segment
        airline_name = Airline_Codename.get(airline_code, airline_code) # Get the airline name from the code, or use the code if not found
        total_cost = offer['price']['total']
        bookable_seats = offer.get('numberOfBookableSeats')
        airline_departure = segments[0]['departure']['iataCode'] # Get the departure airport code from the first segment
        airline_arrival = segments[-1]['arrival']['iataCode'] # Get the arrival airport code from the last segment
        departure_name = Airport_Codes.get(airline_departure, airline_departure)
        arrival_name = Airport_Codes.get(airline_arrival, airline_arrival)

        print(f"Flight {i}:")
        print("")
        print(f"  Airline: {airline_name} ({airline_code})")
        print(f"  Route: {departure_name} ({airline_departure}) to -> {arrival_name} ({airline_arrival})")
        print(f"  Bookable Seats: {bookable_seats}")
        print(f"  Total Stops: {num_stops}")
        print(f"  Total Cost: for {adults} adult ${total_cost}")
        print("-" * 82) # Print a separator line
        print("")
else:
    print("Failed to retrieve flight offers")
    exit()
