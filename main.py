from fastapi import Request, FastAPI
import tbo_handler as tbo
import services
import firebase_db
import bard_handler

app = FastAPI()


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
    if "Received hihihiha" in curr:
        curr = services.convert_string_to_json(curr)
        curr = services.make_json_searchable(curr)
        hotels = tbo.search_hotels(curr)
        if len(hotels) == 0:
            msg = {"messageContent": "Sorry but we were unable to find any hotels that match your criteria.",
                   "author": "model", "itenaryId": ""}
            firebase_db.add_message_to_user_session(userId, sessionId, msg)
            firebase_db.make_user_session_complete(userId, sessionId)
            return "ok"
        if hotels is not None:
            if True:
                hotel_names = []
                for hotel in hotels:
                    hotel_names.append(hotel["HotelInfo"]["HotelName"])
                hotel_names = bard_handler.short_list_hotels(messages, hotel_names)
                final_hotel_list = []
                final_hotel_name_list = []
                for hotel in hotels:
                    if hotel["HotelInfo"]["HotelName"] in hotel_names:
                        final_hotel_list.append(hotel)
                        final_hotel_name_list.append(hotel["HotelInfo"]["HotelName"])
                creative_result = bard_handler.show_hotels_creatively(messages, final_hotel_name_list)
                i = 0
                hotels = []
                for creative in creative_result:
                    msg = {"messageContent": final_hotel_name_list[i] + " : " + final_hotel_list[i]["MinHotelPrice"]
                    ["Currency"] + final_hotel_list[i]["MinHotelPrice"]["TotalPrice"] + "\n" + creative,
                           "author": "model",
                           "itenaryId": final_hotel_list[i]["HotelInfo"]["HotelCode"]}
                    hotels.append(msg)
                    i += 1
                i = 0
                for hotel in hotels:
                    if i >= 5:
                        break
                    firebase_db.add_message_to_user_session(userId, sessionId, hotel)
                    i += 1
                firebase_db.make_user_session_complete(userId, sessionId)
                firebase_db.add_hotels_to_user_session(userId, sessionId, hotels)
                return "ok"
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
