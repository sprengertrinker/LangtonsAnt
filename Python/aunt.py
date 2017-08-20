from tkinter import *
import math


__author__ = 'Mochla'


class Langton(Frame):
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Langton's Ant Simulator")

        # Colors n fonts
        self.light_color = "white"
        self.dark_color = "black"
        self.ant_color = "green"
        self.label_font = ("Courier", "4")

        # Member variables
        self.grid_size = 40  # TODO: Make this variable and dependent on where the ant is trying to go?
        # This will be full of labels later - fill with 0s to claim the space now
        self.label_grid = [[0 for x in range(self.grid_size)] for x in range(self.grid_size)]
        # A sort of underlying grid keeping track of what button bgs should be since the original bg gets stomped over
        # each time the ant crawls on it. 0 = light 1 = dark
        self.int_grid = [[0 for x in range(self.grid_size)] for x in range(self.grid_size)]
        self.mid_point = math.floor(self.grid_size / 2)  # Ant starts here
        self.step_speed = 500  # milliseconds
        self.fastest_speed = 10  # milliseconds
        self.slowest_speed = 10000  # milliseconds
        self.label_size = 10  # This is text size...
        self.ant_x = int(self.mid_point)
        self.ant_y = int(self.mid_point)
        # Facing : N E S W
        #          0 1 2 3
        self.ant_facing = 0
        self.do_steps = BooleanVar()
        self.do_steps.set(0)

        # Frames
        self.parent.grid_frame = Frame(self.parent)
        self.parent.grid_frame.pack(anchor=CENTER, side=TOP)
        self.parent.ctrl_frame = Frame(self.parent)
        self.parent.ctrl_frame.pack(anchor=CENTER, side=TOP)

        # Grid Frame elements
        # Make the labels that compose the grid
        for i in range(self.grid_size):
            self.parent.grid_frame.grid_rowconfigure(i, weight=1)
            for j in range(self.grid_size):
                self.parent.grid_frame.grid_columnconfigure(j, weight=1)
                w = Frame(self.parent.grid_frame, bg=self.light_color, width=self.label_size, height=self.label_size)
                w.grid(row=i, column=j)
                self.label_grid[i][j] = w
                
        # Initial Placement of "ant"
        self.label_grid[self.ant_x][self.ant_y]["bg"] = self.ant_color

        # Control Frame elements
        self.slower = Button(self.parent.ctrl_frame, text="<< Slower", command=self.slowDown).pack(anchor=CENTER, side=LEFT)
        self.start = Button(self.parent.ctrl_frame, text="Start", command=self.startMoving).pack(anchor=CENTER, side=LEFT)
        self.stop = Button(self.parent.ctrl_frame, text="Stop", command=self.stopMoving).pack(anchor=CENTER, side=LEFT)
        self.faster = Button(self.parent.ctrl_frame, text="Faster >>", command=self.speedUp).pack(anchor=CENTER, side=LEFT)

        self.centerWindow()

    def antTurn(self):
        # White square -> turn right
        if self.int_grid[self.ant_x][self.ant_y] == 0:
            self.ant_facing = (self.ant_facing + 1) % 4
        # Black square -> turn left
        else:
            self.ant_facing = (self.ant_facing - 1) % 4

    def antStep(self):
        # Set the label to the opposite of what it was
        if self.int_grid[self.ant_x][self.ant_y] == 0:
            self.label_grid[self.ant_x][self.ant_y]["bg"] = self.dark_color
            self.int_grid[self.ant_x][self.ant_y] = 1
        else:
            self.label_grid[self.ant_x][self.ant_y]["bg"] = self.light_color
            self.int_grid[self.ant_x][self.ant_y] = 0
        # Facing : N E S W
        #          0 1 2 3
        # Move the ant forward according to which direction it's facing, setting a flag for going out of bounds
        going_out_of_bounds = False
        if self.ant_facing == 0:
            self.ant_y -= 1
            going_out_of_bounds = self.ant_y < 0
        elif self.ant_facing == 1:
            self.ant_x += 1
            going_out_of_bounds = self.ant_x > self.grid_size
        elif self.ant_facing == 2:
            self.ant_y += 1
            going_out_of_bounds = self.ant_y > self.grid_size
        elif self.ant_facing == 3:
            self.ant_x -= 1
            going_out_of_bounds = self.ant_x < 0
        else:
            print("That's a facing error... facing = " + str(self.ant_facing))
            exit(1)

        # If we're going out of bounds, stop the movement
        if going_out_of_bounds:
            print("Out of bounds!")
            self.stopMoving()
        else:
            self.label_grid[self.ant_x][self.ant_y]["bg"] = "green"

    # Centers initial window on the screen
    def centerWindow(self):
        s = self.label_size * self.grid_size + 100  # Grid size + 100px buffer
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - s) / 2
        y = (sh - s) / 2
        self.parent.geometry('%dx%d+%d+%d' % (s, s, x, y))

    # Slow down the movement of the ant - down to a minimum speed
    def slowDown(self):
        self.step_speed = int(self.step_speed * 2) if self.step_speed <= self.slowest_speed else self.step_speed

    # Speed up the movement of the ant - up to a maximum speed
    def startMoving(self):
        self.do_steps.set(1)
        self.movementLoop()

    def movementLoop(self):
        if self.do_steps.get():
            self.antStep()
            self.antTurn()
            self.parent.after(self.step_speed, self.movementLoop)

    # Stop the movement of the ant - wherever it may be
    def stopMoving(self):
        self.do_steps.set(0)

    # Start the movement of the ant - wherever it may be
    def speedUp(self):
        self.step_speed = int(self.step_speed / 2) if self.step_speed >= self.fastest_speed else self.step_speed


def main():
    root = Tk()
    app = Langton(root)
    root.mainloop()

main()
