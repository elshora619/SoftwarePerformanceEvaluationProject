import math
import cProfile
import pstats
from io import StringIO
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import requests

app = FastAPI()

# In-memory storage for weather data
weather_data = []

# Middleware for profiling
@app.middleware("http")
async def profile_middleware(request: Request, call_next):
    # Initialize cProfile
    profiler = cProfile.Profile()
    profiler.enable()  # Start profiling

    response = await call_next(request)  # Process the request

    profiler.disable()  # Stop profiling

    # Save profiling results to a string
    result = StringIO()
    stats = pstats.Stats(profiler, stream=result)
    stats.strip_dirs()  # Remove extraneous path info
    stats.sort_stats(pstats.SortKey.TIME)  # Sort by cumulative time
    stats.print_stats()  # Print profiling stats to the string

    # Log the profiling results to the console
    print("Profiling Results:\n", result.getvalue())

    return response

# Function to calculate the distance between two geo-locations using the Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    lat1, lat2 = math.radians(lat1), math.radians(lat2)
    lon1, lon2 = math.radians(lon1), math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Data model for weather submission
class WeatherData(BaseModel):
    latitude: float = Field(..., description="Geo-location's latitude")
    longitude: float = Field(..., description="Geo-location's longitude")
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Humidity percentage (0-100)")

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather API"}

# Favicon route (optional to prevent 404 errors for favicon.ico requests)
@app.get("/favicon.ico")
async def favicon():
    return {"detail": "No favicon available"}

# Endpoint to submit weather data
@app.post("/data")
def submit_weather_data(data: WeatherData):
    """
    Endpoint to receive a single weather data point.
    Example payload:
    {
      "latitude": 51.5074,
      "longitude": -0.1278,
      "temperature": 15.5,
      "humidity": 80
    }
    """
    weather_data.append(data.dict())
    return {"message": "Weather data submitted successfully"}

# Endpoint to get weather data by city
@app.get("/getWeatherByCity")
def get_weather_by_city(city: str):
    """
    Returns the temperature and humidity of the closest measured point
    to the center of a specified city.
    """
    GEOCODING_API_URL = "http://api.openweathermap.org/geo/1.0/direct"
    API_KEY = "your_openweathermap_api_key"  # Replace with your API key
    response = requests.get(GEOCODING_API_URL, params={"q": city, "limit": 1, "appid": API_KEY})
    if response.status_code != 200 or not response.json():
        raise HTTPException(status_code=404, detail="City not found")

    city_data = response.json()[0]
    city_lat = city_data["lat"]
    city_lon = city_data["lon"]

    if not weather_data:
        raise HTTPException(status_code=404, detail="No weather data available")

    closest_data = None
    min_distance = float("inf")
    for data in weather_data:
        distance = haversine(city_lat, city_lon, data["latitude"], data["longitude"])
        if distance < min_distance:
            min_distance = distance
            closest_data = data

    return {
        "city": city,
        "latitude": city_lat,
        "longitude": city_lon,
        "temperature": closest_data["temperature"],
        "humidity": closest_data["humidity"],
    }

# Endpoint to get weather data by geo-location
@app.get("/getWeatherByGeo")
def get_weather_by_geo(latitude: float, longitude: float):
    """
    Returns the temperature and humidity of the closest measured point
    to a specified geo-location.
    Example response:
    {
      "latitude": 51.5074,
      "longitude": -0.1278,
      "temperature": 15.5,
      "humidity": 80
    }
    """
    if not weather_data:
        raise HTTPException(status_code=404, detail="No weather data available")

    closest_data = None
    min_distance = float("inf")
    for data in weather_data:
        distance = haversine(latitude, longitude, data["latitude"], data["longitude"])
        if distance < min_distance:
            min_distance = distance
            closest_data = data

    return {
        "latitude": latitude,
        "longitude": longitude,
        "temperature": closest_data["temperature"],
        "humidity": closest_data["humidity"],
    }

# Endpoint to get aggregated weather statistics
@app.get("/getAggregatedWeather")
def get_aggregated_weather(latitude: float, longitude: float, radius: float):
    """
    Computes average temperature, average humidity, and their variances
    for all data points within a given radius of a specified geo-location.
    Example response:
    {
      "avg_temperature": 16.2,
      "avg_humidity": 75,
      "temperature_variance": 1.3,
      "humidity_variance": 4.2
    }
    """
    relevant_data = []
    for data in weather_data:
        distance = haversine(latitude, longitude, data["latitude"], data["longitude"])
        if distance <= radius:
            relevant_data.append(data)

    if not relevant_data:
        raise HTTPException(status_code=404, detail="No weather data found within the specified radius")

    avg_temperature = sum(d["temperature"] for d in relevant_data) / len(relevant_data)
    avg_humidity = sum(d["humidity"] for d in relevant_data) / len(relevant_data)

    temperature_variance = sum((d["temperature"] - avg_temperature)**2 for d in relevant_data) / len(relevant_data)
    humidity_variance = sum((d["humidity"] - avg_humidity)**2 for d in relevant_data) / len(relevant_data)

    return {
        "avg_temperature": avg_temperature,
        "avg_humidity": avg_humidity,
        "temperature_variance": temperature_variance,
        "humidity_variance": humidity_variance,
    }
