
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("connected with result code {0}".format(str(rc)))
    client.subscribe("testing/junk")

def on_message(client, userdata, msg):
    print("Message received-> %s %s" % (msg.topic, str(msg.payload)))

client = mqtt.Client("epaper_display")
client.on_connect = on_connect
client.on_message = on_message

client.connect('192.168.1.171', 1883)
client.loop_forever()

