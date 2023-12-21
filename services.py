import re
import json

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
        },
        {
            "Adults": 1,
            "Children": 0,
            "ChildrenAges": [
                1
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
        example_json[key] = value
    return example_json