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
        print("in if")
        curr = services.convert_string_to_json(curr)
        curr = services.make_json_searchable(curr)
        hotels = tbo.search_hotels(curr)
        if hotels is not None:
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
            creative_result = bard_handler.show_hotels_creatively(final_hotel_name_list)
            for creative in creative_result:
                msg = {"messageContent": creative, "author": "model",
                       "itenaryId": final_hotel_list["HotelInfo"]["HotelCode"]}
                firebase_db.add_message_to_user_session(userId, sessionId, msg)
            return "ok"
        if hotels is None:
            return "no hotels found"
    msg = {"messageContent": curr, "author": "model", "itenaryId": ""}
    firebase_db.add_message_to_user_session(userId, sessionId, msg)
    print(msg,"end")
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
    msg = {"messageContent":message, "author": "user", "itenaryId":""}
    firebase_db.add_message_to_user_session(userId, sessionId, msg)
    return "ok"