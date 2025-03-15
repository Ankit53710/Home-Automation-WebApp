from machine import Pin
import time
import urequests
import network

R1L1=Pin(19,Pin.OUT)
Kled1=Pin(18,Pin.OUT)
R1fan1=Pin(22,Pin.OUT)
Kfan1=Pin(27,Pin.OUT)

Kled1.on()
Kfan1.on()
R1L1.on()
R1fan1.on()
ssid = "ssid"
password = "password"
firebase_url = "firebase_url/Home_Appliances.json"
regulator=False


def connect_to_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print("Connecting to Wi-Fi...")
        station.connect(ssid, password)
        while not station.isconnected():
            pass
    print("Connected to Wi-Fi")
    
def Home_Data():
    try:
        response = urequests.get(firebase_url)
        data = response.json()
        response.close()  
        return data
    except Exception as e:
        print("Error retrieving Gardening Data:", e)
        return None
    

    
def main():
    connect_to_wifi()
    while True:
        #print("data fetched")
        data=Home_Data()
        #print(data)
        print("R1L1 on")
        R1L1.off()
        time.sleep(10)
        print("R1L1 off")
        R1L1.on()
        time.sleep(10)
        
            
main()

