import vgamepad as vg
from pyfirmata import Arduino , util
import serial.tools.list_ports




def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def convertToTrigger(value):
    return translate(value,0.0,1.0,0,255)


def convertToJoystick(value):
    return translate(value,0.0,1.0,-32768,32767)

ports = list(serial.tools.list_ports.comports())

Arduino_ports = []

for p in ports:
    if 'Arduino' in p.description:
        Arduino_ports.append(p)
if len(Arduino_ports) == 0:
    print("no Arduino board detected")

if len(Arduino_ports) > 1:
    print('Multiple Arduinos found - using the first')
else:
    print("Arduino board detected")

gamepad = vg.VX360Gamepad()
print(Arduino_ports[0].device)

board = Arduino(str(Arduino_ports[0].device))

it = util.Iterator(board)
it.start()

analogue1 = board.get_pin("a:0:i")
analogue2 = board.get_pin("a:1:i")
analogue3 = board.get_pin("a:2:i")


while True:
    gamepad.left_trigger(convertToTrigger(analogue1.read()))
    gamepad.right_trigger(convertToTrigger(analogue2.read()))
    gamepad.left_joystick(convertToJoystick(analogue3.read()))
    gamepad.update()
