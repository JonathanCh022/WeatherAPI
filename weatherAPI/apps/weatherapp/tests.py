from django.test import TestCase
from .views import WeatherView
from django.test import Client


# Create your tests here.
class WeatherViewTests(TestCase):

    def test_weather_response(self):
        """
            If city exist,should return  message is displayed.
        """
        client = Client()
        response = client.get('/weather?city=bogota&country=co')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['location_name'], 'Bogota,CO')

    def test_weather_no_city(self):
        """
            return a message when the city searched is not found.
        """
        client = Client()
        response = client.get('/weather?city=bogota&country=jp')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'city not found')

    def test_weather_json(self):
        """
            check the content-type header and json type of the response
        """
        client = Client()
        response = client.get('/weather?city=bogota&country=co')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()), type({}))
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_wind_info_int(self):
        """
            check wind direction and the compass angle for wind info with integer types
        """
        weather = WeatherView()
        w, a = weather.wind_info(6, 36)
        self.assertEqual(w, 'Light Breeze')
        self.assertEqual(a, 'north-east')

    def test_wind_info_int(self):
        """
            check wind direction and the compass angle for wind info with str types
        """
        weather = WeatherView()
        w, a = weather.wind_info('75', '240')
        self.assertEqual(w, 'Hurricane')
        self.assertEqual(a, 'west-southwest')