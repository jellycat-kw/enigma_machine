"""Checks the cipher logic from src/enigma_vexiq.py without a VEX Brain.

Run with: python3 tests/test_cipher.py
"""

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WIRING = ["EKMFLGDQVZNTOWYHXUSPAIBRCJ",
          "AJDKSIRUXBLHWTMCQGZNPYFVOE",
          "BDFHJLCPRTXVZNYEIWGAKMUSQO"]
NOTCH = [ALPHA.index("Q"), ALPHA.index("E"), ALPHA.index("V")]
REFLECTOR = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


class Enigma:
    def __init__(self):
        self.pos = [0, 0, 0]

    def step(self):
        p = self.pos
        if p[1] == NOTCH[1]:
            p[0] = (p[0] + 1) % 26
            p[1] = (p[1] + 1) % 26
        elif p[2] == NOTCH[2]:
            p[1] = (p[1] + 1) % 26
        p[2] = (p[2] + 1) % 26

    def through(self, c, i, forward):
        p = self.pos[i]
        if forward:
            c = ALPHA.index(WIRING[i][(c + p) % 26])
        else:
            c = WIRING[i].index(ALPHA[(c + p) % 26])
        return (c - p) % 26

    def encrypt(self, text):
        out = ""
        for ch in text:
            self.step()
            c = ALPHA.index(ch)
            for i in (2, 1, 0):
                c = self.through(c, i, True)
            c = ALPHA.index(REFLECTOR[c])
            for i in (0, 1, 2):
                c = self.through(c, i, False)
            out += ALPHA[c]
        return out


def test_known_vector():
    assert Enigma().encrypt("AAAAA") == "BDZGO"


def test_round_trip():
    msg = "HELLOVEXIQENIGMAMACHINE" * 20
    assert Enigma().encrypt(Enigma().encrypt(msg)) == msg


def test_no_letter_maps_to_itself():
    msg = ALPHA * 30
    assert all(a != b for a, b in zip(msg, Enigma().encrypt(msg)))


if __name__ == "__main__":
    test_known_vector()
    test_round_trip()
    test_no_letter_maps_to_itself()
    print("HELLO ->", Enigma().encrypt("HELLO"))
    print("All tests passed")
