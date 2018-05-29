# TODO: Remove x acceleration since acceleration horizontally is constant
# TODO: Remove y acceleration since vertical acceleration is just gravity
# TODO: Don't update if character is at ground position (min_y)


class PhysicsEngine:
    population = {}
    census = 0
    min_x = -100
    max_x = 100
    min_y = 0
    max_y = 200

    def __init__(self, left, right, top, bottom):
        self.min_x = left
        self.max_x = right
        self.min_y = bottom
        self.max_y = top

    def populate(self, sx=0, sy=0, vx=0, vy=0, ax=0, ay=0):
        self.population[self.census] = [sx, sy, vx, vy, ax, ay]
        self.census += 1

    def coordinates(self, i):
        try:
            return self.population[i]
        except KeyError:
            print("No such figure found.")
            return [None, None, None, None, None, None]

    def update(self, i, sx=None, sy=None, vx=None, vy=None, ax=None, ay=None):
        try:
            current_coords = self.population[i]
        except KeyError:
            print("No such figure found.")
            return

        proposed_coords = [sx, sy, vx, vy, ax, ay]
        new_coords = [proposed_coords[i] if proposed_coords[i] is not None else current_coords[i]
                      for i in range(len(current_coords))]

        self.population[i] = new_coords

    def update_coords(self, coords):
        sx = coords[0]
        vx = coords[2]
        ax = coords[4]

        new_sx = min(max((vx + 0.5 * ax) + sx, self.min_x), self.max_x)

        if sx <= self.min_x or sx >= self.max_x:
            new_vx = -(vx + ax)
        else:
            new_vx = vx + ax

        sy = coords[1]
        vy = coords[3]
        ay = coords[5]

        new_sy = min(max((vy + 0.5 * ay) + sy, self.min_y), self.max_y)

        if sy <= self.min_y or sy >= self.max_y:
            new_vy = -(vy + ay)
        else:
            new_vy = vy + ay

        return [new_sx, new_vx, ax, new_sy, new_vy, ay]

    def tick(self):
        for key, val in self.population.items():
            self.population[key] = self.update_coords(val)
