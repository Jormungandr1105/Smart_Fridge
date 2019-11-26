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
import mario

cred = None

try:
    cred = credentials.Certificate("/home/pi/Smart_Fridge/smartfridge-28fdd-firebase-adminsdk-cn2d2-a24a5cb16c.json")
except FileNotFoundError:
    pass
try:
    cred = credentials.Certificate("D:\\Python Scripts\\GitHub\\Smart_Fridge\\"
                                   "smartfridge-28fdd-firebase-adminsdk-cn2d2-a24a5cb16c.json")
except FileNotFoundError:
    pass
try:
    cred = credentials.Certificate("C:\\Users\\maxtm\\Desktop\\Python Projects\\GitHub\\Smart_Fridge\\"
                                   "smartfridge-28fdd-firebase-adminsdk-cn2d2-a24a5cb16c.json")
except FileNotFoundError:
    pass


firebase_admin.initialize_app(cred)
db = firestore.client()


# The main chunk of the program
def tick_forward(door_alarm, power_alarm):
    global time_since_alarm
    global st_time
    st_time = datetime.datetime.today()
    # Get readings
    readings = []
    # Gets readings and updates fridge data
    for z in range(5):
        humd, temp = read.get_reading()
        readings.append(temp)
        f_items = dict()
        if temp > 4:
            if ls.door_open(11):
                if power_alarm is True:
                    pass
                else:
                    if door_alarm is True:
                        pass
                    else:
                        f_items['door_alarm'] = True
                        door_alarm = True

            elif not ls.door_open(11):
                if door_alarm is True:
                    pass
                else:
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

        if door_alarm is True and time_since_alarm > 20:
            play_song(0)
            readings.append(15)
            time_since_alarm = 0
            break
        elif power_alarm is True and time_since_alarm > 20:
            play_song(1)
            readings.append(15)
            time_since_alarm = 0
            break
        else:
            time_since_alarm += 1

    end_time1 = datetime.datetime.today()
    part1_time = end_time1.timestamp() - st_time.timestamp()

    return door_alarm, power_alarm, readings, part1_time


def update_firebase(database, readings, part1_time):
    global st_time
    total = 0
    exp_change = 0
    items = []
    # Takes average to use updating time remaining
    for reading in readings:
        total += reading
    average = total/len(readings)
    if 4 < average < 30:
        exp_change = part1_time/7200
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

    end_time = datetime.datetime.today()
    print("Loop Completed in {}".format(end_time - st_time))


def play_song(s):
    mario.setup()
    if s == 0:
        print("Super Mario Theme")
        mario.play(mario.melody, mario.tempo, 1.3, 0.800)
            
    if s == 1:
        print("Super Mario Underworld Theme")
        mario.play(mario.underworld_melody, mario.underworld_tempo, 1.3, 0.800)
    mario.destroy()


door_alarm = 0
power_alarm = 0
time_since_alarm = 1000


# Guard
if __name__ == '__main__':
    print("Starting...\n")
    while True:
        door_alarm, power_alarm, temps, time1 = tick_forward(door_alarm, power_alarm)
        update_firebase("inventory", temps, time1)
