import math

__author__ = 'Mochla'


class Langton:
    gridSize = None
    grid = None
    currentX = None
    currentY = None
    # N E S W
    # 0 1 2 3
    # Initialize the facing direction to West (left) to start
    facing = 3

    def __init__(self, size):
        self.gridSize = size
        self.grid = [[0 for x in range(size)] for x in range(size)]
        mid = math.floor(size/2)
        self.currentX = mid
        self.currentY = mid

    def turn(self):
        if self.grid[self.currentX][self.currentY] == 0:
            self.grid[self.currentX][self.currentY] = 1
            self.facing = (self.facing + 1) % 4
        else:
            self.grid[self.currentX][self.currentY] = 0
            self.facing = (self.facing + 3) % 4

    def move(self):
        if self.facing == 0:
            self.currentY -= 1
        elif self.facing == 1:
            self.currentX += 1
        elif self.facing == 2:
            self.currentY += 1
        elif self.facing == 3:
            self.currentX -= 1
        else:
            print("OMG FACING ERROR, facing = " + str(self.facing))

    def run(self, steps):
        for i in range(steps):
            for value in self.grid:
                print(value)
            self.move()
            self.turn()
            print("\n")

        for value in self.grid:
            print(value)


def main():
    app = Langton(5)
    app.run(10)

main()
