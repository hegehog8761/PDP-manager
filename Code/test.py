import usb.core
import usb.util
import time
import libusb_package

VID = 0x0e6f
PID = 0x02b8

dev = libusb_package.find(idVendor=VID, idProduct=PID)
if dev is None:
    raise ValueError("Device not found")

#dev.set_configuration()

dev.detach_kernel_driver(dev[0][(0, 0)].bInterfaceNumber)

data = bytes([0x21, 0x00, 0x0e, 0x07, 0xa0, 0x00, 0x00, 0x00, 0xff, 0x64, 0x03])

dev.write(0x01, data)
