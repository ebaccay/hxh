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

    def populate(self, x, y):
        self.population[self.census] = [x, y]
        self.census += 1

    def coordinates(self, i):
        try:
            return self.population[i]
        except KeyError:
            print("No such figure found.")
            return [0, 0]

    def update