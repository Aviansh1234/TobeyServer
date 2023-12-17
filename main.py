from fastapi import Request, FastAPI
import tbo_handler as tbo

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/getHotelInfo")
async def get_hotel_info(hotelId):
    return tbo.get_hotel_info(hotelId)
