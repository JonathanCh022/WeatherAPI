import requests
import requests_cache
from django.http import JsonResponse
from django.views import View
from datetime import datetime


# Create your views here.

class WeatherView(View):

    requests_cache.install_cache('weather_cache', backend='sqlite', expire_after=120)

    def get(self, request):
        """ pull data for the external API
            Parameters:
                    request.GET.city : String with the city to query
                    request.GET.country : Is a country code of two characters in lowercase

            Returns:
                    JsonResponse : the forecast data from the city searched. return error message if city is not founded
        """

        city = "{city},{country}".format(city=request.GET.get("city"), country=request.GET.get("country").lower())
        resp = requests.get('http://api.openweathermap.org/data/2.5/weather',
                            params={'q': city,
                                    'appid': '1508a9a4840a5574c822d70ca2132032'})
        if resp:

            resp_json = resp.json()

            """
                the wind_info func for transform the api info in human-redeable info
            """
            if resp_json['wind']:
                wind, angle = self.wind_info(resp_json['wind']['speed'], resp_json['wind']['deg'])
                speed = resp_json['wind']['speed']
            else:
                wind, angle, speed = "", "", ""

            """
                using datetime libraries to transform unix time data to datetime format
            """
            dt = datetime.fromtimestamp(resp_json['dt']).strftime("%Y-%d-%m %H:%M:%S")
            sunrise = datetime.fromtimestamp(resp_json['sys']['sunrise']).strftime(" %H:%M:%S")
            sunset = datetime.fromtimestamp(resp_json['sys']['sunset']).strftime(" %H:%M:%S")

            """ 
                create de dict from the JSONResponse 
            """
            response_dict = { "location_name": "{name},{c}".format(name=resp_json['name'], c=resp_json['sys']['country']),
                              "temperature": "{celsius} °C, {farenh} °F".format(
                                  celsius=int(resp_json['main']['temp']) - 273,
                                  farenh=(1.8 * int(resp_json['main']['temp']) - 273) + 32),
                              "wind": "{wind}, {speed} m/s, {angle}".format(wind=wind, angle=angle, speed=speed),
                              "cloudiness": "{cloud}".format(cloud=resp_json['weather'][0]['description']),
                              "pressure": "{} hpa".format(resp_json['main']['pressure']),
                              "humidity": "{}%".format(resp_json['main']['humidity']),
                              "sunrise": sunrise,
                              "sunset": sunset,
                              "geo_coordinates": "[{lat}, {lon}]".format(lat=resp_json['coord']['lat'],
                                                                         lon=resp_json['coord']['lon']),
                              "requested_time": dt,
                              "forecast": "{}". format(resp_json['weather'][0]['main'])}
            return JsonResponse(response_dict)
        else:
            return JsonResponse({"message": "city not found"})

    def wind_info(self, speed, deg):
        """ This funcion use a default dict to set the correct angle and wind forecast

            Parameters:
                    speed  : wind speed in m/s
                    deg :  Wind direction, degrees (meteorological)

            Returns:
                    wind (str): Wind scale
                    angle (str): wind direction as a compass
        """
        speed, deg = int(speed), int(deg)
        wind, angle = "", ""
        compass = {
            range(349, 11): 'north',
            range(11, 34): 'north-northeast',
            range(34, 56): 'north-east',
            range(56, 79): 'east-northeast',
            range(79, 101): 'east',
            range(101, 124): 'east-southeast',
            range(124, 146): 'south-east',
            range(146, 169): 'south-southeast',
            range(169, 191): 'south',
            range(191, 214): 'south-southwest',
            range(214, 236): 'southwest',
            range(236, 259): 'west-southwest',
            range(259, 281): 'west',
            range(281, 304): 'west-northwest',
            range(304, 326): 'north-west',
            range(326, 349): 'north-northwest'
        }

        for key, value in compass.items():
            if deg in key:
                angle = value

        wind_scale = {
            range(0, 1): 'Calm',
            range(1, 4): 'Light Air',
            range(4, 8): 'Light Breeze',
            range(8, 13): 'Gentle Breeze',
            range(13, 19): 'Moderate Breeze',
            range(19, 25): 'Fresh Breeze',
            range(25, 32): 'Strong Breeze',
            range(32, 39): 'Near Gale',
            range(39, 47): 'Gale',
            range(47, 55): 'Severe Gale',
            range(55, 64): 'Storm',
            range(64, 72): 'Violent Storm',
            range(72, 83): 'Hurricane'
            }

        for key, value in wind_scale.items():
            if speed in key:
                wind = value

        return wind, angle
