import button_engine as be
import physics_engine as pe


def main():
    print("Choose a debug mode:")
    print("1) ButtonEngine")
    print("2) PhysicsEngine")

    option = ""
    while not isinstance(option, int):
        try:
            option = int(input("> "))
            assert 1 <= option <= 2
        except ValueError:
            print("Please enter a valid value.")
        except AssertionError:
            print("Option not available.")
            option = ""

    if option == 1:
        button_test()
    elif option == 2:
        physics_test()


def button_test():
    import sys

    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    eprint("NOTE: This only works on windows! Mac and Unix functionality to be added soon...\n")
    eprint("Testing ButtonEngine functionality...")
    eprint("\nPress any button to test input.")
    eprint("Press ESC to terminate debug.\n")

    while True:
        buttons = be.ButtonEngine()
        presses = buttons.poll()

        if len(presses) != 0:
            eprint(presses)

        if "(ESC)" in presses:
            break

    eprint("\nButton debug terminated.")


def physics_test():
    import sys
    import matplotlib.pyplot as plt

    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    eprint("Testing PhysicsEngine functionality...")

    test = True

    while test:
        horizontal_velocity = ""
        vertical_velocity = ""

        mag = ""
        thet = ""

        decay = ""

        eprint("Please enter said values to test:")

        eprint("\nHorizontal Velocity?")
        while not isinstance(horizontal_velocity, int):
            try:
                horizontal_velocity = input("> ")
                horizontal_velocity = int(horizontal_velocity)
            except ValueError:
                eprint("Please enter a valid value.")

        eprint("Vertical Velocity?")
        while not isinstance(vertical_velocity, int):
            try:
                vertical_velocity = int(input("> "))
            except ValueError:
                eprint("Please enter a valid value.")

        eprint("Magnitude??")
        while not isinstance(mag, int):
            try:
                mag = input("> ")
                mag = int(mag)
            except ValueError:
                eprint("Please enter a valid value.")

        eprint("Theta?")
        while not isinstance(thet, int):
            try:
                thet = int(input("> "))
            except ValueError:
                eprint("Please enter a valid value.")

        eprint("Decay rate? A value between 0 and 1")
        while not isinstance(decay, float):
            try:
                decay = float(input("> "))
                assert 0 <= decay <= 1
            except ValueError:
                eprint("Please enter a valid value.")
            except AssertionError:
                eprint("Please enter a value between 0 and 1.")
                decay = ""

        physics = pe.PhysicsEngine(left=-50, right=50, top=50, bottom=0, ay=-10, decay=decay)
        physics.populate(vx=horizontal_velocity, vy=vertical_velocity)
        char_two = physics.populate()
        physics.throw(char_two, mag, thet)

        x0 = []
        y0 = []

        x1 = []
        y1 = []

        for i in range(1000):
            x0.append(physics.coordinates(0)[0])
            y0.append(physics.coordinates(0)[1])

            x1.append(physics.coordinates(1)[0])
            y1.append(physics.coordinates(1)[1])

            physics.tick()

        plt.plot(x0, y0, "b^", x1, y1, "r^")
        plt.show()

        eprint("Test again?")

        response = ""
        while response not in ["Y", "y", "N", "n"]:
            response = input("> ")
            eprint(response)

            if response == "N" or response == "n":
                test = False
            elif response == "Y" or response == "y":
                pass
            else:
                eprint("Please enter a valid input.")

    eprint("Physics debug terminated.")

if __name__ == "__main__":
    main()
