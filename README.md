# VEX IQ Enigma machine

A working 3-rotor Enigma cipher machine built with VEX IQ (2nd gen). The Brain does the cipher math, and three motor-driven rotor discs physically turn to show each rotor's position, like the windows on a real Enigma.

It uses the historical Enigma I rotors I, II and III with reflector B. Typing `AAAAA` from A-A-A gives `BDZGO`, the same as a real machine.

## What's here

| Path | What it is |
| --- | --- |
| `src/enigma_vexiq.py` | VEXcode IQ Python program for the Brain |
| `animation/index.html` | Interactive animation of the machine (open in any browser) |
| `tests/test_cipher.py` | Checks the cipher logic on a computer, no robot needed |

## Parts

- 1 Brain + battery
- 3 Smart Motors (ports 1, 2, 3 = left, middle, right rotor)
- 1 Touch LED (port 4)
- 3 large gears (60-tooth works well) or round wheels as rotor discs
- Shafts, beams, plates, pins and standoffs for the frame
- Paper letter rings (A–Z, one letter every 13.85°) taped onto each disc
- 3 small beams or pins as pointers above each disc

## Build

1. **Base:** Lay a long plate (or two joined) as the chassis, about 3 rotors wide.
2. **Rotor towers:** Mount the 3 Smart Motors side by side, standing upright, shafts pointing toward the front. Space them so the discs don't touch.
3. **Rotor discs:** Put a 60T gear on each motor shaft (1:1, no gearing) and tape a letter ring to its face.
4. **Pointers:** Add a short beam above each disc pointing down at the top letter. That letter is the rotor's current position.
5. **Brain:** Mount it in front of the rotors, screen facing you, buttons easy to reach.
6. **Touch LED:** Mount it to one side as the reset and lamp button.
7. **Before running:** Turn every disc by hand so **A** is under its pointer.

## Using it

- **Left / Right** buttons scroll through A–Z.
- **Check** presses the key. The output letter shows on the screen, the Touch LED flashes yellow like the lampboard, and the rotors step.
- **Touch LED** resets all rotors to A-A-A.
- **To decrypt:** reset, then type the encrypted letters. The original message comes back, because Enigma is symmetric.

## How the cipher works

1. The right rotor steps on every keypress. When it passes its notch (V), the middle rotor steps. When the middle rotor reaches its notch (E), it and the left rotor both step (the "double-step").
2. The letter goes through the right, middle and left rotors, bounces off the reflector, and comes back through all three in reverse.
3. Because the rotors move on every key, the same letter typed twice gives different outputs, and no letter ever encrypts to itself.

## Run the tests

```
python3 tests/test_cipher.py
```

## Ideas to extend it

- **Plugboard:** add a letter-swap table applied before and after the rotors.
- **Starting key:** a setup mode where the buttons set each rotor's start letter.
- **Controller input:** use the IQ Controller for faster letter selection.
