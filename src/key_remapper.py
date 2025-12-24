import asyncio, evdev
from evdev import InputDevice, ecodes, UInput

async def intercept(device, altPressed, ui):
    device.grab()
    try:
        async for event in device.async_read_loop():
            targetCode = event.code
            if event.type == ecodes.EV_KEY:
                if event.code == ecodes.KEY_LEFTALT and event.value == 1:
                    altPressed = True
                    continue

                if event.code == ecodes.KEY_LEFTALT and event.value == 0:
                    altPressed = False
                    continue

                # Left Alt + J -> Arrow key down
                if altPressed and event.code == ecodes.KEY_J: #and event.value == 1:
                    targetCode = ecodes.KEY_DOWN

                ## Left Alt + K -> Arrow key up
                if altPressed and event.code == ecodes.KEY_K: #and event.value == 1:
                    targetCode = ecodes.KEY_UP

                ## Left Alt + H -> Arrow key left
                if altPressed and event.code == ecodes.KEY_H: #and event.value == 1:
                    targetCode = ecodes.KEY_LEFT

                ## Left Alt + L -> Arrow key right
                if altPressed and event.code == ecodes.KEY_L: #and event.value == 1:
                    targetCode = ecodes.KEY_RIGHT

                ui.write(event.type, targetCode, event.value);
                ui.syn()
    finally:
        device.ungrab()

async def main():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    keyboards = [InputDevice(device.path) for device in devices if device.name.lower().find("keyboard") > -1]

    # Create tasks for both devices
    # gather() runs them concurrently and waits for them
    altPressed = False
    ui = UInput()
    await asyncio.gather(*[intercept(device, altPressed, ui) for device in keyboards])

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping...")

