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
    img = ImageTk.PhotoImage(Image.open("./resources/colour-wheel.png").resize((375, 375)))
    img_label = tk.Label(window, image=img)
    img_label.image = img # Prevent python garbage collector from disposing of the image

    img_label.grid(padx=5, pady=5, row=0, column=0, rowspan=4)

    img_label.bind("<Button-1>", update_colour)

    ## Draw custom red, green and blue value boxes and labels
    red_label = tk.Label(window, text="Red: ")
    red_label.grid(padx=0, pady=5, row=0, column=1)
    red_field = tk.Entry(window, textvariable=red_variable, width=5)
    red_variable.set("0")
    red_field.text_var = red_variable # Associate with to allow for getting when updated
    red_field.grid(padx=0, pady=5, row=0, column=2)
    red_field.bind("<KeyRelease>", validate_rgb_val)

    green_label = tk.Label(window, text="Green: ")
    green_label.grid(padx=0, pady=5, row=1, column=1)
    green_field = tk.Entry(window, textvariable=green_variable, width=5)
    green_variable.set("0")
    green_field.text_var = green_variable # Associate with to allow for getting when updated
    green_field.grid(padx=0, pady=5, row=1, column=2)
    green_field.bind("<KeyRelease>", validate_rgb_val)

    blue_label = tk.Label(window, text="Blue: ")
    blue_label.grid(padx=0, pady=5, row=2, column=1)
    blue_field = tk.Entry(window, textvariable=blue_variable, width=5)
    blue_variable.set("0")
    blue_field.text_var = blue_variable # Associate with to allow for getting when updated
    blue_field.grid(padx=0, pady=5, row=2, column=2)
    blue_field.bind("<KeyRelease>", validate_rgb_val)

    ## Draw colour preview box

    preview_label = tk.Label(window, text="Preview: ")
    preview_label.grid(padx=0, pady=5, row=3, column=2)
    preview_box = tk.Label(window, text=" ", width=5, height=1, background=hex_value_here)
    

def validate_rgb_val(event):
    rgb_var = event.widget.text_var
    try:
        number = int(rgb_var.get())
        if number < 0:
            rgb_var.set("0")
        elif number > 255:
            rgb_var.set("255")
    except:
        if rgb_var.get().strip(): # String is not a value and not empty
            rgb_var.set("0")
        else: # String is not a number but probably empty so allow for when a user is replacing the value with a new on
            pass
            

def update_colour(event):
    global red_variable, green_variable, blue_variable
    x = event.x - event.widget.winfo_x()
    y = event.y - event.widget.winfo_y()

    try:
        colour = event.widget.image._PhotoImage__photo.get(x, y)
    except tk.TclError:
        return # Clicked outside of the image
    if colour == (0, 0, 0):
        return # Invalid colour, either clicked square border or inner center but cannot show white light
    
    red_variable.set(colour[0])
    green_variable.set(colour[1])
    blue_variable.set(colour[2])

draw_controller_screen()




window.mainloop()