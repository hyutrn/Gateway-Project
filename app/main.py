import time
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_mqtt import Mqtt
app = Flask(__name__, template_folder='templates')

df = pd.DataFrame(columns=['topic', 'payload'])

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
        time.sleep(1.5)
        return publish_message(topic, data, qos=qos)
    return "OK"

def get_payload_from_csv(topics):
    # Đường dẫn đến file CSV
    file_path = 'data.csv'
    
    # Đọc file CSV vào DataFrame
    df = pd.read_csv(file_path)
    
    payloads = []
    
    for topic in topics:
        # Tìm dòng có topic khớp với topic được chọn
        row = df[df['topic'] == topic]
        
        # Kiểm tra nếu không tìm thấy dòng tương ứng với topic
        if row.empty:
            payloads.append(None)
        else:
            # Lấy giá trị payload từ dòng tìm thấy
            payload = row['payload'].iloc[0]
            payloads.append(payload)
    # print(payloads)
    return payloads


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/now')
def values_now():
    global air_temperature, air_humidity, soil_moisture, light_intensity, fan, water_pump, light
    air_temperature, air_humidity, soil_moisture, light_intensity, fan, water_pump, light = get_payload_from_csv([
        subscribe_topic(1),
        subscribe_topic(2), 
        subscribe_topic(3), 
        subscribe_topic(4), 
        subscribe_topic(6), 
        subscribe_topic(7),
        subscribe_topic(8) 
    ])
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



