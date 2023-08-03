from pynput import mouse
from pynput import keyboard
from pynput.mouse import Controller

from os import popen
from os.path import dirname
from os.path import isfile

from re import findall as regex_findall
from time import sleep as sleep 

window_info = {

    "X" : 0,
    "Y" : 0,
    "WIDTH" : 0,
    "HEIGHT" : 0,

}

look_for = ["X","Y","WIDTH","HEIGHT"]

settings = {
    "keybind" : "<ctrl>+<shift>+o",
    "edge-offset" : 20
}

script_path = dirname(__file__)
config_path = script_path + "/settings.cfg"

config_file = isfile(config_path)

if not config_file:

    print("config file, settings.cfg not found!")
    print("using default settings:")

    for key in settings.keys():
        print(key,settings[key])

else:

    with open(config_path) as config_file_object:

        for line in config_file_object.readlines():
            
            prarms = line.split("=")

            prarms[0] = prarms[0].strip()
            prarms[1] = prarms[1].strip()

  
            if not prarms[0] in settings:
                continue

            try:
                settings[prarms[0]] = int(prarms[1])
            except:
                settings[prarms[0]] = prarms[1]



last_x_y = (0,0)
pause = False
mouse_object = Controller()

print("Be prepared to focus and click your cursor at the Roblox window, press any key when you're ready")
input()
print("Sleeping for 3 seconds")

sleep(3)

output = popen("xdotool getwindowfocus getwindowgeometry --shell") 

for lines in output.readlines():

    for target in look_for:
        if not lines.find(target) == -1:
          
          window_info[target] = int(regex_findall("\d+",lines)[0])


def on_move(x,y):
   
   """
   
        Function to fix mouse going out of window
        Works in 1st person, 3rd person
   
   """

   if pause: 
       return
   
   error_offset = settings["edge-offset"]

   error_offset_safe = error_offset + 10

   if x <= window_info["X"] + error_offset:
        mouse_object.position = ( window_info["X"] + window_info["WIDTH"] - error_offset_safe,y)
        return
   

   if x >= (window_info["X"] + window_info["WIDTH"]) - error_offset :
        mouse_object.position = (window_info["X"] + error_offset_safe,y)
        return

   if y >= window_info["HEIGHT"] - error_offset:
        mouse_object.position = (x,window_info["HEIGHT"] - error_offset_safe)
        return

   if y <= window_info["Y"] + error_offset:
        mouse_object.position = (x,window_info["Y"] + error_offset_safe)
        return

def on_click(x,y,button,pressed):

   
   """ 
        Roblox right click simulation 

   """

   if pause:
       return
   
   global last_x_y

   if not button == mouse.Button.right:
        return
 
   if pressed:
        last_x_y = (x,y)

   if not pressed:
        sleep(0.5)
        mouse_object.position = last_x_y
        

def on_keybind():

    """
    
        Keykind to pause the program
    
    """

    global pause
    
    pause = not pause

    print(pause and "Paused" or "Resumed")

print("Exit by pressing CTRL+C")
print("Keybind to pause is: ",settings["keybind"])

hotkey_event_listener = keyboard.GlobalHotKeys({
    settings["keybind"] : on_keybind
})

hotkey_event_listener.start()

with mouse.Listener(on_click=on_click,on_move=on_move) as event:
    event.join()
