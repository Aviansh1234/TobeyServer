from fastapi import FastAPI
import tbo_handler as tbo
import services
import threading
import firebase_db
import bard_handler

app = FastAPI()


def found_json(curr, userId, sessionId, messages):
    curr = services.convert_string_to_json(curr)
    loc = curr["City"]
    depTime = curr["CheckIn"]
    curr = services.make_json_searchable(curr)
    print(curr)
    hotels = tbo.search_hotels(curr)
    if len(hotels) == 0:
        msg = {"messageContent": "Sorry but we were unable to find any hotels that match your criteria.",
               "author": "model", "itenaryId": ""}
        firebase_db.add_message_to_user_session(userId, sessionId, msg)
        firebase_db.make_user_session_complete(userId, sessionId)
    if hotels is not None:
        hotels = hotels[0:10]
        if True:
            hotel_names = []
            for hotel in hotels:
                hotel_names.append(hotel["HotelInfo"]["HotelName"])
            hotel_names = bard_handler.short_list_hotels(messages[0:-1], hotel_names)
            final_hotel_list = []
            final_hotel_name_list = []

            print(hotels)
            for hotel in hotels:
                if hotel["HotelInfo"]["HotelName"] in hotel_names:
                    final_hotel_list.append(hotel)
                    final_hotel_name_list.append(hotel["HotelInfo"]["HotelName"])
            firebase_db.add_data_to_session(userId, sessionId, loc, depTime)
            creative_result = bard_handler.show_hotels_creatively_one_liner_edition(messages[0:-1],
                                                                                    final_hotel_name_list[:5])
            firebase_db.make_user_session_complete(userId, sessionId)
            i = 0
            hotels = []
            for creative in creative_result:
                msg = {"messageContent": final_hotel_name_list[i] + " : " + str(final_hotel_list[i]["MinHotelPrice"]
                                                                                ["Currency"]) + str(
                    final_hotel_list[i]["MinHotelPrice"]["TotalPrice"]) + "\n" + creative,
                       "author": "model",
                       "itenaryId": str(final_hotel_list[i]["HotelInfo"]["HotelCode"])}
                hotels.append(msg)
                i += 1
            i = 0
            for hotel in hotels:
                if i >= 5:
                    break
                firebase_db.add_message_to_user_session(userId, sessionId, hotel)
                i += 1
            bard_handler.show_hotels_creatively(messages[0:-1], final_hotel_name_list,
                                                firebase_db.add_hotels_to_user_session, final_hotel_list, userId,
                                                sessionId)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/updateForNext")
async def updateForNext(sessionId: str, userId: str):
    messages = firebase_db.get_user_session(userId, sessionId)
    messages = services.convert_firebase_msg_to_bard(messages)
    curr = bard_handler.get_full_user_details(messages)
    print(curr)
    if "Received hihihiha" in curr:
        thread = threading.Thread(target=found_json, args=(curr, userId, sessionId, messages,))
        thread.start()
        return "show loading"
    msg = {"messageContent": curr, "author": "model", "itenaryId": ""}
    firebase_db.add_message_to_user_session(userId, sessionId, msg)
    return "ok"


@app.get("/getHotelInfo")
async def get_hotel_info(hotelId: str):
    return tbo.get_hotel_info(hotelId)


@app.get("/createNewSession")
async def create_new_session(userId: str):
    return firebase_db.create_user_session(userId,
                                           "Hello, I am Tobey, your AI travel assistant,\nWhere would you like to go?")


@app.get("/addMessage")
async def add_message(userId: str, sessionId: str, message: str):
    msg = {"messageContent": message, "author": "user", "itenaryId": ""}
    firebase_db.add_message_to_user_session(userId, sessionId, msg)
    return "ok"
