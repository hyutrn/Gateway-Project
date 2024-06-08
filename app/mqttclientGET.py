import paho.mqtt.client as mqtt
import pandas as pd

# Cấu hình MQTT
mqtt_broker_url = 'mqtt3.thingspeak.com'
mqtt_broker_port = 1883
mqtt_username = 'DgInByokAyIdNSw1BCAILBE'
mqtt_password = '7gLyEL0+HQSbFHKA3WM1EXNa'

# Khởi tạo và cấu hình client MQTT
mqtt_client = mqtt.Client(client_id='DgInByokAyIdNSw1BCAILBE')
mqtt_client.username_pw_set(mqtt_username, mqtt_password)
mqtt_client.connect(mqtt_broker_url, mqtt_broker_port, keepalive=60)

# Tạo DataFrame để lưu dữ liệu
df = pd.DataFrame(columns=['topic', 'payload'])

# Khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    print(f'Connected to MQTT broker with result code {rc}')
    # Subscribe topic tôi muốn
    mqtt_client.subscribe('channels/2174698/subscribe/fields/+')

# Khi nhận được message
def on_message(client, userdata, msg):
    global df
    payload = msg.payload.decode('utf-8')
    topic = msg.topic
    print(f'Received message: {payload} on topic: {topic}')
    
    # Kiểm tra nếu topic đã tồn tại trong DataFrame
    if topic in df['topic'].values:
        # Ghi đè payload vào dòng có cùng topic
        df.loc[df['topic'] == topic, 'payload'] = payload
    else:
        # Tạo một DataFrame mới và gắn vào df
        new_row = pd.DataFrame({'topic': [topic], 'payload': [payload]})
        df = pd.concat([df, new_row], ignore_index=True)
    
    # Ghi DataFrame vào file CSV
    df.to_csv('data.csv', index=False)

# Thiết lập các hàm callback cho client MQTT
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Lặp vô hạn để duy trì kết nối và lắng nghe message
mqtt_client.loop_forever()

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
    
    return payloads