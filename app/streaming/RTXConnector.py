from logging import error

from kafka import KafkaConsumer
from kafka import KafkaProducer
from app import Config
import msgpack, sys
from colorama import Fore
import json

# Starting the producer
consumer = None
mqttClient = None
mqttQueue = []

def on_message(client, userdata, message):
    print("message received")
    # we deserialize each message that comes from mqtt and store it in a queue
    mqttQueue.append(json.loads(message.payload.decode('utf-8')))

# Try to connect to Kafka, else exits the process
def connect():
    if Config.kafkaUpdates:
        try:
            global consumer
            consumer = KafkaConsumer(bootstrap_servers="glider.srvs.cloudkafka.com:9094",
                                     sasl_plain_username="ejmgtktq",
                                     sasl_plain_password="eB71RaFxPqhECa5ojKD9_Zu0MAw3_62K",
                                     value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                     group_id=None,
                                     sasl_mechanism="SCRAM-SHA-512",
                                     security_protocol="SASL_SSL",
                                     consumer_timeout_ms=100)
            consumer.subscribe([Config.kafkaCommandsTopic])
            print(Fore.GREEN + '# KafkaConnector OK!' + Fore.RESET)
        except RuntimeError:
            sys.exit(Fore.RED + "Connection to Kafka failed!" + Fore.RESET)
    if Config.mqttUpdates:
        try:
            global mqttClient
            import paho.mqtt.client as mqtt
            # create mqtt client and connect
            mqttClient = mqtt.Client()
            mqttClient.connect(Config.mqttHost, port=Config.mqttPort)
            # register callback
            mqttClient.on_message = on_message
            # subscribe and start listing on second thread
            mqttClient.subscribe(Config.kafkaCommandsTopic, 0)
            mqttClient.loop_start()
        except RuntimeError:
            sys.exit(Fore.RED + "Connection to MQTT failed!" + Fore.RESET)


# checks if we got a new configuration from the server
def checkForNewConfiguration():
    if Config.mqttUpdates:
        try:
            return mqttQueue.pop(0)
        except:
            return None
    if Config.kafkaUpdates:
        try:
            # @todo get last value
            return next(consumer).value
        except:
            return None
    else:
        return None