# TODO: Add decay to vy as well
import math


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

    def throw(self, i, magnitude, theta):
        rad = theta * (math.pi / 180)

        vx = magnitude * math.cos(rad)
        vy = magnitude * math.sin(rad)
        self.update(i, vx=vx, vy=vy)

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
