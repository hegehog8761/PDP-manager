import tkinter as tk
import subprocess, usb.core, warnings, os
from PIL import ImageTk, Image


### Set up tkinter window
window = tk.Tk()
window.title("PDP manager")

red_variable = tk.StringVar()
green_variable = tk.StringVar()
blue_variable = tk.StringVar()


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
    global red_variable, green_variable, blue_variable
    ## Draw colour wheel
    img = ImageTk.PhotoImage(Image.open("./resources/colour-wheel.png"))
    img_label = tk.Label(window, image=img)
    img_label.image = img # Prevent python garbage collector from disposing of the image

    img_label.grid(column=0, row=0)

    img_label.bind("<Button-1>", update_colour)

    ## Draw custom red, green and blue value boxes and labels
    red_label = tk.Label(window, text="Red: ")
    red_field = tk.Entry(window, textvariable=red_variable)
    red_variable.set("0")
    red_field.text_var = red_variable # Associate with to allow for getting when updated
    red_field.grid(row=1, column=0)
    red_field.bind("<KeyRelease>", validate_rgb_val)

def validate_rgb_val(event):
    rgb_val = event.widget.text_var.get()
    try:
        number = int(rgb_val)
    except:
        if rgb_val.strip()

def update_colour(event):
    x = event.x - event.widget.winfo_x()
    y = event.y - event.widget.winfo_y()

    try:
        colour = event.widget.image._PhotoImage__photo.get(x, y)
    except tk.TclError:
        return # Clicked outside of the image
    if colour == (0, 0, 0):
        return # Invalid colour, either clicked square border or inner center but cannot show white light
    print(colour)

draw_controller_screen()




window.mainloop()