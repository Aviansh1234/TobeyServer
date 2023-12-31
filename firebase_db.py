import firebase_admin
from firebase_admin import credentials, firestore
import time
import config


def current_milli_time():
    return str(round(time.time() * 1000))


cred = credentials.Certificate(config.firebase_key_path)
app = firebase_admin.initialize_app(cred)
db = firestore.client()
users_ref = db.collection("users")


def create_user_session(userId, msg):
    id = current_milli_time()
    (users_ref.document(userId).collection(id)
     .document("1").set({"messageContent": msg, "location": "", "departTime": "", "author": "model", "itenaryId": ""}))
    return id


def add_message_to_user_session(userId, sessionId, msg):
    users_ref.document(userId).collection(sessionId).document(current_milli_time()).set(msg)


def get_user_session(userId, sessionId):
    docs = users_ref.document(userId).collection(sessionId).stream()
    arr = []
    for doc in docs:
        arr.append(doc.to_dict())
    return arr


def make_user_session_complete(userId, sessionId):
    users_ref.document(userId).collection(sessionId).document('1').update({"complete": True})


def add_data_to_session(userId, sessionId, location, departTime):
    users_ref.document(userId).collection(sessionId).document('1').update(
        {"location": location, "departTime": departTime})
    users_ref.document(userId).update({"trigger": current_milli_time()})


def add_hotels_to_user_session(userId, sessionId, hotels):
    for hotel in hotels:
        users_ref.document(userId).collection(sessionId + " : hotels").document(current_milli_time()).set(hotel)
