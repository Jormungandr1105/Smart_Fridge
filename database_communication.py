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
import light_sensor as ls

cred = credentials.Certificate("/home/pi/Smart_Fridge/smartfridge-28fdd-firebase-adminsdk-cn2d2-a24a5cb16c.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# The main chunk of the program
def tick_forward(database, door_alarm, power_alarm):
    st_time = datetime.datetime.today()
    items = []
    # Get readings
    readings = []
    total = 0
    exp_change = 0
    # Gets readings and updates fridge data
    for z in range(15):
        humd, temp = read.get_reading()
        #readings.append(temp)
        f_items = dict()
        if temp >= 10:
            if ls.door_open(11):
                if door_alarm is True:
                    pass
                else:
                    f_items['door_alarm'] = True
                    door_alarm = True
                    
            elif not ls.door_open(11):
                if power_alarm is True:
                    pass
                else:
                    f_items['power_alarm'] = True
                    power_alarm = True
        else:
            f_items['door_alarm'] = False
            f_items['power_alarm'] = False
            door_alarm = False
            power_alarm = False
        f_items['humidity'] = humd
        f_items["temperature"] = int((temp * 1.8) + 32)
        f_data_ref = db.collection(u'{}'.format('fridge_data')).document(u'{}'.format("data"))
        f_data_ref.set(f_items, merge=True)
    # Takes average to use updating time remaining
    """
    Temp Comment to Test
    for reading in readings:
        total += reading
    average = total/len(readings)
    if 10 < average < 50:
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
    """
    
    end_time = datetime.datetime.today()
    print(end_time - st_time)

    return door_alarm, power_alarm


door_alarm = 0
power_alarm = 0

# Guard
if __name__ == '__main__':
    print("sTART")
    while True:
        door_alarm, power_alarm = tick_forward('inventory', door_alarm, power_alarm)
        print("TICK")
