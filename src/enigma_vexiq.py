# VEX IQ Enigma Machine
# VEXcode IQ Python (2nd gen Brain)
#
# Ports:
#   1 = left rotor motor, 2 = middle rotor motor, 3 = right rotor motor
#   4 = Touch LED (tap to reset rotors to A-A-A)
#
# Brain buttons: Left/Right scroll the letter, Check encrypts it.
# Before running, turn every rotor disc by hand so A is under its pointer.

from vex import *

brain = Brain()
rotors_m = [Motor(Ports.PORT1), Motor(Ports.PORT2), Motor(Ports.PORT3)]  # left, middle, right
led = Touchled(Ports.PORT4)

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# Historical Enigma I rotors I, II, III and reflector B
WIRING = ["EKMFLGDQVZNTOWYHXUSPAIBRCJ",
          "AJDKSIRUXBLHWTMCQGZNPYFVOE",
          "BDFHJLCPRTXVZNYEIWGAKMUSQO"]
NOTCH = [ALPHA.index("Q"), ALPHA.index("E"), ALPHA.index("V")]
REFLECTOR = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
DEG_PER_LETTER = 360 / 26

pos = [0, 0, 0]     # current letter of each rotor
turns = [0, 0, 0]   # total steps (so motors always turn forward)
selected = 0
plain = ""
cipher = ""


def move_rotor(i):
    pos[i] = (pos[i] + 1) % 26
    turns[i] += 1
    rotors_m[i].spin_to_position(turns[i] * DEG_PER_LETTER, DEGREES, wait=False)


def step():
    if pos[1] == NOTCH[1]:      # double-step
        move_rotor(0)
        move_rotor(1)
    elif pos[2] == NOTCH[2]:
        move_rotor(1)
    move_rotor(2)


def through(c, i, forward):
    p = pos[i]
    if forward:
        c = ALPHA.index(WIRING[i][(c + p) % 26])
    else:
        c = WIRING[i].index(ALPHA[(c + p) % 26])
    return (c - p) % 26


def encrypt(c):
    step()
    for i in (2, 1, 0):
        c = through(c, i, True)
    c = ALPHA.index(REFLECTOR[c])
    for i in (0, 1, 2):
        c = through(c, i, False)
    return c


def draw():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Rotors: " + ALPHA[pos[0]] + ALPHA[pos[1]] + ALPHA[pos[2]])
    brain.screen.set_cursor(2, 1)
    brain.screen.print("Key: < " + ALPHA[selected] + " >")
    brain.screen.set_cursor(3, 1)
    brain.screen.print("In:  " + plain[-12:])
    brain.screen.set_cursor(4, 1)
    brain.screen.print("Out: " + cipher[-12:])


def wait_release(btn):
    while btn.pressing():
        wait(10, MSEC)


def reset_all():
    global plain, cipher
    for i in range(3):
        pos[i] = 0
        turns[i] = 0
        rotors_m[i].spin_to_position(0, DEGREES, wait=False)
    plain = ""
    cipher = ""


for m in rotors_m:
    m.set_position(0, DEGREES)
    m.set_velocity(60, PERCENT)
led.set_color(Color.BLUE)
draw()

while True:
    if brain.buttonRight.pressing():
        selected = (selected + 1) % 26
        draw()
        wait_release(brain.buttonRight)
    elif brain.buttonLeft.pressing():
        selected = (selected - 1) % 26
        draw()
        wait_release(brain.buttonLeft)
    elif brain.buttonCheck.pressing():
        out = encrypt(selected)
        plain += ALPHA[selected]
        cipher += ALPHA[out]
        led.set_color(Color.YELLOW)   # "lamp" lights up
        draw()
        wait_release(brain.buttonCheck)
        led.set_color(Color.BLUE)
    elif led.pressing():
        reset_all()
        led.set_color(Color.RED)
        draw()
        wait_release(led)
        led.set_color(Color.BLUE)
    wait(20, MSEC)
