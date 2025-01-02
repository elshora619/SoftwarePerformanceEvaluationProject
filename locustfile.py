from locust import HttpUser, task

class WeatherAPITester(HttpUser):
    @task
    def test_post_data(self):
        """
        Test the `/data` endpoint by submitting weather data.
        """
        self.client.post(
            "/data",
            json={
                "latitude": 51.5074,
                "longitude": -0.1278,
                "temperature": 15.5,
                "humidity": 80,
            },
        )

    @task
    def test_get_weather_by_city(self):
        """
        Test the `/getWeatherByCity` endpoint for a valid city.
        """
        self.client.get("/getWeatherByCity?city=London")

    @task
    def test_get_weather_by_geo(self):
        """
        Test the `/getWeatherByGeo` endpoint for a valid geo-location.
        """
        self.client.get("/getWeatherByGeo?latitude=51.5074&longitude=-0.1278")

    @task
    def test_aggregated_weather(self):
        """
        Test the `/getAggregatedWeather` endpoint for a location and radius.
        """
        self.client.get(
            "/getAggregatedWeather?latitude=51.5074&longitude=-0.1278&radius=10"
        )
