# TODO: Change manual x, y assignment vectors to be theta, magnitude form instead
# TODO: Add decay to vy as well

class PhysicsEngine:
    population = {}
    census = 0

    def __init__(self, left=-1, right=1, top=1, bottom=-1, ax=0, ay=-0.1, frames_per_second=30, decay=0.99):
        self.min_x = left
        self.max_x = right
        self.min_y = bottom
        self.max_y = top

        self.ax = ax
        self.ay = ay

        self.decay = decay

        self.t = 1 / frames_per_second

    def populate(self, sx=0, sy=0, vx=0, vy=0):
        self.population[self.census] = [sx, sy, vx, vy]
        self.census += 1
        return self.census - 1

    def coordinates(self, i):
        try:
            return self.population[i]
        except KeyError:
            print("No such figure found.")
            return [None, None, None, None]

    def update(self, i, sx=None, sy=None, vx=None, vy=None):
        try:
            current_coords = self.population[i]
        except KeyError:
            print("No such figure found.")
            return

        proposed_coords = [sx, sy, vx, vy]
        new_coords = [proposed_coords[i] if proposed_coords[i] is not None else current_coords[i]
                      for i in range(len(current_coords))]

        self.population[i] = new_coords

    def update_coords(self, coords):
        sy = coords[1]
        vy = coords[3]

        proposed_sy = (vy*self.t + 0.5*self.ay*self.t*self.t) + sy
        new_sy = max(min(proposed_sy, self.max_y), self.min_y)

        if new_sy <= self.min_y:
            new_vy = 0
        else:
            new_vy = vy + self.ay * self.t

        if new_sy > self.min_y:
            sx = coords[0]
            vx = coords[2]

            proposed_sx = (vx*self.t + 0.5*self.ax*self.t*self.t) + sx
            new_sx = max(min(proposed_sx, self.max_x), self.min_x)

            if new_sx <= self.min_x or new_sx >= self.max_x:
                new_vx = -(vx + self.ax * self.t) * self.decay
            else:
                new_vx = (vx + self.ax * self.t) * self.decay

        else:
            new_sx = coords[0]
            new_vx = 0

        return [new_sx, new_sy, new_vx, new_vy]

    def tick(self):
        for key, val in self.population.items():
            self.population[key] = self.update_coords(val)

if __name__ == "__main__":
    import sys
    import matplotlib.pyplot as plt

    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    eprint("Testing PhysicsEngine functionality...")

    test = True

    while test:
        horizontal_velocity = ""
        vertical_velocity = ""
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

        eprint("Decay rate? A value between 0 and 1")
        while not isinstance(decay, float):
            try:
                decay = float(input("> "))
                assert 0 <= decay <= 1
            except ValueError:
                eprint("Please enter a valid value.")
            except AssertionError:
                eprint("Please enter a value between 0 and 1.")

        physics = PhysicsEngine(left=-50, right=50, top=50, bottom=0, ay=-10, decay=decay)
        physics.populate(vx=horizontal_velocity, vy=vertical_velocity)

        x0 = []
        y0 = []

        for i in range(1000):
            x0.append(physics.coordinates(0)[0])
            y0.append(physics.coordinates(0)[1])

            physics.tick()

        plt.plot(x0, y0, "b^")
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
