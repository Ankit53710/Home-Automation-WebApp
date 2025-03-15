from machine import Pin,ADC,PWM
import time
import urequests
import network
import utime
import dht

# Define pin assignments
Rgas_p = 35
Kgas_p= 34
dht_pin =Pin(13)
dht_sensor = dht.DHT11(dht_pin)
m1=Pin(27,Pin.OUT)
m1.on()


# Initialize peripherals
Rgas = ADC(Pin(Rgas_p))
Kgas = ADC(Pin(Kgas_p))
#pwm = PWM(Pin(servo_pin), freq=50, duty=0)

# Constants and configurations
conversion_factor = 100 / 1023
ssid = "Ankit"
password = "88888862"
firebase_url = "https://dht11-training-default-rtdb.asia-southeast1.firebasedatabase.app/Home_Appliances.json"

def connect_to_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print("Connecting to Wi-Fi...")
        station.connect(ssid, password)
        while not station.isconnected():
            pass
    print("Connected to Wi-Fi")

def read_gas_sensor():
    Rsensor_value = Rgas.read()
    Ksensor_value = Kgas.read()
    RG = Rsensor_value * conversion_factor
    KG= Ksensor_value * conversion_factor
    return RG,KG

def update_status(jdata):
    try:
        print(jdata)
        response = urequests.put(firebase_url, json=jdata)
        if response.status_code == 200:
            print("Status updated successfully!")
        else:
            print(f"Error updating status: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

def move_servo(position):
    try:
        duty = int(((position) / 180 * 2 + 0.5) / 20 * 1023)
        pwm.duty(duty)
        utime.sleep(1)
        print("Servo Angle:", position)
    except Exception as e:
        print(f"Error moving servo: {e}")
    
def read_dht11_data():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temperature, humidity
    except Exception as e:
        print("Error reading DHT11 sensor:", e)
        return None, None

def devices_data():
    try:
        response = urequests.get(firebase_url)
        data = response.json()
        response.close()
        print(data)
        return data
    except Exception as e:
        print(f"Error retrieving Gardening Data: {e}")
        return 

def main():
    connect_to_wifi()
    regulator=False
    while True:
        data = devices_data()
        print(data)
        if not data:
            continue
        RGL,KGL=read_gas_sensor()
        try:
            temperature, humidity = read_dht11_data()
            data['Temperature']=temperature
            data['Humidity']=humidity
        except:
            pass
        data['R_Smoke']=RGL
        data['K_Smoke']=KGL
        update_status(data)
        if KGL>=400:
            m1.off()
        else:
            m1.on()
        time.sleep(3)
        

if __name__ == "__main__":
    main()
