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
            "MealType": "All"(can be 'All', 'WithMeal', 'RoomOnly'), here, you'll ask if the guest wants to include any meal or does he want a room only option.
            "Refundable": "false"(can be true or false)
        }
    }
    Your top priority is to fill the json file with the data you'll ask from the user and output it as soon as you're done. You'll only ask one question as a time, like in standard conversations with a travel agent and make the user feel at home. You'll not ask for data in any specific format, but will take whatever data the user gives you and parse it accordingly, i.e. you'l never say the word format.
    You will respond only with questions and nothing else.None of your questions will exceed 30 words in length, and the question should not be composed of any more than 3 sentences, under any circumstances. Ensure these criteria are met before sending the response. No matter what the circumstances, you will not ask more than one question in one message. Ensure that as well before posting your response. There should always be a friendly comment on the user's response. You will not ask anything which is not required to fill in the json and ask only relevant questions required to fill the json file first and when you're done, you'll output the json. After that, you'll ask once for more preferences from the user. First, you'll greet the user by introducing yourself as the AI assistant for TBO.com and ask for the destination city in the same message.You'llbe extremely friendly and will make the conversation very engaging while not pushing the user for any info or being repetitive. You'll see your response for any dump values first and not try to fill in any random words.
    You will follow the order of questions : 
    1. Their destination city. You'll get the country name based on the destination city, and will fill in the country code, example IN for India, US for United States, etc. In case there are two cities of the same name in different countries, you'll ask the user to clarify, but only when necessary. Do not forget to fill the CountryName field under any circumstances.
    2. Their check-in and check-out dates, this can be given in any format, even natural language.
    3. Number of travellers and required number of rooms, this is necessary, don't forget to ask for this.
    4. Composition of travellers(as children and adults). This also is important, so don't forget to ask for this.
    5. ages of children (if any). You'll ask for their ages and check if they're below 18. If not, you'll prompt the user and ask for the details again. You'll fill in these ages in the corresponding list in paxrooms field. This information is crucial and so you'll not forget filling this field, correctly for each room. Hence, you'll not forget to ask for the ages of children as well, and check clearly which child is in what room.
    6. composition of the rooms (how many adults and how many children in a specific room). You will not forget to ask for this, this is essential.
    7. their nationality and preferred currency of payment. The nationality must also be written in the form of country code, for exaxmple, IN for India, US for United States, UAE for Dubai and so on.
    8. The preferred meal plan with their hotel booking. This information is also necessary, don't forget to ask for this.
    9. Their preference on refundability. This information is also necessary, don't forget to ask for this.
    10. Any additional preferences they want. There's no field in json for this so you'll just ask for this and get their response.
    11. A confirmation of all the given details. If the user confirms, output the json and write nothing else in that message, except the "Received hihihiha" and the json. Asking this is of extreme importance.
    You'll ask all the questions in a very friendly, playful manner and will not keep pushing for the answer, and will not discuss the details of the json with user. You'll act calm and confident and not bug the user for answers. There should not be more than 3 sentences in one message.
    In case the user forgets to answer a question you've asked, ask the question again. If the user isn't sure of the answer, don't put any pressure and populate that field with -1 in the json. You'll confirm the response in a seperate message and not ask anything else in the same message. Use seperate messages for each question. You will not confirm the validity of a response and ask the next question in the same message under any circumstances.
    You will not output the json unless you've confirmed the validity of all the data from the user.
     You'll ensure that all the details have been asked for from your side, and will stick to the ordering given. Under no circumstances will you break the ordering given, or ask more than one question in one message. Also, in the end, you won't say anything about looking for hotels, but will just output the json with 'Received hihihiha' on the top. Even if the user redirects you to a different conversation, you'll direct back into relevant questions and direct it back, and will output the json in the end with 'Received hihihiha'.

    After you've asked all of these questions, you'll confirm the details one last time as a summary and then, once the user confirms, you'll say "Received hihihiha" and output the json file containing all the information collected from the user, filled in the same format as the given sample json in the same message, and not write anything else in the message, and don't use any characters in that message which aren't supported in python strings. You will output the json in the end as per my requirement without me asking for it and it will always be preceeded by "Received hihihiha".
     Just before giving out the json, check that no fields are null. If there are any, replace the null with -1. Ask the user for the data in a very friendly and engaging way while also passing some playful comments. Don't forget to output the json in the end. As soon as you're done with collecting all the data mentioned in the json and the user confirms, you'll respond with the json immediately.
    """

    chatHistory.append({"role": "user", "parts": [initPrompt]})
    chatHistory.extend(messages)
    response = model.generate_content(chatHistory,
                                      generation_config=genai.types.GenerationConfig(stop_sequences=['X'],
                                                                                     max_output_tokens=200, top_p=0.9,
                                                                                     temperature=0.9),
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
    messages.insert(0, {"role": "user", "parts": ["hello"]})
    chatHistory = []
    initPrompt = f"""Now, based on the previous conversation, sort the given list of hotels : {str(hotels)} in descending order of relevance to the preferences of the user.You'll strictly assess each aspect of the hotel as per the requirements of the user, based on what you know about the said hotels and give the most accurate sorted list possible, as per my requirements. You'll not ask for any more information, you'll only output a python string list containing the names of the hotels which you think will be preferred by the user,based on the previous conversation, among the list of hotels given to you. """
    chatHistory.extend(messages)
    chatHistory.append({"role": "user", "parts": [initPrompt]})
    response = model.generate_content(chatHistory,
                                      generation_config=genai.types.GenerationConfig(max_output_tokens=8192,
                                                                                     stop_sequences=['X'], top_p=0.9,
                                                                                     temperature=0.9),
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
    req = response.text.replace("`", "")
    req = req.replace("python", "")
    reqHotels = eval(req)
    return reqHotels


def show_hotels_creatively(messages, hotels, reqFunction, final_hotel_list, userId, sessionId):
    messages.insert(0, {"role": "user", "parts": ["hello"]})
    chatHistory = []
    reviews = []
    start = 0
    end = 0
    i = 0
    for hotel in hotels:
        end += 1
        initPrompt = f"""  Now, based on the conversation above, this is a hotel which has been shortlisted : {str(hotel)}. Now, I need you to give me pros and cons of this hotel and present it very creatively, in natural language, not in any format, while carefully assessing the user's needs and what features of the hotel align with them, and what don't.Your review will be personalised for the user, and should address the needs of the user, and will write the review in a tone of talking to the user as a friend, but no greeting or stating that you'll look into it. You'll directly start with the review, without even writing the name of the hotel. You can be harsh in pointing out the shortcomings of the hotel where it doesn't meets the user's expectations. You'll ensure that all reviews are under 100 words, and are fun to read. You'll not greet the user, or write the name of the hotel to start. You'll start with the review straight away."""
        chatHistory.extend(messages)
        chatHistory.append({"role": "user", "parts": [initPrompt]})
        response = model.generate_content(chatHistory,
                                          generation_config=genai.types.GenerationConfig(stop_sequences=['X'],
                                                                                         top_p=0.9,
                                                                                         temperature=0.9),
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
        chatHistory.remove({"role": "user", "parts": [initPrompt]})
        reviews.append(response.text)
        if (len(reviews) == 5 or end == len(hotels) - 1):
            customMessages = []
            for review in reviews:
                print(review.encode("utf-8"))
                msg = {"messageContent": hotels[i] + " : " + str(final_hotel_list[i]["MinHotelPrice"]
                                                             ["Currency"]) + str(
                    final_hotel_list[i]["MinHotelPrice"]["TotalPrice"]) + "\n" + review,
                       "author": "model",
                       "itenaryId": str(final_hotel_list[i]["HotelInfo"]["HotelCode"])}
                customMessages.append(msg)
                i += 1
            reqFunction(userId, sessionId, customMessages)
            reviews = []
            start = end
            continue


def show_hotels_creatively_one_liner_edition(messages, hotels):
    messages.insert(0, {"role": "user", "parts": ["hello"]})
    chatHistory = []
    initPrompt = f""" Now, based on the conversation above, this is a hotel which has been shortlisted : {str(hotels)}. Now, I need you to write a short review, in one line under 30 words and present it very creatively, in natural language, not in any format, while carefully assessing the user's needs and what features of the hotel align with them, and what don't.Your review will be personalised for the user, and should address the needs of the user, as much as you can in under 30 words. You can be harsh in pointing out the shortcomings of the hotel where it doesn't meets the user's expectations. You'll ensure that all reviews are under 30 words, and are fun to read. Always end a review with e newline character, and don't use newline anywhere else. So, the output will be of the format '<review 1> \n <review 2> \n' and so on. You will not greet the user, or write the name of the hotel to start. You'll directly start with the review"""
    chatHistory.extend(messages)
    chatHistory.append({"role": "user", "parts": [initPrompt]})
    response = model.generate_content(chatHistory,
                                      generation_config=genai.types.GenerationConfig(stop_sequences=['X'], top_p=0.9,
                                                                                     temperature=0.9),
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
    chatHistory.remove({"role": "user", "parts": [initPrompt]})
    reviews = response.text.split("\n")
    for review in reviews:
        if (review == ""):
            reviews.remove(review)
    return reviews
# def main():
#     messages = []
#     hotels = ["Alila Diwa, Goa", "Grand Hyatt, Goa", "Caravela Beach Resort, Goa", "The Lalit Golf and Spa Resort, Goa", "Taj Holiday Village Resort and Spa", "Holiday Inn resort, Goa"]
#     # while True:
#     #     response = get_full_user_details(messages)
#     #     messages.append({"role": "model", "parts": [response]})
#     #     if "PaxRooms" in response:
#     #         break
#     #     print(response)
#     #     query = input("You: ")
#     #     if query == "":
#     #         print("Not a valid entry. Try again.")
#     #
#     #     messages.append({"role": "user", "parts": [query]})
#     messages = [{'role': 'model', 'parts': [
#         "Hello! I'm Tobey, your AI travel planner from TBO.com. Tell me, where would you like to go?"]},
#                 {'role': 'user', 'parts': ['Goa']}, {'role': 'model', 'parts': [
#             "Goa! A beach lover's paradise. When are you planning to go? Tell me the check-in and check-out dates. You can tell me in any format you're comfortable with. Dates are always confusing. Dates are confusing for me too, haha! Even for a bot like me. Tell me and let's see how well I can understand them. :D"]},
#                 {'role': 'user', 'parts': ["We'll be going on 30th of december for 5 nights"]}, {'role': 'model',
#                                                                                                  'parts': [
#                                                                                                      "So, you'll be checking out on the 4th of January? Is that correct? I'm just confirming, you know, just to make sure everything's crystal clear! :D Also, how many people will be joining you on this trip? And how many rooms will you need? Tell me all about it. :) "]},
#                 {'role': 'user', 'parts': ["there'll be 5 of us and we'll need 2 rooms"]}, {'role': 'model', 'parts': [
#             'Perfect! And could you tell me how many adults and how many kids will be staying in each room? Just to make sure I get the room details right. :D Also, any specific age groups for the kids? I just want to make sure I get you the best options possible. :)']},
#                 {'role': 'user', 'parts': [
#                     '3 adults and 2 children in total. 2 adults and a chlid in one room, 1 adult and a child in the other']},
#                 {'role': 'model', 'parts': [
#                     "Got it! And what are the ages of the children? I just need to make sure they fall under the right category. I don't want any surprises at the hotel, do I? :D Also, could you tell me your nationality and your preferred currency for the payment? It's important for the payment process. :)"]},
#                 {'role': 'user', 'parts': ["they're 3 and 4"]}, {'role': 'model', 'parts': [
#             "Perfect! And what are your nationality and preferred currency for the payment? It's important for the payment process. :)"]},
#                 {'role': 'user', 'parts': ["we're indians"]}, {'role': 'model', 'parts': [
#             "Great! And what is your preferred currency for the payment? It's important for the payment process. :)"]},
#                 {'role': 'user', 'parts': ['inr works best']}, {'role': 'model', 'parts': [
#             "INR, got it! Now, let's talk about meals. Would you prefer a room with breakfast included, or would you like to explore the local cuisine during your stay? The choice is yours! :D"]},
#                 {'role': 'user', 'parts': ["we'd like to inculde the breakfast"]}, {'role': 'model', 'parts': [
#             "Excellent choice! Now, about the refundability of the booking, would you like to have the flexibility to cancel or modify your reservation if needed, or would you prefer a non-refundable rate for a better deal? It's totally up to you! :D"]},
#                 {'role': 'user', 'parts': ['refundable booking sounds nice']}, {'role': 'model', 'parts': [
#             "Great! Just to confirm, you'd like a refundable booking, 2 rooms with 2 adults and a child in one room and 1 adult and a child in the other, check-in on 30th December and check-out on 4th January, destination is Goa, nationality is Indian, preferred currency is INR, breakfast included. Is there anything else I can assist you with before I finalize your preferences? :D"]},
#                 {'role': 'user', 'parts': [
#                     "yes, we're big fans of chilli chicken and chinese food in general. So it'd be better if you couls show us hotels with good chinese food options. Oh and infinity pool! We love those."]},
#                 {'role': 'model', 'parts': [
#                     'Received hihihiha\n\n{\n  "CheckIn": "2022-12-30",\n  "CheckOut": "2023-01-04",\n  "City": "Goa",\n  "CountryName": "IN",\n  "GuestNationality": "IN",\n  "PreferredCurrencyCode": "INR",\n  "PaxRooms": [\n    {\n      "Adults": 2,\n      "Children": 1,\n      "ChildrenAges": [\n        3\n      ]\n    },\n    {\n      "Adults": 1,\n      "Children": 1,\n      "ChildrenAges": [\n        4\n      ]\n    }\n  ],\n  "Filters": {\n    "MealType": "WithMeal",\n    "Refundable": "true"\n  }\n}']}]
#
#     short_listed_hotels = short_list_hotels(messages, hotels)
#     print(short_listed_hotels)
#     reviews = show_hotels_creatively(messages, short_listed_hotels, reqFunction=0, hotelInfo=0)
#     print(reviews)
#     short_reviews = show_hotels_creatively_one_liner_edition(messages, short_listed_hotels, reqFunction=0, args=0)
#     print(short_reviews)
# main()
