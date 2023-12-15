import firebase_admin
from firebase_admin import credentials, firestore
import time

def current_milli_time():
    return str(round(time.time() * 1000))

cred = credentials.Certificate("tobey-server-firebase-adminsdk-zjpzl-6194f79440.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
users_ref = db.collection("users")

def save_itenary(userId, itenary):
    pass

def create_user_session(userId, msg):
    (users_ref.document(userId).collection(current_milli_time())
     .document("1").set(msg))
    pass


def add_message_to_user_session(userId, sessionId, msg):
    users_ref.document(userId).collection(sessionId).document(current_milli_time()).set(msg)
    pass