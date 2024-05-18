import requests
from datetime import datetime

# Replace with your actual API key
API_KEY = "342f332dd47791c622414afd6f44a7d2"

# Function to get latitude and longitude from location name using Geocoding API
def get_lat_lon(location):
    location = location.strip()  # Remove any leading or trailing spaces
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"
    response = requests.get(geocode_url)
    
    # Print debug information
    print(f"Geocode API URL: {geocode_url}")
    print(f"Geocode API Response Status Code: {response.status_code}")
    print(f"Geocode API Response: {response.text}")
    
    data = response.json()
    if response.status_code == 200 and data:
        return data[0]['lat'], data[0]['lon']
    else:
        print("Error: Could not retrieve location coordinates.")
        return None, None

# Function to get current weather data
def get_current_weather(lat, lon):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    response = requests.get(weather_url)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        print(f"Error: {response.status_code}, could not retrieve weather data.")
        return None

# Function to get 5-day weather forecast using 3-hour forecast endpoint
def get_forecast(lat, lon):
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    response = requests.get(forecast_url)
    data = response.json()
    
    # Print debug information for forecast
    print(f"Forecast API URL: {forecast_url}")
    print(f"Forecast API Response Status Code: {response.status_code}")
    print(f"Forecast API Response: {response.text}")
    
    if response.status_code == 200:
        return data
    else:
        print(f"Error: {response.status_code}, could not retrieve weather forecast.")
        return None

# Function to display current weather
def display_current_weather(data):
    print("Current Weather:")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Feels like: {data['main']['feels_like']}°C")
    print(f"Weather: {data['weather'][0]['description'].capitalize()}")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Wind Speed: {data['wind']['speed']} m/s")
    print(f"Pressure: {data['main']['pressure']} hPa")

# Function to display 5-day forecast
def display_forecast(data):
    print("5-Day Forecast (3-hour intervals):")
    for item in data['list']:
        date_time = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S')
        temp = item['main']['temp']
        weather = item['weather'][0]['description'].capitalize()
        print(f"{date_time}: {temp}°C, {weather}")

# Main function to run the app
def main():
    while True:
        print("Weather App")
        print("1. Check current weather")
        print("2. Check 5-day forecast")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1' or choice == '2':
            location = input("Enter location: ")
            lat, lon = get_lat_lon(location)
            if lat is None or lon is None:
                continue

        if choice == '1':
            weather_data = get_current_weather(lat, lon)
            if weather_data:
                display_current_weather(weather_data)
        
        elif choice == '2':
            forecast_data = get_forecast(lat, lon)
            if forecast_data:
                display_forecast(forecast_data)
        
        elif choice == '3':
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
