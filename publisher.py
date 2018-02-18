from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.exceptions import PubNubException
from pubnub.pubnub import PubNub
from random import *
import time

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-cb6369c0-0fdf-11e8-91c1-eac6831c625c'
pnconfig.publish_key = 'pub-c-50d55c74-1141-477e-9456-36f1126859c1'

pubnub = PubNub(pnconfig)

#Set default variables
light = 'green'
vel = 50
temp = 21.2
status = 'OK'

#Traffic lights changes manager
def lights (light):
    if (light == 'green'):
        light = 'yellow'
        return light
    if (light == 'yellow'):
        light = 'red'
        return light
    if (light == 'red'):
        light = 'green'
        return light

def speed_limit(n_cars, status, vel):
    if (status == 'DANGER'):
        vel = 20
        return vel
    if (n_cars >= 15):
        vel = 30
        return vel
    if (n_cars <= 3):
        vel = 70
        return vel
    if (n_cars < 15 and n_cars > 3):
        vel = 50
        return vel

#Send message function
def send_message(mes):
    try:
        envelope = pubnub.publish().channel("proyecto").message(mes).sync()
        print("publish timetoken: %d" % envelope.result.timetoken)
    except PubNubException as e:
        print e

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):

        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            print "entramos en publish"
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel("proyecto").message("hello!!").async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
    def message(self, pubnub, message):

        pass  # Handle new message stored in message.message
#pubnub.publish().channel("proyecto").message("hello!!").async(my_publish_callback)

#Running
while True:
    #Local time
    localtime = time.localtime(time.time())
    #Set number of cars and speed limits
    n_cars = randint(0,20)
    vel = speed_limit(n_cars, status, vel)
    #Message definition
    mes = {
        'id_node': '1sem24',
        'type': 'traffic light',
        'gps_x': 39.481411,
        'gps_y': -0.350458,
        'lights': light,
        'n_cars': n_cars,
        'speed_limit': '%d km'%(vel),
        'time': '%d H:%d m:%d s' %(localtime.tm_hour+2,localtime.tm_min,localtime.tm_sec),
        'date': '%d/%d/%d' %(localtime.tm_mday,localtime.tm_mon,localtime.tm_year),
        'temp': '%.1f C' %(temp),
        'status': status,
        'online': True
    }
    #Call send message function
    send_message(unicode(mes))

    #Traffic lights changes
    if (light == 'yellow'):
        time.sleep(5)
        light = lights(light)
    else:
        time.sleep(15)
        light = lights(light)

    pubnub.add_listener(MySubscribeCallback())
