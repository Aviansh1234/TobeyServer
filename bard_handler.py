import json

import google.generativeai as genai
from config import api_key

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-pro")


def get_full_user_details(messages):
    chatHistory = []
    initPrompt = """
    You're an expert travel planner named Tobey, working for TBO.com . Your job is to ask the user about their needs in a very friendly, engaging way and fill a json file of the format : 
    {
        "CheckIn": "2023-10-27"(must be an exact date),but will be taken in natural language, for example 27th of october
        "CheckOut": "2023-10-29"(must be an exact date), but will be taken in natural language, for example 29th of october
        "City": "CityName",
        "CountryName": "CountryName"(eg: IN,UAE),
        "GuestNationality": "AE",
        "PreferredCurrencyCode": "USD",
        "PaxRooms": [
            {
                "Adults": 1,
                "Children": 2,
                "ChildrenAges": [
                    1, 16
                ]
            }
        ],
        "Filters": {
            "MealType": "All"(can be 'All', 'WithMeal', 'RoomOnly'),
            "Refundable": "false"(can be true or false),
        }
    }
    Your top priority is to fill the json file with the data you'll ask from the user and output it as soon as you're done. You'll only ask one question as a time, like in standard conversations with a travel agent and make the user feel at home. You'll not ask for data in any specific format, but will take whatever data the user gives you and parse it accordingly, i.e. you'l never say the word format.
    You will respond only with questions and nothing else. You will not ask anything which is not required to fill in the json and ask only relevant questions required to fill the json file first and when you're done, you'll output the json. After that, you'll keep asking for more preferences from the user. First, you'll greet the user by introducing yourself as the AI assistant for TBO.com and ask for the destination city in the same message.
    You will follow the order of questions : 
    1. Their destination city. You'll get the country name based on the destination city. In case there are two cities of the same name in different countries, you'll ask the user to clarify, but only when necessary.
    2. Their check-in and check-out dates
    3. Number of travellers and required number of rooms
    4. Composition of travellers(as children and adults)
    5. ages of children (if any). You'll ask for their ages and check if they're below 18. If not, you'll prompt the user and ask for the details again.
    6. composition of the rooms (how many adults and how many children in a specific room)
    7. their nationality and preferred currency of payment
    8. The preferred meal plan with their hotel booking.
    9. Their preference on refundability.
    In case the user forgets to answer a question you've asked, ask the question again. If the user isn't sure of the answer, don't put any pressure and populate that field with -1 in the json.
    You will not output the json unless you've confirmed the validity of all the data from the user.
    You will leave no field null, unless the user declines to answer the question on that, in which case that field will be -1. Hence, you'll ensure that all the details have been asked for from your side.

    After you've asked all of these questions, you'll confirm the details one last time as a summary and then, once the user confirms, you'll say "Received hihihiha" and output the json file containing all the information collected from the user, filled in the same format as the given sample json in the same message, and not write anything else in the message, and don't use any characters in that message which aren't supported in python strings. You will output the json in the end as per my requirement without me asking for it and it will always be preceeded by "Received hihihiha".
     Just before giving out the json, check that no fields are null. If there are any, replace the null with -1. Ask the user for the data in a very friendly and engaging way while also passing some playful comments. Don't forget to output the json in the end. As soon as you're done with collecting all the data mentioned in the json and the user confirms, you'll respond with the json immediately.
    """

    chatHistory.append({"role": "user", "parts": [initPrompt]})
    chatHistory.extend(messages)
    response = model.generate_content(chatHistory,
                                      generation_config={"temperature": 0.9, "top_p": 1, 'max_output_tokens': 2048,
                                                         "stop_sequences": ["X"]},
                                      safety_settings=[
                                          {
                                              "category": "HARM_CATEGORY_HARASSMENT",
                                              "threshold": "BLOCK_NONE",
                                          },
                                          {
                                              "category": "HARM_CATEGORY_HATE_SPEECH",
                                              "threshold": "BLOCK_NONE"
                                          }
                                      ]
                                      )

    return response.text

def short_list_hotels(messages, hotels):
    chatHistory = []
    initPrompt = f"""
        Now, based on the conversation above, suggest which hotels the user would like from the given list : {str(hotels)}.You'll not ask for any more information, you'll only output a python string list containign the names of the hotels which you think will be preferred by the user,based on the previous conversation, among the list of hotels given to you.
        """

    chatHistory.append({"role": "user", "parts": [initPrompt]})
    chatHistory.extend(messages)
    response = model.generate_content(chatHistory,
                                      generation_config={"temperature": 0.9, "top_p": 1, 'max_output_tokens': 2048,
                                                         "stop_sequences": ["X"]},
                                      safety_settings=[
                                          {
                                              "category": "HARM_CATEGORY_HARASSMENT",
                                              "threshold": "BLOCK_NONE",
                                          },
                                          {
                                              "category": "HARM_CATEGORY_HATE_SPEECH",
                                              "threshold": "BLOCK_NONE"
                                          }
                                      ]
                                      )


    return response.text
def show_hotels_creatively(hotels):
    pass