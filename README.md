# Flight-Planner2.0
This project lets users request flight data for specific dates and airports

In order to use this application you will need to make an account on https://developers.amadeus.com/
Once doing so you be given an API Key and API Secret. Create an .env file where you place your Amadeus given API key and secret,  Line 1. AMADEUS_CLIENT_ID="API key", Line 2. AMADEUS_CLIENT_SECRET="API Secret". A git ignore has already been set up to ignore your .env file so that your keys are kept off github. Also be aware that this program uses python-dotenv library so you will need to install  "pip install python-dotenv", as well uses request library so you will need to install "pip install requests" as well. These are all the steps needed to run this program . Use "python main.py" to start the program it will give you feedback "Access token retrieved!" and "Token Status: approved" if the API keys from Amadeus were set up correctly. Next you simply type in your airline code of where you would like to depart and where you want to go. You will be prompted to enter a departure date and how  many adults will be flying. Once given the following information you will get feedback for all the flights from the specified airports on that date. The feedback will include the following:

Airline: 
Route: 
Bookable Seats: 
Total Stops: 
Total Cost: 