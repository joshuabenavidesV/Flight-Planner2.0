# ✈️ Flight-Planner2.0 🗺️

This project lets users search for available flights between major airports on specific dates, using live data from the Amadeus API.

## ✨ Features

- 🔎 Search for flights between major US airports on specific dates
- 🌐 Live flight data from the Amadeus API
- 👨‍👩‍👧‍👦 Only shows flights with enough bookable seats for your group
- 🛫 Displays airline, route, departure/arrival times, stops, seats, and total cost
- 🎨 Colorful, easy-to-read terminal output
- ⚙️ Simple setup with environment variables and pip
## Getting Started

1. **Create an Amadeus Developer Account**  
   Sign up at [Amadeus for Developers](https://developers.amadeus.com/) to get your API Key and API Secret.

2. **Set Up Your Environment Variables**  
   Create a `.env` file in your project directory with the following lines (replace with your actual credentials):
   ```
   AMADEUS_CLIENT_ID="your_api_key"
   AMADEUS_CLIENT_SECRET="your_api_secret"
   ```
   > **Note:** `.env` is already in `.gitignore` to keep your keys safe.

3. **Install Required Libraries**  
   Open a terminal and run:
   ```
   pip install -r requirements.txt
   ```

4. **Run the Application**  
   Start the program with:
   ```
   python main.py
   ```
   If your API keys are set up correctly, you will see:
   - ✅ `Access token retrieved!`
   - ✅ `Token Status: approved`

## 📝 How to Use

- Enter the **airport code** for your departure and destination (e.g., `DAL` for Dallas Love Field, `LAX` for Los Angeles International).
- Enter your **departure date** in `MM-DD-YYYY` format.
- Enter the **number of adults** flying.

The program will display all available flights that match your criteria, including only those with enough bookable seats for your group.

### 🛩️ Flight Information Displayed

- 🏢 **Airline**
- 🗺️ **Route**
- ⏰ **Departure & Arrival Times**
- 💺 **Bookable Seats**
- 🔁 **Total Stops**
- 💲 **Total Cost**
---

🎉 **Enjoy planning your next trip!** 🌍