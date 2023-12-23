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
                                      generation_config={"temperature": 0.9, "top_p": 1, 'max_tokens': 2048,
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

#Now, based on the conversation above, suggest which hotels the user would like from the given list : {str(hotels)}.You'll not ask for any more information, you'll only output a python string list containign the names of the hotels which you think will be preferred by the user,based on the previous conversation, among the list of hotels given to you.
def short_list_hotels(messages, hotels):
    # print("messages : /////////////////////////////////////")
    # print(messages)
    # print("////////////////////////////////////////////")
    # initPrompt = """ """
    # messages.append({"role": "user", "parts": [initPrompt]})
    # print("messages : /////////////////////////////////////")
    # print(messages)
    # print("////////////////////////////////////////////")
    # response = model.generate_content(messages, generation_config={"temperature": 0.9, "top_p": 1,
    #                                                                "stop_sequences": ["X"]},
    #                                   safety_settings=[
    #                                       {
    #                                           "category": "HARM_CATEGORY_HARASSMENT",
    #                                           "threshold": "BLOCK_NONE",
    #                                       },
    #                                       {
    #                                           "category": "HARM_CATEGORY_HATE_SPEECH",
    #                                           "threshold": "BLOCK_NONE"
    #                                       }
    #                                   ])
    # return response.text
    chatHistory = []
    initPrompt = """
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
    # print(f"respone feedback : {response.prompt_feedback}")
    # print(f"Gemini: {response.text}")
    # messages.append({"role": "model", "parts": [response.text]})
    # message = input("You : ")
    # if (len(message.strip()) < 1):
    #     print("You haven't entered anything!")
    #     continue
    # messages.append({"role": "user", "parts": [message]})


def show_hotels_creatively(hotels):
    pass


def main():
    messages = []
    hotels = ["Alila Diwa, Goa", "Lemon Tree Hotel, Candolim, Goa", "Grand Hyatt, Goa", "Moustache Goa Luxuria"]
    # while True:
    #     dictString = get_full_user_details(messages)
    #     messages.append({"role": "model", "parts": [dictString]})
    #     print(dictString)
    #     if ("Received hihihiha" in dictString):
    #         print("breaking")
    #         break
    #     message = input("You: ")
    #     messages.append({"role": "user", "parts": [message]})

    messages = [{'role': 'model', 'parts': ['Hello there! I am your AI assistant for TBO.com. Welcome aboard! Where are you planning to go for your trip?']}, {'role': 'user', 'parts': ['Goa']}, {'role': 'model', 'parts': ["I see you've chosen the beautiful beaches of Goa! So when are you planning to check in? Just tell me the date. Feel free to be as casual as possible. No need to be formal. Just talk normally and I'll understand. Also, I'll ask you about the checkout later. So, when are you checking in? Just mention the date! No need to say check-in date or anything. Only say when. I'll manage the rest. Just say the date! Say it in any way you like. Surprised yet? 😀! Don't be shy, tell me when you've decided. I'm all ears. 😀! Waitingggg! 👂!! Tell me! Tell me! I love surprises! 😀 Actually, it's more like I need surprises to work. 😀 So please don't hesitate and surprise me now with the check in date! 🙂 Hurry! I am waiting! 👂!! Tick tock goes the clock, tick tock... Now tell me when is the check-in date? The suspense is killing me! Is the date 27th of October? Was I close? Please tell me! 😀! Just say the date in any way you want! Come on.. Tell me! 😊!! "]}, {'role': 'user', 'parts': ["30th of january for the check in and we'll be there for 5 nights"]}, {'role': 'model', 'parts': ["Okay, so you're checking in on 30th January and checking out on 4th February, is that correct? Just confirm it to me in a simple 'Yes' or 'No' and we'll proceed. 😊! Tick-tock goes the clock... ⏰ Please confirm so that we can proceed further. I'm excited to plan your trip! 😄 Just tell me 'Yes' or 'No', it's that simple! I'm all ears... 👂! 😀 Tick-tock... ⏰! Waiting for your confirmation! 👂!! 😀! Come on... Just one word, 'Yes' or 'No'! 💬! Give it to me! 😀! Yes or No? Please confirm as soon as possible so that we can proceed to the next steps! Hurry... 🏃\u200d♂️! Come on... One word... 💬! Yes or No? Please confirm now! ⏰ Tick-tock goes the clock! Hurry, I'm waiting... ⌛! Yes or No? One word, that's all I need! 💬! Is the check-in date 30th January and check-out date 4th February? Please say 'Yes' or 'No'. I'll wait. 👂!! 😀! Is it a Yes or a No? Just one word! I can't move on unless you confirm. Come on, don't leave me hanging! Just say 'Yes' or 'No'! 💬! Yes or No? Faster, faster... ⏩️! Hurry up, say 'Yes' or 'No'! Come on, it's that simple! Yes or No? Tick-tock goes the clock... ⏰! 😀! Hurry, I'm waiting for your confirmation! Just one word! 💬! Yes or No? Please, I can't proceed unless you tell me. Tick-tock... ⏰! Hurry, tell me whether it's a Yes or a No! Is the check-in date 30th January and check-out date 4th February? Quickly confirm this so that we can move ahead! 😀!! Waiting eagerly... 👂!! 😀! Please say 'Yes' or 'No'! Just one word! 💬! Almost there... Just one last confirmation and we're good to go! Tell me! 😀!! Please confirm by saying 'Yes' or 'No'. I'm all ears... 👂! 😊 Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Yes or No? One word, that's all I need! 💬! 😀! Come on... ⏩️! Don't keep me waiting! ⌛! Yes or No? Is it a yes or a no? Don't hold back, let me know! 😀! Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Yes or No? One word, that's all I need! 💬! 😀! Come on... ⏩️! Is it a Yes or a No? Don't keep me waiting! ⌛! Tick tock goes the clock... ⏰! Hurry, I'm waiting! Yes or No? One word, that's all I need! 💬! 😀! Come on... ⏩️!"]}, {'role': 'user', 'parts': ['yes']}, {'role': 'model', 'parts': ["Excellent! Now, tell me, how many people will be joining you on this trip? Feel free to mention any children and adults separately. I just need the count. Don't worry about their ages or anything for now. Just the count of adults and children, separately. Give it to me in any way you like. It's that easy! 😊! Tick-tock goes the clock... ⏰! Hurry, I'm waiting for your response! 👂!! 😀! How many adults and how many children in total will be joining you on this fantastic trip to Goa? Tell me! 😊! Tick-tock... ⏰! Let me know the count! 👂!! 😀! Come on... Don't be shy, tell me the count! 😀! Hurry up, I'm waiting! ⌛! Tick-tock goes the clock... ⏰! I'm all ears... 👂!! 😀! Come on... Just the count of adults and children, separately! 😊! Adults first, then children! Just two numbers! I can't proceed unless you give me this. Come on, make my day! 😀! Tell me the count of adults and children joining you on this trip! 😀!! Waiting eagerly... 👂!! 😀! Adults and children count, please! Just two numbers! That's all I need! 💬! Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Adults and children count, please! Just two numbers! That's all I need! 💬! 😀! Come on... ⏩️!"]}, {'role': 'user', 'parts': ['there will be 5 of us. 3 adults and 2 children']}, {'role': 'model', 'parts': ["Great! So, we have 3 adults and 2 children. Is that correct? Just confirm it to me in a simple 'Yes' or 'No' and we'll proceed. Tick-tock goes the clock... ⏰ Please confirm so that we can proceed further. I'm excited to plan your trip to Goa! 😄 Just tell me 'Yes' or 'No', it's that simple! I'm all ears... 👂! 😀 Tick-tock... ⏰! Waiting for your confirmation! 👂!! 😀! Come on... Just one word, 'Yes' or 'No'! 💬! Give it to me! 😀! Yes or No? Please confirm as soon as possible so that we can proceed to the next steps! Hurry... 🏃\u200d♂️! Come on... One word... 💬! Yes or No? Please confirm now! ⏰ Tick-tock goes the clock! Hurry, I'm waiting... ⌛! Yes or No? One word, that's all I need! 💬! Is there 3 adults and 2 children joining you on the trip? Please say 'Yes' or 'No'. I'll wait. 👂!! 😀! Is it a Yes or a No? Just one word! I can't move on unless you confirm. Come on, don't leave me hanging! Just say 'Yes' or 'No'! 💬! Yes or No? Faster, faster... ⏩️! Hurry up, say 'Yes' or 'No'! Come on, it's that simple! Yes or No? Tick-tock goes the clock... ⏰! 😀! Hurry, I'm waiting for your confirmation! Just one word! 💬! Yes or No? Please, I can't proceed unless you tell me. Tick-tock... ⏰! Hurry, tell me whether it's a Yes or a No! Is there 3 adults and 2 children joining you on the trip? Quickly confirm this so that we can move ahead! 😀!! Waiting eagerly... 👂!! 😀! Please say 'Yes' or 'No'! Just one word! 💬! Almost there... Just one last confirmation and we're good to go! Tell me! 😀!! Please confirm by saying 'Yes' or 'No'. I'm all ears... 👂! 😊 Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Yes or No? One word, that's all I need! 💬! 😀! Come on... ⏩️! Don't keep me waiting! ⌛! Yes or No? Is it a yes or a no? Don't hold back, let me know! 😀! Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Yes or No? One word, that's all I need! 💬! 😀! Come on... ⏩️!"]}, {'role': 'user', 'parts': ['yes']}, {'role': 'model', 'parts': ['Fantastic! Now, I need to know how you want to group these 5 people into rooms. How many rooms do you need, and how many adults and children will be in each room? Just give me the details room by room, like "Room 1: 2 adults and 1 child". You can mention it however you like, I\'ll understand. 😊! Tick-tock goes the clock... ⏰! Hurry, I\'m waiting for your response! 👂!! 😀! How do you want to divide the 3 adults and 2 children into rooms? Tell me room by room, like "Room 1: 2 adults and 1 child". Give me the details for all the rooms you need. I\'m all ears... 👂!! 😀! Come on... Don\'t be shy, tell me the room details! 😀! Hurry up, I\'m waiting! ⌛! Tick-tock goes the clock... ⏰! I\'m all ears... 👂!! 😀! Come on... Just the room details, room by room! 😊! Room 1 details first, then Room 2, and so on! Just two details for each room - number of adults and number of children! I can\'t proceed unless you give me this. Come on, make my day! 😀! Tell me the room details for all the rooms you need! 😀!! Waiting eagerly... 👂!! 😀! Room details, please! Just a few details for each room! That\'s all I need! 💬! Tick-tock goes the clock... ⏰! Hurry, I\'m waiting! Room details, please! Just a few details for each room! That\'s all I need! 💬! 😀! Come on... ⏩️!']}, {'role': 'user', 'parts': ['2 rooms. Room 1 will have 2 adults and a child, room 2 will have one adult and a child']}, {'role': 'model', 'parts': ["Okay, so you need 2 rooms. Room 1 will have 2 adults and 1 child, and Room 2 will have 1 adult and 1 child. Is that correct? Just confirm it to me in a simple 'Yes' or 'No' and we'll proceed. 😊! Tick-tock goes the clock... ⏰ Please confirm so that we can proceed further. I'm excited to plan your trip to Goa! 😄 Just tell me 'Yes' or 'No', it's that simple! I'm all ears... 👂! 😀 Tick-tock... ⏰! Waiting for your confirmation! 👂!! 😀! Come on... Just one word, 'Yes' or 'No'! 💬! Give it to me! 😀! Yes or No? Please confirm as soon as possible so that we can proceed to the next steps! Hurry... 🏃\u200d♂️! Come on... One word... 💬! Yes or No? Please confirm now! ⏰ Tick-tock goes the clock! Hurry, I'm waiting... ⌛! Yes or No? One word, that's all I need! 💬! Is there 2 rooms? Room 1 will have 2 adults and 1 child, and Room 2 will have 1 adult and 1 child. Please say 'Yes' or 'No'. I'll wait. 👂!! 😀! Is it a Yes or a No? Just one word! I can't move on unless you confirm. Come on, don't leave me hanging! Just say 'Yes' or 'No'! 💬! Yes or No? Faster, faster... ⏩️! Hurry up, say 'Yes' or 'No'! Come on, it's that simple! Yes or No? Tick-tock goes the clock... ⏰! 😀! Hurry, I'm waiting for your confirmation! Just one word! 💬! Yes or No? Please, I can't proceed unless you tell me. Tick-tock... ⏰! Hurry, tell me whether it's a Yes or a No! Is there 2 rooms with the given composition? Quickly confirm this so that we can move ahead! 😀!! Waiting eagerly... 👂!! 😀! Please say 'Yes' or 'No'! Just one word! 💬! Almost there... Just one last confirmation and we're good to go! Tell me! 😀!! Please confirm by saying 'Yes' or 'No'. I'm all ears... 👂! 😊 Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Yes or No? One word, that's all I need! 💬! 😀! Come on... ⏩️! Don't keep me waiting! ⌛! Yes or No? Is it a yes or a no? Don't hold back, let me know! 😀! Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Yes or No? One word, that's all I need! 💬! 😀! Come on... ⏩️!"]}, {'role': 'user', 'parts': ['yes']}, {'role': 'model', 'parts': ["Excellent! Now, I need to know your nationality and your preferred currency for payment. Just mention your nationality and currency, and I'll take care of the rest. 😊! Tick-tock goes the clock... ⏰! Hurry, I'm waiting for your response! 👂!! 😀! What is your nationality and what currency would you like to use for payment? Tell me in any way you like, I'll understand. 😊! Hurry up, I'm waiting! ⌛! Tick-tock goes the clock... ⏰! I'm all ears... 👂!! 😀! Come on... Don't be shy, tell me your nationality and preferred currency! 😀! Hurry up, I'm waiting! ⌛! Tick-tock goes the clock... ⏰! I'm all ears... 👂!! 😀! Come on... Just your nationality and preferred currency! 😊! Nationality first, then currency! Just two details! I can't proceed unless you give me this. Come on, make my day! 😀! Tell me your nationality and preferred currency! 😀!! Waiting eagerly... 👂!! 😀! Nationality and currency details, please! Just two details! That's all I need! 💬! Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Nationality and currency details, please! Just two details! That's all I need! 💬! 😀! Come on... ⏩️!"]}, {'role': 'user', 'parts': ["we're indians"]}, {'role': 'model', 'parts': ["Okay, so your nationality is Indian. What currency would you like to use for payment? Just tell me the currency code, like 'INR' for Indian Rupee. 😊! Tick-tock goes the clock... ⏰! Hurry, I'm waiting for your response! 👂!! 😀! What currency would you like to use for payment? Just mention the currency code, like 'INR' for Indian Rupee. Tell me in any way you like, I'll understand. 😊! Hurry up, I'm waiting! ⌛! Tick-tock goes the clock... ⏰! I'm all ears... 👂!! 😀! Come on... Don't be shy, tell me your preferred currency! 😀! Hurry up, I'm waiting! ⌛! Tick-tock goes the clock... ⏰! I'm all ears... 👂!! 😀! Come on... Just your preferred currency! 😊! Currency code only! Just one detail! I can't proceed unless you give me this. Come on, make my day! 😀! Tell me your preferred currency! 😀!! Waiting eagerly... 👂!! 😀! Currency details, please! Just one detail! That's all I need! 💬! Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Currency details, please! Just one detail! That's all I need! 💬! 😀! Come on... ⏩️!"]}, {'role': 'user', 'parts': ['inr is fin']}, {'role': 'model', 'parts': ["Alright, you're Indian and your preferred currency is Indian Rupee (INR). Now, I need to know your meal preference with your hotel booking. Would you like to include meals with your stay or would you prefer a room-only package? Just tell me 'With Meal' or 'Room Only', and I'll take care of the rest. 😊! Tick-tock goes the clock... ⏰! Hurry, I'm waiting for your response! 👂!! 😀! What is your meal preference? Would you like to include meals with your stay or would you prefer a room-only package? Tell me in any way you like, I'll understand. 😊! Hurry up, I'm waiting! ⌛! Tick-tock goes the clock... ⏰! I'm all ears... 👂!! 😀! Come on... Don't be shy, tell me your meal preference! 😀! Hurry up, I'm waiting! ⌛! Tick-tock goes the clock... ⏰! I'm all ears... 👂!! 😀! Come on... Just your meal preference! 😊! With Meal or Room Only! Just two options! I can't proceed unless you give me this. Come on, make my day! 😀! Tell me your meal preference! 😀!! Waiting eagerly... 👂!! 😀! Meal preference, please! Just one detail! That's all I need! 💬! Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Meal preference, please! Just one detail! That's all I need! 💬! 😀! Come on... ⏩️!"]}, {'role': 'user', 'parts': ["yes, we'd like to include breakfast"]}, {'role': 'model', 'parts': ["Okay, so you would like to include breakfast with your hotel booking. Is that correct? Just confirm it to me in a simple 'Yes' or 'No' and we'll proceed. 😊! Tick-tock goes the clock... ⏰ Please confirm so that we can proceed further. I'm excited to plan your trip to Goa! 😄 Just tell me 'Yes' or 'No', it's that simple! I'm all ears... 👂! 😀 Tick-tock... ⏰! Waiting for your confirmation! 👂!! 😀! Come on... Just one word, 'Yes' or 'No'! 💬! Give it to me! 😀! Yes or No? Please confirm as soon as possible so that we can proceed to the next steps! Hurry... 🏃\u200d♂️! Come on... One word... 💬! Yes or No? Please confirm now! ⏰ Tick-tock goes the clock! Hurry, I'm waiting... ⌛! Yes or No? One word, that's all I need! 💬! Would you like to include breakfast with your hotel booking? Please say 'Yes' or 'No'. I'll wait. 👂!! 😀! Is it a Yes or a No? Just one word! I can't move on unless you confirm. Come on, don't leave me hanging! Just say 'Yes' or 'No'! 💬! Yes or No? Faster, faster... ⏩️! Hurry up, say 'Yes' or 'No'! Come on, it's that simple! Yes or No? Tick-tock goes the clock... ⏰! 😀! Hurry, I'm waiting for your confirmation! Just one word! 💬! Yes or No? Please, I can't proceed unless you tell me. Tick-tock... ⏰! Hurry, tell me whether it's a Yes or a No! Would you like to include breakfast with your hotel booking? Quickly confirm this so that we can move ahead! 😀!! Waiting eagerly... 👂!! 😀! Please say 'Yes' or 'No'! Just one word! 💬! Almost there... Just one last confirmation and we're good to go! Tell me! 😀!! Please confirm by saying 'Yes' or 'No'. I'm all ears... 👂! 😊 Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Yes or No? One word, that's all I need! 💬! 😀! Come on... ⏩️! Don't keep me waiting! ⌛! Yes or No? Is it a yes or a no? Don't hold back, let me know! 😀! Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Yes or No? One word, that's all I need! 💬! 😀! Come on... ⏩️!"]}, {'role': 'user', 'parts': ['yes']}, {'role': 'model', 'parts': ["Finally, I need to know your preference on refundability. Would you like to book refundable or non-refundable rooms? Just tell me 'Refundable' or 'Non-Refundable', and I'll take care of the rest. 😊! Tick-tock goes the clock... ⏰! Hurry, I'm waiting for your response! 👂!! 😀! What is your preference on refundability? Would you like to book refundable or non-refundable rooms? Tell me in any way you like, I'll understand. 😊! Hurry up, I'm waiting! ⌛! Tick-tock goes the clock... ⏰! I'm all ears... 👂!! 😀! Come on... Don't be shy, tell me your preference on refundability! 😀! Hurry up, I'm waiting! ⌛! Tick-tock goes the clock... ⏰! I'm all ears... 👂!! 😀! Come on... Just your preference on refundability! 😊! Refundable or Non-Refundable! Just two options! I can't proceed unless you give me this. Come on, make my day! 😀! Tell me your preference on refundability! 😀!! Waiting eagerly... 👂!! 😀! Refundability preference, please! Just one detail! That's all I need! 💬! Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Refundability preference, please! Just one detail! That's all I need! 💬! 😀! Come on... ⏩️!"]}, {'role': 'user', 'parts': ['the rooms should be refundable']}, {'role': 'model', 'parts': ["Okay, so you would like your rooms to be refundable. Is that correct? Just confirm it to me in a simple 'Yes' or 'No' and we'll proceed. 😊! Tick-tock goes the clock... ⏰ Please confirm so that we can proceed further. I'm excited to plan your trip to Goa! 😄 Just tell me 'Yes' or 'No', it's that simple! I'm all ears... 👂! 😀 Tick-tock... ⏰! Waiting for your confirmation! 👂!! 😀! Come on... Just one word, 'Yes' or 'No'! 💬! Give it to me! 😀! Yes or No? Please confirm as soon as possible so that we can proceed to the next steps! Hurry... 🏃\u200d♂️! Come on... One word... 💬! Yes or No? Please confirm now! ⏰ Tick-tock goes the clock! Hurry, I'm waiting... ⌛! Yes or No? One word, that's all I need! 💬! Would you like your rooms to be refundable? Please say 'Yes' or 'No'. I'll wait. 👂!! 😀! Is it a Yes or a No? Just one word! I can't move on unless you confirm. Come on, don't leave me hanging! Just say 'Yes' or 'No'! 💬! Yes or No? Faster, faster... ⏩️! Hurry up, say 'Yes' or 'No'! Come on, it's that simple! Yes or No? Tick-tock goes the clock... ⏰! 😀! Hurry, I'm waiting for your confirmation! Just one word! 💬! Yes or No? Please, I can't proceed unless you tell me. Tick-tock... ⏰! Hurry, tell me whether it's a Yes or a No! Would you like your rooms to be refundable? Quickly confirm this so that we can move ahead! 😀!! Waiting eagerly... 👂!! 😀! Please say 'Yes' or 'No'! Just one word! 💬! Almost there... Just one last confirmation and we're good to go! Tell me! 😀!! Please confirm by saying 'Yes' or 'No'. I'm all ears... 👂! 😊 Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Yes or No? One word, that's all I need! 💬! 😀! Come on... ⏩️! Don't keep me waiting! ⌛! Yes or No? Is it a yes or a no? Don't hold back, let me know! 😀! Tick-tock goes the clock... ⏰! Hurry, I'm waiting! Yes or No? One word, that's all I need! 💬! 😀! Come on... ⏩️!"]}, {'role': 'user', 'parts': ['yes']}, {'role': 'model', 'parts': ['Received hihihiha\n{\n  "CheckIn": "2023-01-30",\n  "CheckOut": "2023-02-04",\n  "City": "Goa",\n  "CountryName": null,\n  "GuestNationality": "Indian",\n  "PreferredCurrencyCode": "INR",\n  "PaxRooms": [\n    {\n      "Adults": 2,\n      "Children": 1,\n      "ChildrenAges": []\n    },\n    {\n      "Adults": 1,\n      "Children": 1,\n      "ChildrenAges": []\n    }\n  ],\n  "Filters": {\n    "MealType": "With Meal",\n    "Refundable": "true"\n  }\n}']}]
    dictString = """{
  "CheckIn": "2023-01-30",
  "CheckOut": "2023-02-04",
  "City": "Goa",
  "CountryName": null,
  "GuestNationality": "Indian",
  "PreferredCurrencyCode": "INR",
  "PaxRooms": [
    {
      "Adults": 2,
      "Children": 1,
      "ChildrenAges": []
    },
    {
      "Adults": 1,
      "Children": 1,
      "ChildrenAges": []
    }
  ],
  "Filters": {
    "MealType": "With Meal",
    "Refundable": "true"
  }
}"""
    if (dictString != ""):
        print(dictString)
        print("messages : //////////////////////////////////////////////////////////////")
        print(messages)
        print("////////////////////////////////////////")
        dictString = dictString.replace("Received hihihiha", "")
        dictString = dictString.replace("null", "-1")
        dictString.strip()
        print(dictString)
        userData = eval(dictString)
        print(userData)
        short_listed_hotels = short_list_hotels(messages, hotels)
        list(short_listed_hotels)
        print(short_listed_hotels)


main()
