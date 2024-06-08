import time
from flask import Flask, render_template, request, jsonify
from flask_mqtt import Mqtt
app = Flask(__name__, template_folder='templates')

# Cấu hình kết nối tới broker
app.config['MQTT_BROKER_URL'] = 'mqtt3.thingspeak.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config["MQTT_TRANSPORT"] = "TCP"
app.config['MQTT_USERNAME'] = 'CAUDCSUbKwMkLC8mJC4tDDU'
app.config['MQTT_CLIENT_ID'] = 'CAUDCSUbKwMkLC8mJC4tDDU'
app.config['MQTT_PASSWORD'] = 'IOdPv1233vqfaZAVyWaJ7BEC'
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_REFRESH_TIME'] = 5.0 # refresh time in seconds
# Khởi tạo đối tượng MQTT
mqtt = Mqtt(app)
mqtt.init_app(app)
channel = 2174698
topic_subscribe = f"channels/{channel}/subscribe/fields/"
topic_publish = f"channels/{channel}/publish/fields/"

""" Storage all values of the fields """
# Sensor
air_temperature, air_humidity, soil_moisture, light_intensity = [23, 23, 44, 44]
# Actuator
fan, water_pump, light = [0, 1, 0]

# Var storage form MQTT Broker
topic_received = ''
data_received = 0

def subscribe_topic(topic):
    return f'{topic_subscribe}field{topic}'

def publish_topic(topic):
    return f'{topic_publish}field{topic}'

def publish_message(topic, data, qos=1):
    results, mid = mqtt.publish(topic, data, qos=qos)
    if results == 0:
        print(f'Message from {topic} with data: {data} published successfully')
    else:
        time.sleep(1)
        return publish_message(topic, data, qos=qos)
    return "OK"

def handle_received_message(topic, data):
    if topic == subscribe_topic(1):
        global air_temperature
        air_temperature = data
    elif topic == subscribe_topic(2):
        global air_humidity
        air_humidity = data
    elif topic == subscribe_topic(3):
        global soil_moisture
        soil_moisture = data
    elif topic == subscribe_topic(4):
        global light_intensity
        light_intensity = data
    elif topic == subscribe_topic(6):
        global fan
        fan = int(data)
    elif topic == subscribe_topic(7):
        global water_pump
        water_pump = int(data)
    elif topic == subscribe_topic(8):
        global light
        light = int(data)
    

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(f'{topic_subscribe}+') # Subscribe all fields

@mqtt.on_message()
def handle_message(client, userdata, message):
    global topic_received, data_received
    topic_received = message.topic
    data_received = float(message.payload.decode('utf-8'))
    print(f'Received message: {data_received} on topic: {topic_received}')
    handle_received_message(topic_received, data_received)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/now')
def values_now():
    temp = {
        'air_temperature': air_temperature,
        'air_humidity': air_humidity,
        'soil_moisture': soil_moisture,
        'light_intensity': light_intensity,
        'fan': fan,
        'water_pump': water_pump,
        'light': light
    }
    return jsonify(temp)

@app.route('/fan', methods=["POST"])
def control_fan():
    global fan
    if not request.is_json:
        return jsonify({'error': 'Payload JSON không hợp lệ'}), 415
    data = request.get_json()
    state = data.get('state')
    fan = int(state) 
    publish_message(publish_topic(6), fan)
    return "OK"

@app.route('/water_pump', methods=["POST"])
def control_water_pump():
    global water_pump
    if not request.is_json:
        return jsonify({'error': 'Payload JSON không hợp lệ'}), 415
    data = request.get_json()
    state = data.get('state') 
    water_pump = int(state) 
    publish_message(publish_topic(7), water_pump)
    return "OK"

@app.route('/light', methods=["POST"])
def control_light():
    global light
    if not request.is_json:
        return jsonify({'error': 'Payload JSON không hợp lệ'}), 415
    data = request.get_json()
    state = data.get('state')
    light = int(state)
    publish_message(publish_topic(8), light)
    return "OK"


###################################################################################

if __name__ == '__main__':
    app.run(host="0.0.0.0" ,port=3001, debug=True)
    print("Offline")

###################################################################################



