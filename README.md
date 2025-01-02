Weather Data API Project Report
Introduction
The Weather Data API project provides a scalable and efficient solution for managing
and analyzing weather-related data. It offers functionality to submit, retrieve, and
aggregate weather data. By leveraging modern technologies such as FastAPI,
asynchronous programming, and caching, the API is optimized for high performance and
scalability.
This report outlines the implementation of the API, the profiling and performance testing
conducted to evaluate its efficiency, and the optimizations performed to enhance its
functionality and reliability.

Weather Data API Features
1. Submit Weather Data
 Endpoint: /data
 Method: POST
 Description:
o This endpoint allows users to submit weather data for specific geo-locations.
o Users can provide latitude, longitude, temperature, and humidity
values, which are then stored in the API's in-memory data store.
 Example Use Case:
o Collecting weather data from IoT devices or weather stations and storing it for
future analysis.

2. Get Weather by City
 Endpoint: /getWeatherByCity
 Method: GET
 Description:
o Fetches the weather data closest to the center of a specified city.
o Integrates with the OpenWeatherMap Geocoding API to determine the latitude
and longitude of the city.
 Example Use Case:
o Applications that display weather information for specific cities, such as travel
or tourism websites.

3. Get Weather by Geo-Location
 Endpoint: /getWeatherByGeo
 Method: GET
 Description:
o Retrieves the weather data closest to a given geo-location (latitude and
longitude).
o Uses the Haversine formula to calculate the distance between the geocoordinates and stored weather data points.
 Example Use Case:
o Systems where geo-coordinates (e.g., GPS data) are available, such as maps or
logistics applications.


4. Get Aggregated Weather Statistics
 Endpoint: /getAggregatedWeather
 Method: GET
 Description:
o Computes statistical insights for weather data within a specified radius of a
given geo-location.
o Outputs include:
 Average temperature and humidity.
 Variance of temperature and humidity.
 Example Use Case:
o Applications requiring weather analytics over a region, such as agricultural
platforms or environmental monitoring systems.

Profiling
In this project, profiling was implemented using Python's built-in cProfile library. A
middleware was added to the FastAPI application to automatically profile every
incoming request and log the performance metrics to the console. Here's how it works:
1. Middleware Integration:
o A custom middleware was added to wrap each HTTP request and response
cycle. This middleware uses cProfile to measure the time taken by all
function calls during the processing of the request.
2. Logging Metrics:
o The profiling middleware logs the following details for each request:
 Total time taken for the request.
Function call count.
 Time spent in each function (cumulative and individual).
o These logs are printed to the console for real-time analysis.
3. Identifying Bottlenecks:
o The profiling results revealed slow operations, such as blocking calls to
the OpenWeatherMap API and computationally intensive functions like
the Haversine formula and data aggregation calculations

Performance Testing in the Weather Data API
Performance testing is a crucial aspect of ensuring the scalability and reliability of the
Weather Data API under varying loads. In this project, performance testing was
conducted using Locust, a Python-based tool that simulates concurrent user traffic to
evaluate the API's responsiveness, throughput, and error rates. A dedicated
locustfile.py was created to define test tasks for each endpoint (/data,
/getWeatherByCity, /getWeatherByGeo, and /getAggregatedWeather). These tasks
simulate real-world scenarios, such as users submitting weather data, retrieving it by city
or coordinates, and calculating aggregated statistics. The Locust web interface allowed
the configuration of parameters like the number of simulated users and the spawn rate.
Metrics such as requests per second (RPS), response times, and failure rates were
monitored during the tests. This approach revealed performance bottlenecks, particularly
under high concurrency, and helped validate the impact of optimizations like caching,
asynchronous API calls, and multi-worker setups. By incorporating performance testing,
the API was fine-tuned to handle real-world traffic efficiently.

