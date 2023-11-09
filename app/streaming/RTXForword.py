from kafka import KafkaProducer
from app import Config
import msgpack, sys
from colorama import Fore
import json

# Starting the producer
producer = None


# Try to connect to Kafka, else exits the process
def connect():
    if Config.kafkaUpdates:
        try:
            global producer
            producer = KafkaProducer(bootstrap_servers="glider.srvs.cloudkafka.com:9094",
                                     sasl_plain_username="ejmgtktq",
                                     sasl_plain_password="eB71RaFxPqhECa5ojKD9_Zu0MAw3_62K",
                                     value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                     sasl_mechanism="SCRAM-SHA-512",
                                     security_protocol="SASL_SSL",
                                     request_timeout_ms=5000)
            print(Fore.GREEN + '# StreamForword OK!' + Fore.RESET)
        except RuntimeError:
            sys.exit(Fore.RED + "Connection to Kafka failed!" + Fore.RESET)


# Publishes a message to the configured kafka server
def publish(message,topic):
    if Config.mqttUpdates:
        from paho.mqtt import publish
        try:
            publish.single(topic, payload=json.dumps(message).encode('utf-8'),
                       qos=0, retain=False, hostname=Config.mqttHost,
                       port=Config.mqttPort, client_id="CrowdNav", keepalive=60)
        except:
            print("Error sending mqtt status")
    if Config.kafkaUpdates:
        try:
            producer.send(topic, message)
        except Exception as e:
            print(str(e))
            print("Error sending kafka status")
    else:
        # we ignore this in json mode
        pass
