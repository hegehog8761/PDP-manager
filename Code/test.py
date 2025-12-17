import usb.core
import usb.util
import time

VID = 0x0e6f
PID = 0x02b8

dev = usb.core.find(idVendor=VID, idProduct=PID)
if dev is None:
    raise ValueError("Device not found")

dev.set_configuration()

print("Sending control-transfer probes...")

# Common vendor-specific request patterns
requests = [
    (0x40, 0x01, 0x0000, 0x0000),
    (0x40, 0x01, 0x0001, 0x0000),
    (0x40, 0x09, 0x0200, 0x0000),  # HID-like SET_REPORT
    (0x40, 0x09, 0x0300, 0x0000),
]

payloads = [
    bytes([0xFF, 0x00, 0x00]),  # red
    bytes([0x00, 0xFF, 0x00]),  # green
    bytes([0x00, 0x00, 0xFF]),  # blue
]

try:
    for req in requests:
        for p in payloads:
            print(f"bmRequestType={hex(req[0])} bRequest={hex(req[1])} payload={p.hex()}")
            try:
                dev.ctrl_transfer(
                    bmRequestType=req[0],
                    bRequest=req[1],
                    wValue=req[2],
                    wIndex=req[3],
                    data_or_wLength=p,
                    timeout=1000
                )
            except usb.core.USBError as e:
                print("  ignored:", e)
            time.sleep(1)
except KeyboardInterrupt:
    pass
