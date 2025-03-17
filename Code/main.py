import tkinter as tk
import subprocess, usb.core, warnings
from PIL import ImageTk, Image


### Set up tkinter window
window = tk.Tk()
window.title("PDP manager")

###   Set up controller selection menu

controllers = []

def get_controllers():
    global controllers
    devices = usb.core.find(find_all=True)
    for device in devices:
        try:
            manufacturer = device.manufacturer

            warnings.warn("Currently checking for incorrect manufacturer, ensure to change manufacturer name upon release.")
            if manufacturer == "Sunplus IT Co ":
                print("Found usb")
                controllers.append(device)
            
        except ValueError:
            print("This script must be ran with sudo. Exiting...")
            exit()

get_controllers()

### Draw controller selection menu


### Draw controller management page

def draw_controller_screen():
    img = ImageTk.PhotoImage(Image.open("./resources/colour-wheel.png"))
    img_label = tk.Label(window, image=img)
   
    
    
    button = tk.Button(window, text="Hello World!")
    button.pack(padx=10, pady=5)

    img_label.pack(side = "bottom", fill = "both", expand = "yes")

draw_controller_screen()



tk.mainloop()