import tkinter as tk
import subprocess, usb.core, warnings, os, codes
from PIL import ImageTk, Image


### Set up tkinter window
window = tk.Tk()
window.title("PDP manager")

red_variable = tk.StringVar()
green_variable = tk.StringVar()
blue_variable = tk.StringVar()
brightness_variable = tk.IntVar()
preview_box = None
device_port = None


###   Set up controller selection menu

controllers = []

def get_controllers():
    global controllers
    devices = usb.core.find(find_all=True)
    for device in devices:
        try:
            manufacturer = device.manufacturer
            if manufacturer == "Performance Designed Products":
                controllers.append(device)
            
        except ValueError:
            print("This script must be ran with sudo. Exiting...")
            exit()

get_controllers()

### Draw controller selection menu

def draw_selection_menu():
    title = tk.Label(window, text="Select Controller.", font=("Carrier", 20))
    title.grid(row=0, column=0, columnspan=3)
    rw = 1
    col = 0
    for controller in controllers:
        name = controller.product
        port = controller.port_number
        button = tk.Button(window, text=name, command=lambda p=port: select_device(p))
        button.grid(row=rw, column=col)
        col+=1
        if col == 3:
            col = 0
            rw+=1

    custom_port = tk.Button(window, text="Other device", command=custom_device_port)
    custom_port.grid(row=rw+1, column=0)

def select_device(id):
    global device_port, window, old_window
    device_port = id
    window.withdraw()
    old_window = window
    window = tk.Toplevel(window)
    draw_controller_screen()

def custom_device_port():
    print("Custom port")


### Draw controller management page

def draw_controller_screen():
    global red_variable, green_variable, blue_variable, preview_box, brightness_variable
    ## Draw colour wheel
    img = ImageTk.PhotoImage(Image.open(f"{os.path.dirname(os.path.realpath(__file__))}/resources/colour-wheel.png").resize((375, 375)))
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
    preview_label.grid(padx=0, pady=5, row=3, column=1)
    preview_box = tk.Label(window, text=" ", width=5, height=1, background=rgb_to_hex(int(red_variable.get()), int(green_variable.get()), int(blue_variable.get())), borderwidth=2, relief="groove")
    preview_box.grid(padx=0, pady=5, row=3, column=2)


    ## Draw brightness slider
    brightness_label = tk.Label(window, text="Brightness:")
    brightness_label.grid(padx=15, pady=5, row=0, column=3)
    brightness_slider = tk.Scale(window, from_=100,  length=350, to=0, orient=tk.VERTICAL, variable=brightness_variable)
    brightness_slider.grid(padx=0, pady=15, row=1, column=3, rowspan=3)

    # Draw update controller button
    update_button = tk.Button(window, text="Update", command=update_controller_values)
    update_button.grid(row=5)

    

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
    update_preview_colour()
            
def rgb_to_hex(red, green, blue):
    return "#" + ('{:02X}' * 3).format(red, green, blue)

def update_colour(event):
    global red_variable, green_variable, blue_variable
    x = event.x - event.widget.winfo_x()
    y = event.y - event.widget.winfo_y()

    try:
        colour = event.widget.image._PhotoImage__photo.get(x, y)
    except tk.TclError:
        return # Clicked outside of the image
    if colour == (0, 0, 0):
        return # Counted as invalid colour, hopefully user just types it in rather than trying to click it on the wheel as that won't work
    
    red_variable.set(colour[0])
    green_variable.set(colour[1])
    blue_variable.set(colour[2])
    update_preview_colour()


def update_preview_colour():
    global preview_box
    if any(variable.get() == '' for variable in [red_variable, green_variable, blue_variable]):
        return # User is busy typing new colour code so don't update
    preview_box.config(background=rgb_to_hex(int(red_variable.get()), int(green_variable.get()), int(blue_variable.get())))


def update_controller_values():
    print(f"Update controller to RGB({red_variable.get()}, {green_variable.get()}, {blue_variable.get()}), brightness {brightness_variable.get()}%")
    device = usb.core.find(custom_match = lambda d: d.port_number == device_port)
    print(f"Communincating with {device.product}")
    endpoint = device[0][(0, 0)][0]
    # rdevice.detach_kernel_driver(device[0][(0, 0)].bInterfaceNumber)
    endpoint.write(codes.mode.off)


def close_down():
    global old_window, window
    old_window.destroy()
    window.destroy()
    exit()
    print("after exit")



### Draw first screen to display last thing to make sure everything is defined
draw_selection_menu()

window.protocol("WM_DELETE_WINDOW", close_down)

window.mainloop()