from pynput import mouse
from pynput import keyboard
from pynput.mouse import Controller

from os import popen
from os.path import dirname
from os.path import isfile

from re import findall as regex_findall
from time import sleep as sleep

script_path = dirname(__file__)
config_path = script_path + "/keybind.cfg"

config_file = isfile(config_path)

if not config_file:

    print("config file, keybind.cfg not found!")
    print("using default keybind: <ctrl>+<shift>+o")

keybind_key = config_file and open(config_path).read() or "<ctrl>+<shift>+o"

window_info = {

    "X" : 0,
    "Y" : 0,
    "WIDTH" : 0,
    "HEIGHT" : 0,

}

look_for = [

    "X","Y","WIDTH","HEIGHT"

]

error_offset = 100
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

   if x <= window_info["X"]:
        mouse_object.position = (window_info["WIDTH"] - error_offset,y)
        return

   if x >= window_info["WIDTH"]:
        mouse_object.position = (window_info["X"] + error_offset,y)
        return

   if y >= window_info["HEIGHT"]:
        mouse_object.position = (x,window_info["HEIGHT"] - error_offset)
        return

   if y <= window_info["Y"]:
        mouse_object.position = (x,window_info["Y"] + error_offset)
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
print("Keybind to pause is: ",keybind_key)

hotkey_event_listener = keyboard.GlobalHotKeys({
    keybind_key : on_keybind
})

hotkey_event_listener.start()

with mouse.Listener(on_click=on_click,on_move=on_move) as event:
    event.join()
