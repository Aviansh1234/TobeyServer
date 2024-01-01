import re
import json
import tbo_handler as tbo


def convert_to_messages(strings):
    messages = []
    for string in strings:
        messages.append({"author": "model", "msgContent": string, "itenaryId": ""})

def convert_string_to_json(input):
    match = re.search(r'\{', input)
    input = input[match.start():]
    return eval(input)
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
    if len(input_json["CountryName"]) >2:
        input_json["CountryName"] = input_json["CountryName"][0:2]
    if len(input_json["GuestNationality"]) >2:
        input_json["GuestNationality"] = "IN"
    if input_json["CheckIn"][0:4] < "2024":
        input_json["CheckIn"] = str(int(input_json["CheckIn"][0:4])+1)+"-"+str(input_json["CheckIn"][5:])
    if input_json["CheckOut"][0:4] < "2024":
        input_json["CheckOut"] = str(int(input_json["CheckOut"][0:4])+1)+"-"+str(input_json["CheckOut"][5:])
    for key, value in input_json.items():
        if value == '-1':
            continue
        if key == "City":
            continue
        if key == "CountryName":
            currcode = tbo.get_city_code(input_json["CountryName"], input_json["City"])
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