import math
import time
from tkinter import *
__author__ = 'Mochla'


class Langton(Frame):
    gridSize = None
    cgrid = None
    # Keeps track of the tkinter labels for color-changing purposes
    tgrid = None
    cx = None
    cy = None
    ent = None
    # N E S W
    # 0 1 2 3
    # Initialize the facing direction to West (left) to start
    facing = 3

    def __init__(self, parent, size):
        # Tkinter parent frame init
        Frame.__init__(self, parent, width=100, height=100, background="gray")
        self.parent = parent
        i = IntVar()
        self.ent = Entry(parent, textvariable=i)
        self.ent.pack(anchor=CENTER, side=BOTTOM)
        b = Button(parent, text="Run", command=self.run)
        b.pack(anchor=CENTER, side=BOTTOM)

        # Child frame init
        self.gridFrame = Frame(parent)
        self.gridFrame.pack(anchor=CENTER, side=TOP)

        # Console output stuff
        self.gridSize = size
        self.cgrid = [[0 for x in range(size)] for x in range(size)]
        self.tgrid = [[0 for x in range(size)] for x in range(size)]
        mid = math.floor(size/2)
        self.cx = mid
        self.cy = mid

        # Tkinter grid make
        for i in range(size):
            for j in range(size):
                w = Label(self.gridFrame, bg="white", width="4", height="2", bd="2")
                w.grid(row=i, column=j)
                self.tgrid[i][j] = w

        # Initial placement of the "ant"
        self.tgrid[self.cx][self.cy]["bg"] = "green"
        self.cgrid[self.cx][self.cy] = 1

        self.centerwindow(size)
        self.initui()

    def turn(self):
        direction = ["North", "East", "South", "West"]
        tmp = self.cgrid[self.cx][self.cy]
        if tmp == 0:
            self.cgrid[self.cx][self.cy] = 1
            self.facing = (self.facing + 1) % 4
        elif tmp == 1:
            self.cgrid[self.cx][self.cy] = 0
            self.facing = (self.facing - 1) % 4
        else:
            print("That's a cgrid error, current grid position = " + str(tmp))
            exit(1)

    def move(self):
        tmp = self.cgrid[self.cx][self.cy]
        if tmp == 0:
            self.tgrid[self.cx][self.cy]["bg"] = "white"
        elif tmp == 1:
            self.tgrid[self.cx][self.cy]["bg"] = "black"

        # N - E - S - W
        if self.facing == 0:
            self.cy -= 1
        elif self.facing == 1:
            self.cx += 1
        elif self.facing == 2:
            self.cy += 1
        elif self.facing == 3:
            self.cx -= 1
        else:
            print("OMG FACING ERROR, facing = " + str(self.facing))
            exit(1)
        self.tgrid[self.cx][self.cy]["bg"] = "green"

    def run(self):
        steps = int(self.ent.get())
        self.step(steps)

    def step(self, steps):
        if steps <= 0:
            return
        else:
            self.move()
            self.turn()
            steps -= 1
            self.parent.after(500, self.step, steps)

    def initui(self):
        self.parent.title("Langton's Ant")

    # Centers initial window on the screen
    def centerwindow(self, size):
        w = 40 * size
        h = 40 * size
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    root = Tk()
    app = Langton(root, 20)
    root.mainloop()

main()
