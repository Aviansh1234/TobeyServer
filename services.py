import re
import json
import tbo_handler as tbo

def convert_string_to_json(input):
    match = re.search(r'\{')
    input = input[match.start():]
    return json.loads(input)
def make_json_searchable(input_json):
    example_json = {
    "CheckIn": "2024-01-27",
    "CheckOut": "2024-01-29",
    "HotelCodes": "",
    "CityCode": "115936",
    "GuestNationality": "AE",
    "PreferredCurrencyCode": "AED",
    "PaxRooms": [
        {
            "Adults": 1,
            "Children": 2,
            "ChildrenAges": [
                1,
                16
            ]
        }
    ],
    "IsDetailResponse": True,
    "ResponseTime": 23,
    "Filters": {
        "MealType": "All",
        "Refundable": "true",
        "NoOfRooms": 0
    }
}
    for key,value in input_json.items():
        if key == "CityName":
            continue
        if key == "CountryName":
            currcode = tbo.get_city_code(input_json["CountryName"], input_json["CityName"])
            if currcode == "City Not Found" or currcode == '-1':
                currcode = example_json["CityCode"]
            example_json["CityCode"] = currcode
            continue
        example_json[key] = value
    return example_json
def convert_firebase_msg_to_bard(messages):
    ans = []
    for msg in messages:
        curr = {}
        curr["role"] = msg["author"]
        curr["parts"] = [msg["messageContent"]]
        ans.append(curr)
    return ans