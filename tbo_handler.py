import json
import requests
from requests.auth import HTTPBasicAuth
import config

creds = HTTPBasicAuth(config.user_name, config.password)

def search_hotels(query):
    response = requests.post(config.tbo_base_url + "/HotelSearch", auth=creds, json=query)
    if response.status_code == 200:
        return response.json()['HotelSearchResults']
    else:
        return None
    pass

def get_hotel_info(hotel_id):
    response = requests.post(config.tbo_base_url + "/Hoteldetails", auth=creds,
                             json={'Hotelcodes': str(hotel_id), 'Language': 'en'})
    if response.status_code == 200:
        return response.json()['HotelDetails']
    else:
        return None
    pass
def get_city_code(country_code, city_name):
    response = requests.post(config.tbo_base_url + "/CityList", auth=creds, json={'CountryCode': country_code})
    if response.status_code == 200:
        for i in response.json()['CityList']:
            if city_name in i['Name']:
                return i["Code"]
        return 'City Not Found'
    return '-1'