#smartclassroom
#set PYTHONPATH = C:/Users/ASUS/AppData/Local/Programs/Python/Python311/Lib/site-packages:%PYTHONPATH%
import paho.mqtt.client as mqtt
import time
import logging
topicid = 0
lenh = "on"
fan_topics = ["/AIRC/FAN1/", "/AIRC/FAN2/", "/AIRC/FAN3/", "/AIRC/FAN4/", "/AIRC/FAN5/", "/AIRC/FAN6/"]
led_topics = ["/AIRC/LED1/", "/AIRC/LED2/", "/AIRC/LED3/", "/AIRC/LED4/", "/AIRC/LED5/", "/AIRC/LED6/"]
#===============================================================================
mqtt_broker = "broker.emqx.io"
mqtt_port = 1883
version = '5'
mytransport = 'tcp'
if version == '5':
    client = mqtt.Client(client_id="MQTT_VO",
                        transport=mytransport,
                        protocol=mqtt.MQTTv5)
if version == '5':
    from paho.mqtt.properties import Properties
    from paho.mqtt.packettypes import PacketTypes
    myproperties=Properties(PacketTypes.CONNECT)
    myproperties.SessionExpiryInterval=30*60  # in seconds
    client.connect(mqtt_broker, port=mqtt_port,
                  clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                  properties=myproperties,
                  keepalive=60);
client.username_pw_set("tronvo", "311284")

def on_connect(client, userdata, flags, rc, myproperties):
    if rc == 0:
        print("Connected!")
    else:
        print("Failed to connect, return code %d\n", rc)
client.on_connect=on_connect

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60
def on_disconnect(client, userdata, rc):
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        time.sleep(reconnect_delay)
        try:
            client.reconnect()
            return
        except Exception as err:
            print("Reconnect failed. Retrying...")
        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
client.on_disconnect = on_disconnect
#-------------------------------------------------------------------------------
def vop(topicid, lenh):
    from paho.mqtt.properties import Properties
    from paho.mqtt.packettypes import PacketTypes
    myproperties=Properties(PacketTypes.PUBLISH)
    myproperties.MessageExpiryInterval=30   # in seconds
    topic = led_topics[topicid]

    client.publish(topic, lenh, qos = 2,properties=myproperties);

#-------------------------------------------------------------------------------
def vos(client: mqtt, topicid):
    topic =led_topics[topicid]
    def on_message(client, userdata, msg):
      for led_topic in led_topics:
        if msg.topic == led_topic:
            led_value = msg.payload.decode()
            print(f"LED value of {led_topic}: {led_value}")
            topic = msg.topic
            break 
    client.subscribe(topic, qos = 2)
    client.on_message = on_message
client.loop_start()
vop(topicid, lenh)
vos(client, topicid)
client.loop_stop()
