"""
This part communicates with the database

Author: Max Marshall
Project: Fridge Tracker
"""
import datetime
import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import readings as read

cred = credentials.Certificate("C:\\Users\\maxtm\\Dropbox\\Shared Python Files\\IED\\Fridge Tracker\\"
                               "smartfridge-28fdd-firebase-adminsdk-cn2d2-a24a5cb16c.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# The main chunk of the program
def tick_forward(database, alarm):
    items = []
    # Get readings
    readings = []
    total = 0
    exp_change = 0
    # Gets readings and updates fridge data
    for z in range(15):
        temp, humd = read.get_reading()
        readings.append(temp)
        f_items = dict()
        if temp >= 40 and humd >= 70:
            if alarm is True:
                pass
            else:
                f_items['alarm'] = True
                alarm = True
        else:
            f_items['alarm'] = False
            alarm = False
        f_items['humidity'] = humd
        f_items["temperature"] = temp
        f_data_ref = db.collection(u'{}'.format('fridge_data')).document(u'{}'.format("data"))
        f_data_ref.set(f_items, merge=True)
    # Takes average to use updating time remaining
    for reading in readings:
        total += reading
    average = total/len(readings)
    if 40 < average < 90:
        exp_change = 0.00208333333

    # Get items from firebase
    data_ref = db.collection(u'{}'.format(database))
    docs = data_ref.stream()
    for doc in docs:
        items.append((doc.id, doc.to_dict()))

    # For each item, updates date info
    for item in items:
        z = item[1]['expDate']
        y = item[1]['addDate']
        z = float(z)
        y = float(y)
        z = z - (exp_change * (z - y))
        current_time = datetime.datetime.today()
        ct_mils = (current_time.timestamp()*1000)
        item[1]['expDate'] = int(z)
        item[1]['daysOld'] = math.floor((ct_mils - y) / 80640000)
        item[1]['daysLeft'] = math.ceil((z - ct_mils) / 80640000)

    # This bit updates the firebase
    for item in items:
        new_data_ref = db.collection(u'{}'.format(database)).document(u'{}'.format(item[0]))
        new_data = dict()
        for dict_item in item[1]:
            if isinstance(item[1][dict_item], str):
                new_data[u'{}'.format(dict_item)] = u'{}'.format(item[1][dict_item])
            elif isinstance(item[1][dict_item], int):
                new_data[u'{}'.format(dict_item)] = item[1][dict_item]
        new_data_ref.set(new_data)

    return alarm


alarm = 0

# Guard
if __name__ == '__main__':
    user_input = input("Enter Collection ==> ")
    for x in range(50):
        alarm = tick_forward(user_input, alarm)
        print("TICK")
