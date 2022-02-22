from time import time
import vgamepad as vg
from pyfirmata import Arduino , util
import serial.tools.list_ports
from time import sleep
import random



def NumMapper(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def convertToTrigger(value):
    return int(NumMapper(value,0,1,0,255))


def convertToJoystick(value):
    return int(NumMapper(value,0,1,-32768,32767))






ports = list(serial.tools.list_ports.comports())

Arduino_ports = []

for p in ports:
    if 'Arduino' in p.description:
        Arduino_ports.append(p)
if len(Arduino_ports) == 0:
    print("no Arduino board detected")
    sleep(2)
    exit()

if len(Arduino_ports) > 1:
    print('Multiple Arduinos found - using the first')
else:
    print("Arduino board detected")

gamepad = vg.VX360Gamepad()
print("Xbox Controller initialized")

print(Arduino_ports[0].device)

board = Arduino(str(Arduino_ports[0].device))

it = util.Iterator(board)
it.start()
# getting all pin to use as inputs
LEFT_TRIIGER = board.get_pin("a:0:i")
RIGHT_TRIGGER = board.get_pin("a:1:i")
LEFT_STICK_X = board.get_pin("a:2:i")
LEFT_STICK_Y = board.get_pin("a:3:i")
RIGHT_STICK_X = board.get_pin("a:4:i")
RIGHT_STICK_Y = board.get_pin("a:5:i")

D_PAD_LEFT = board.get_pin("d:13:i")
D_PAD_RIGHT = board.get_pin("d:12:i")
D_PAD_UP = board.get_pin("d:11:i")
D_PAD_DOWN = board.get_pin("d:10:i")

S_KEY_A = board.get_pin("d:9:i")
S_KEY_B = board.get_pin("d:8:i")
S_KEY_X = board.get_pin("d:7:i")
S_KEY_Y = board.get_pin("d:6:i")

SHOLDER_LEFT = board.get_pin("d:5:i")
SHOLDER_RIGHT = board.get_pin("d:4:i")

LEFT_STICK_KEY = board.get_pin("d:3:i")
RIGHT_STICK_KEY = board.get_pin("d:2:i")

START_KEY = board.get_pin("d:1:i")
BACK_KEY = board.get_pin("d:0:i")

board.iterate()

def updateTriggers():
    gamepad.left_trigger(convertToTrigger(LEFT_TRIIGER.read()))
    gamepad.right_trigger(convertToTrigger(RIGHT_TRIGGER.read()))
    gamepad.update()


def updateJoySticks():
    gamepad.left_joystick(convertToJoystick(LEFT_STICK_X.read()),convertToJoystick(LEFT_STICK_Y.read()))
    gamepad.right_joystick(convertToJoystick(RIGHT_STICK_X.read()),convertToJoystick(RIGHT_STICK_Y.read()))
    gamepad.update()

def updateNavigationKey():
    if START_KEY.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        gamepad.update()
    if START_KEY.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        gamepad.update()

    if BACK_KEY.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        gamepad.update()
    if BACK_KEY.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        gamepad.update()



def updateJoyStickKey():
    if LEFT_STICK_KEY.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
        gamepad.update()
    if LEFT_STICK_KEY.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
        gamepad.update()

    if RIGHT_STICK_KEY.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
        gamepad.update()
    if RIGHT_STICK_KEY.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
        gamepad.update()


def updateSholder():
    if SHOLDER_LEFT.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        gamepad.update()
    if SHOLDER_LEFT.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        gamepad.update()

    if SHOLDER_RIGHT.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        gamepad.update()
    if SHOLDER_RIGHT.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        gamepad.update()


def updateDpad():
    if D_PAD_LEFT.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        gamepad.update()
    if D_PAD_LEFT.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        gamepad.update()

    if D_PAD_RIGHT.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        gamepad.update()
    if D_PAD_RIGHT.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        gamepad.update()

    if D_PAD_UP.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        gamepad.update()
    if D_PAD_UP.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        gamepad.update()

    if D_PAD_DOWN.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        gamepad.update()
    if D_PAD_DOWN.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        gamepad.update()


def updateSKey():
    if S_KEY_A.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        gamepad.update()
    if S_KEY_A.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        gamepad.update()

    if S_KEY_B.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()
    if S_KEY_B.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()

    if S_KEY_X.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        gamepad.update()
    if S_KEY_X.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        gamepad.update()

    if S_KEY_Y.read() == 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        gamepad.update()
    if S_KEY_Y.read() == 0:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        gamepad.update()



while True:
    try:
        updateTriggers()
        updateJoySticks()
        updateSholder()
        updateDpad()
        updateSKey()
        updateJoyStickKey()
        updateNavigationKey
    except KeyboardInterrupt:
        board.exit()
        exit()