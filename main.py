import os
from dotenv import load_dotenv
import requests
from colorama import init, Fore, Style
import time

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
# Dictionary to map airport codes to names
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
init() # Initialize colorama for colored output


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
    print(Fore.GREEN +"Access token retrieved!")
    token_status = response.json().get('state') # Get the token status from the response
    print(Fore.GREEN + f"Token Status: {token_status}")
    print("")
    print("")
    
    print(Fore.MAGENTA + "=" * 82)
    print(Fore.RESET + r"""
                        __|__
                --o--o--( _ )--o--o--
                         / \
                                                        """)
    print(Fore.BLUE + Style.BRIGHT + "            Welcome to the Flight Planner!✈️")
    print(Fore.MAGENTA + "=" * 82)
    print("")
    print("")
else:
    print( Fore.RED +"Failed to retrieve access token")
    print(Fore.YELLOW + "Please check your AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET in the .env file.")
    time.sleep(5) # Wait for 5 seconds before exiting
    
    exit() # Exit the program if the token retrieval fails
while True:
# Ask user for flight details
    while True:
        origin = input(Fore.LIGHTBLUE_EX + "Where would you like to depart, please enter airport code" + Fore.GREEN + " (ex: DAL): " + Fore.RESET).strip().upper() #strip() is used to remove any leading or trailing whitespace
        if origin in Airport_Codes: # Check if the origin airport code is valid
            break # If valid, break the loop
        else:
            print(Fore.RED + f" '{origin}' is an invalid airport code. Please try again.")
    
    while True:
        destination = input(Fore.LIGHTBLUE_EX +"Where would you like to go? Please enter airport code" + Fore.GREEN + " (ex: LAX): " + Fore.RESET).strip().upper() #upper() is used to convert the input to uppercase
        if destination in Airport_Codes: # Check if the destination airport code is valid
            break # If valid, break the loop
        else:
            print(Fore.RED + f" '{destination}' is an invalid destination airport code. Please try again.")
        

    while True:
        date = input(Fore.LIGHTBLUE_EX + "Enter departure date, in this format " + Fore.GREEN + "(MM-DD-YYYY): " + Fore.RESET).strip()
        # Check if the date is in the correct format
        if len(date) == 10 and date[2] == '-' and date[5] == '-':
            month, day, year = date.split('-')
            # Check if month, day, and year are numbers
            if month.isdigit() and day.isdigit() and year.isdigit():
                month = int(month)
                day = int(day)
                year = int(year)
                # Check if the numbers are in valid ranges
                if 1 <= month <= 12 and 1 <= day <= 31 and len(str(year)) == 4 and year >= 2025:
                    # add leading zeros
                    if month < 10:
                        month_str = "0" + str(month)
                    else:
                        month_str = str(month)

                    if day < 10:
                        day_str = "0" + str(day)
                    else:
                        day_str = str(day)

                    api_date = str(year) + "-" + month_str + "-" + day_str
                    break
        print(Fore.RED + "Invalid date format. Please use MM-DD-YYYY.")

    while True:# Ask for the number of adults flying   
        adults = input(Fore.LIGHTBLUE_EX +"How many adults will be flying?: " + Fore.RESET).strip()
        if adults.isdigit() and int(adults) > 0:
            break
        else:
            print(Fore.RED + f"'{adults}' number of adults cannot fly. Please try again.")
        

    supported_currencies = ["USD", "EUR", "GBP", "CAD", "AUD", "JPY"]
    while True:
        currency = input(Fore.LIGHTBLUE_EX + "Enter preferred currency code " + ", Supported currencies: " 
                         + Fore.GREEN + f"{supported_currencies}" + Fore.LIGHTBLUE_EX + " default is " + Fore.GREEN + "USD): " + Fore.RESET).strip().upper()
        if currency == "":
            currency = "USD"
            break
        elif currency in supported_currencies:
            break
        else:
            print(Fore.RED + f"'{currency}' is not a supported currency. Please try again.")

    print(Fore.YELLOW +f"Searching flights from {origin} to {destination} on {date} for {adults} adults")

    # Searches Flights
    headers = {
        'Authorization': f'Bearer {access_token}', # Bearer token for authorization
        'Accept': 'application/json' # Accept header to specify the response format
    }

    params = {
        'originLocationCode': origin,
        'destinationLocationCode': destination,
        'departureDate': api_date, # Departure date in YYYY-MM-DD format
        'adults': adults,
        'currencyCode': currency, # Currency code for the prices
    }

    search_url = 'https://test.api.amadeus.com/v2/shopping/flight-offers' # URL to search for flight offers
    search_response = requests.get(search_url, headers=headers, params=params)

    if search_response.status_code == 200: # Check if the request was successful
        flight_offers = search_response.json().get('data')
        if not flight_offers:
            print(Fore.RED +"No flights found.")
            continue # If no flights found, go to the next loop

        print("")    
        print(Fore.GREEN +"All Available Flights:")
        print("")
        print(Fore.MAGENTA + "=" * 82)

        cheapest_flights = []
        
        for i, offer in enumerate(flight_offers, 1): # Enumerate through the flight offers
            #enumerate is a built-in Python function that lets you loop over a list to get both the index (number) and the value at the same time.
            # Gets information from the flight offer
            itinerary = offer['itineraries'][0] # Get the first itinerary from the offer
            segments = itinerary['segments'] # Get the segments of the itinerary
            airline_arrival = segments[-1]['arrival']['iataCode'] # Get the arrival airport code from the last segment

        # Only show flights that arrive at the requested destination
            if airline_arrival != destination:
                continue
            num_stops = len(segments) - 1  # 0 stops = direct, 1 = one stop

            airline_code = segments[0]['carrierCode'] # Get the airline code from the first segment
            airline_name = Airline_Codename.get(airline_code, airline_code) # Get the airline name from the code, or use the code if not found
            total_cost = offer['price']['total']
            bookable_seats = offer.get('numberOfBookableSeats')
            airline_departure = segments[0]['departure']['iataCode'] # Get the departure airport code from the first segment
            airline_arrival = segments[-1]['arrival']['iataCode'] # Get the arrival airport code from the last segment
            departure_name = Airport_Codes.get(airline_departure, airline_departure)
            arrival_name = Airport_Codes.get(airline_arrival, airline_arrival)

            arrival_time = segments[-1]['arrival']['at'] # Get the arrival time from the last segment
            departure_time = segments[0]['departure']['at'] # Get the departure time from the first segment
            
            if int(adults) > bookable_seats: # Check if the number of adults exceeds the number of bookable seats
                continue  # If it does, skip this flight offer

            # Store all relevant info for cheapest flight
            cheapest_flights.append({ #append adds an item to the end of a list
                "index": i,
                "airline_name": airline_name,
                "airline_code": airline_code,
                "departure_name": departure_name,
                "departure_code": airline_departure,
                "arrival_name": arrival_name,
                "arrival_code": airline_arrival,
                "bookable_seats": bookable_seats,
                "num_stops": num_stops,
                "total_cost": total_cost,
                "departure_time": departure_time,
                "arrival_time": arrival_time
            })
            
            print(Fore.WHITE + Style.BRIGHT +  f"✈️  Flight {i}:")
            print("")
            print(Fore.WHITE +  "🧳  Airline: " + Fore.BLUE + f"{airline_name} ({airline_code})")
            print(Fore.WHITE + f"    Route: " + Fore.BLUE + f"{departure_name} ({airline_departure}) to -> {arrival_name} ({airline_arrival})")
            print(Fore.WHITE + f"    Departure: " + Fore.BLUE + f"{departure_time}")
            print(Fore.WHITE + f"    Arrival: " + Fore.BLUE + f"{arrival_time}")
            print(Fore.WHITE + f"💺 Bookable Seats: " + Fore.BLUE + f"{bookable_seats}")
            print(Fore.WHITE + f"   Total Stops: " + Fore.BLUE + f"{num_stops}")
            print(Fore.WHITE + f"💲 Total Cost: " +  Fore.BLUE + f"for {adults} adult  ${total_cost} {currency}")
            print(Fore.MAGENTA + "=" * 82) # Prints a separator line
            print("")
        
        
        if not cheapest_flights:
            print(Fore.RED + "No valid flights found for your search.")
            continue
        # Find the flight with the lowest total cost
        cheapest = cheapest_flights[0]
        for flight in cheapest_flights: # Iterate through the list of cheapest flights
            if float(flight["total_cost"]) < float(cheapest["total_cost"]): # Compares the total cost of the current flight with the cheapest found so far
                cheapest = flight
        
        print(Fore.GREEN + Style.BRIGHT + "Cheapest Flight:")
        print("")
        print(Fore.WHITE + f"🧳 Airline: " + Fore.BLUE + f"{cheapest['airline_name']} ({cheapest['airline_code']})")
        print(Fore.WHITE + f"   Route: " + Fore.BLUE + f"{cheapest['departure_name']} ({cheapest['departure_code']}) to -> {cheapest['arrival_name']} ({cheapest['arrival_code']})")
        print(Fore.WHITE + f"   Departure: " + Fore.BLUE + f"{cheapest['departure_time']}")
        print(Fore.WHITE + f"   Arrival: " + Fore.BLUE + f"{cheapest['arrival_time']}")
        print(Fore.WHITE +f"💺  Bookable Seats: " + Fore.BLUE + f"{cheapest['bookable_seats']}")
        print(Fore.WHITE + f"   Total Stops: " + Fore.BLUE + f"{cheapest['num_stops']}")
        print(Fore.WHITE +f"💲  Total Cost: " +  Fore.BLUE + f"for {adults} adult  ${cheapest['total_cost']} {currency}")
        print(Fore.MAGENTA + "=" * 82)
        print("")
    else:
        print(Fore.RED +"Failed to retrieve flight offers")
        print(Fore.YELLOW + "API response details: " + search_response.text)



    # Ask user if they want to search for another flight
    again = input(Fore.CYAN +"Would you like to search for another flight? (y/n): ").strip().lower()
    print("")
    if again != "y":
        print("")
        print(Fore.RED +"Thank you for using the Flight Planner! Bye bye")
        exit() # Exit the program if the user does not want to search for another flight