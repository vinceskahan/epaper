
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("connected with result code {0}".format(str(rc)))
    client.subscribe("vp2/outTemp")

def on_message(client, userdata, msg):
    print(str(msg.payload.decode('utf-8')) + " degF" )
    client.disconnect()

client = mqtt.Client("epaper_display")
client.on_connect = on_connect
client.on_message = on_message

client.connect('192.168.1.171', 1883)
client.loop_forever()

