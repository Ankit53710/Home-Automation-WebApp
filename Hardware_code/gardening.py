from machine import Pin
import time
import urequests
import network

motor_p=Pin(13,Pin.OUT)
motor_p.on()
ssid = "SSID"
password = "password"

firebase_url = "firebase_rtdb_url/Gardening.json"

def connect_to_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print("Connecting to Wi-Fi...")
        station.connect(ssid, password)
        while not station.isconnected():
            pass
    print("Connected to Wi-Fi")

def Gardening_Data():
    try:
        response = urequests.get(firebase_url)
        data = response.json()
        response.close()  
        return data
    except Exception as e:
        print("Error retrieving Gardening Data:", e)
        return None

def update_motor_status(data):
    try:
        
        json_data = urequests.json.dumps(data)
        response = urequests.put(firebase_url, data=json_data)
        if response.status_code == 200:
          print("Motor status updated successfully!")
        else:
            print(f"Error updating status: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def current_time():
    current_time = time.localtime()  
    hour = current_time[3]
    minute = current_time[4]
    return hour,minute

def ftime(time_string):
    try:
        hours, minutes = map(int, time_string.split(":"))
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            return time.time(hours, minutes, 0)  
        else:
            return False
    except ValueError:
        return False


# Main loop
def main():
    connect_to_wifi()
    while True:
        data=Gardening_Data()
        if not data:
            continue
        run_time,duration,Motor_status=data['run_time'].split(":"),int(data['Duration']),data['Motor_status']
        hour,minute=current_time()
        print("current time",hour,minute)
        rhour,rminute=int(run_time[0]),int(run_time[1])
        print("run_time",rhour,rminute)
        if (rhour==hour and rminute==minute):
            motor_p.off()
            #update_motor_status(True)
            time.sleep(duration*60)
            #update_motor_status(False)
            motor_p.on()
        while data['Motor_status']:
            motor_p.off()
            print("by status on")
            data=Gardening_Data()
        else:
          motor_p.on()
          print('off')
            
        
        
        

if __name__ =="__main__":
    main()
