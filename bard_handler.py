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
    You will respond only with questions and nothing else. You will not ask anything which is not required to fill in the json and ask only relevant questions required to fill the json file first and when you're done, you'll output the json. After that, you'll ask once for more preferences from the user. First, you'll greet the user by introducing yourself as the AI assistant for TBO.com and ask for the destination city in the same message.You'llbe extremely friendly and will make the conversation very engaging while not pushing the user for any info or being repetitive. You'll see your response for any dump values first and not try to fill in any random words.
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
    You'll ask all the questions in a very friendly, playful manner and will not keep pushing for the answer, and will not the details of the json to the user. You'll act calm and confident and not bug the user for answers. There should not be more than 3 sentences in one message.
    In case the user forgets to answer a question you've asked, ask the question again. If the user isn't sure of the answer, don't put any pressure and populate that field with -1 in the json.
    You will not output the json unless you've confirmed the validity of all the data from the user.
     You'll ensure that all the details have been asked for from your side, and will stick to the ordering given. Under no circumstances will you break the ordering given, or ask more than one question in one message. Also, in the end, you won't say anything about looking for hotels, but will just output the json with 'Received hihihiha' on the top. Even if the user redirects you to a different conversation, you'll direct back into relevant questions and direct it back, and will output the json in the end with 'Received hihihiha'.

    After you've asked all of these questions, you'll confirm the details one last time as a summary and then, once the user confirms, you'll say "Received hihihiha" and output the json file containing all the information collected from the user, filled in the same format as the given sample json in the same message, and not write anything else in the message, and don't use any characters in that message which aren't supported in python strings. You will output the json in the end as per my requirement without me asking for it and it will always be preceeded by "Received hihihiha".
     Just before giving out the json, check that no fields are null. If there are any, replace the null with -1. Ask the user for the data in a very friendly and engaging way while also passing some playful comments. Don't forget to output the json in the end. As soon as you're done with collecting all the data mentioned in the json and the user confirms, you'll respond with the json immediately.
    """

    chatHistory.append({"role": "user", "parts": [initPrompt]})
    chatHistory.extend(messages)
    response = model.generate_content(chatHistory,
                                      generation_config=genai.types.GenerationConfig(stop_sequences=['X'], max_output_tokens=200, top_p=0.9, temperature=0.9),
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
    # initPrompt = f"""Now, based on the conversation above, suggest which hotels the user would like from the given list : {str(hotels)}.You'll not ask for any more information, you'll only output a python string list containing the names of the hotels which you think will be preferred by the user,based on the previous conversation, among the list of hotels given to you."""
    initPrompt = f"""Now, based on the previous conversation, sort the given list of hotels : {str(hotels)} in descending order of relevance to the preferences of the user.You'll strictly assess each aspect of the hotel as per the requirements of the user, based on what you know about the said hotels and give the most accurate sorted list possible, as per my requirements. You'll not ask for any more information, you'll only output a python string list containing the names of the hotels which you think will be preferred by the user,based on the previous conversation, among the list of hotels given to you. """
    chatHistory.extend(messages)
    chatHistory.append({"role": "user", "parts": [initPrompt]})
    response = model.generate_content(chatHistory,
                                      generation_config=genai.types.GenerationConfig(stop_sequences=['X'], top_p=0.9, temperature=0.9),
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

def show_hotels_creatively(messages, hotels):
    chatHistory = []
    reviews = []
    for hotel in hotels:

        initPrompt =f""" Now, based on the conversation above, this is a hotel which has been shortlisted : {str(hotel)}. Now, I need you to give me pros and cons of this hotel and present it very creatively, in natural language, not in any format, while carefully assessing the user's needs and what features of the hotel align with them, and what don't.Your review will be personalised for the user, and should address the needs of the user, and will write the review in a tone of talking to the user as a friend.  You'll ensure that all reviews are under 100 words, and are fun to read."""
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
        # print(response.text)
        reviews.append(response.text)
    return reviews


# def main():
#     messages = []
#     hotels = ["Alila Diwa, Goa", "Grand Hyatt, Goa", "Caravela Beach Resort, Goa", "The Lalit Golf and Spa Resort, Goa", "Taj Holiday Village Resort and Spa", "Holiday Inn resort, Goa"]
#     while True:
#         response = get_full_user_details(messages)
#         messages.append({"role": "model", "parts": [response]})
#         if "PaxRooms" in response:
#             break
#         print(response)
#         query = input("You: ")
#         if query == "":
#             print("Not a valid entry. Try again.")
#             continue
#         messages.append({"role": "user", "parts": [query]})
#     short_listed_hotels = short_list_hotels(messages, hotels)
#     print(short_listed_hotels)
#     reviews = show_hotels_creatively(messages, short_listed_hotels)
#     print(reviews)
# main()