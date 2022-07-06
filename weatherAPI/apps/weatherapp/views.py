
from django.http import HttpResponse, JsonResponse
from django.views import View

# Create your views here.


class WeatherView(View):

    def get(self, request):
        # <view logic>
        response_dict = { "location_name": "Bogota, CO",
                          "temperature": "17 °C",
                          "wind": "Gentle breeze, 3.6 m/s, west-northwest",
                          "cloudiness": "Scattered clouds",
                          "pressure": "1027 hpa",
                          "humidity": "63%",
                          "sunrise": "06:07",
                          "sunset": "18:00",
                          "geo_coordinates": "[4.61, -74.08]",
                          "requested_time": "2018-01-09 11:57:00"}
        return JsonResponse(response_dict)
