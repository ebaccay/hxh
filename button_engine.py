import msvcrt
import time
import sys


def key_poll():
    keystroke = msvcrt.kbhit()
    if keystroke:
        return int(str(ord(msvcrt.getch())))
    return 0


def create_key_dictionary():
    key_arr = [96, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 8, 9, 113, 119, 101, 114, 116, 121, 117, 105, 111
               , 112, 91, 93, 92, 97, 115, 100, 102, 103, 104, 106, 107, 108, 59, 39, 13, 122, 120, 99, 118, 98, 110,
               109, 44, 46, 47, 32, 75, 72, 80, 77, 27]
    val_arr = ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=",  "(BACKSPACE)", "(TAB)",  "q", "w", "e",
               "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'",
               "(ENTER)", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/",  "(SPACE)",  "(LEFT)", "(UP)",  "(DOWN)",
               "(RIGHT)", "(ESC)"]
    key_dictionary, i = {}, 0
    for k in key_arr:
        key_dictionary[k] = val_arr[i]
        i += 1
    return key_dictionary


class ButtonEngine:
    refresh_rate = 0
    key_dict = create_key_dictionary()

    def __init__(self, frames_per_second=30):
        self.refresh_rate = 1 / frames_per_second

    def poll(self):
        inputs = []
        start = time.time()

        while time.time() - start < self.refresh_rate:
            press = key_poll()
            if press != 0:
                inputs.append(self.key_dict[press])

        return sorted(inputs)

if __name__ == "__main__":

    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    eprint("Testing ButtonEngine functionality...")
    eprint("\nPress any button to test input.")
    eprint("Press ESC to terminate debug.\n")

    while True:
        buttons = ButtonEngine(30)
        presses = buttons.poll()

        if len(presses) != 0:
            eprint(sorted(presses))

        if "(ESC)" in presses:
            break

    eprint("\nDebug terminated.")
