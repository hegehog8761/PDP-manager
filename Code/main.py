import tkinter as tk
import subprocess, usb.core, warnings, os
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
    img_label.image = img # Prevent python garbage collector from disposing of the image

    img_label.grid(column=0, row=0)

    img_label.bind("<Button-1>", update_colour)

    window.update()

def update_colour(event):
    x = event.x - event.widget.winfo_x()
    y = event.y - event.widget.winfo_y()

    colour = event.widget.image._PhotoImage__photo.get(x, y)
    if colour == (0, 0, 0):
        return # Invalid colour, either clicked square border or inner center but cannot show white light
    print(colour)

draw_controller_screen()




window.mainloop()