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
        self.window_width = 1000
        self.window_height = 900
        self.grid_size = 40
        # This will be full of frames later - fill with 0s to fill the arrays now
        self.label_grid = [[0 for x in range(self.grid_size)] for x in range(self.grid_size)]
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
                w.bind("<Button-1>", self.onGridClick)  # If a user clicks on the grid - toggle the frame bg
                w.val = 0  # Put a secret value keeping track of what the background color should be
                w.grid(row=i, column=j)
                self.label_grid[i][j] = w
                
        # Initial Placement of "ant"
        self.label_grid[self.ant_x][self.ant_y]["bg"] = self.ant_color

        # Control Frame elements
        self.slower = Button(self.parent.ctrl_frame, text="<< Slower", command=self.slowDown).pack(anchor=CENTER, side=LEFT)
        self.start_stop = Button(self.parent.ctrl_frame, text="Start", command=self.startOrStop)
        self.start_stop.pack(anchor=CENTER, side=LEFT)
        self.faster = Button(self.parent.ctrl_frame, text="Faster >>", command=self.speedUp).pack(anchor=CENTER, side=LEFT)
        self.reset = Button(self.parent.ctrl_frame, text="Reset", command=self.resetWindow).pack(anchor=CENTER, side=RIGHT)

        self.centerWindow()

    # Centers initial window on the screen
    def centerWindow(self):
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - self.window_width) / 2
        y = (sh - self.window_height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (self.window_width, self.window_height, x, y))

    def startOrStop(self):
        if self.do_steps.get():
            self.stopMoving()
        else:
            self.startMoving()

    def onGridClick(self, event):
        if event.widget.val == 0:
            event.widget["bg"] = self.dark_color
            event.widget.val = 1
        else:
            event.widget["bg"] = self.light_color
            event.widget.val = 0

    def antTurn(self):
        # White square -> turn right
        if self.label_grid[self.ant_x][self.ant_y].val == 0:
            self.ant_facing = (self.ant_facing + 1) % 4
        # Black square -> turn left
        else:
            self.ant_facing = (self.ant_facing - 1) % 4

    def antStep(self):
        startx = self.ant_x
        starty = self.ant_y
        # Set the label to the opposite of what it was
        if self.label_grid[self.ant_x][self.ant_y].val == 0:
            self.label_grid[self.ant_x][self.ant_y]["bg"] = self.dark_color
            self.label_grid[self.ant_x][self.ant_y].val = 1
        else:
            self.label_grid[self.ant_x][self.ant_y]["bg"] = self.light_color
            self.label_grid[self.ant_x][self.ant_y].val = 0
        # Facing : N E S W
        #          0 1 2 3
        # Move the ant forward according to which direction it's facing, setting a flag for going out of bounds
        going_out_of_bounds = False
        if self.ant_facing == 0:
            self.ant_y -= 1
            going_out_of_bounds = self.ant_y < 0
        elif self.ant_facing == 1:
            self.ant_x += 1
            going_out_of_bounds = self.ant_x >= self.grid_size
        elif self.ant_facing == 2:
            self.ant_y += 1
            going_out_of_bounds = self.ant_y >= self.grid_size
        elif self.ant_facing == 3:
            self.ant_x -= 1
            going_out_of_bounds = self.ant_x < 0
        else:
            print("Facing error... facing = " + str(self.ant_facing))
            exit(1)

        # If we're going out of bounds, stop the movement
        if going_out_of_bounds:
            print("Out of bounds!")
            self.label_grid[startx][starty]["bg"] = "green"
            self.stopMoving()
        else:
            self.label_grid[self.ant_x][self.ant_y]["bg"] = "green"

    def resetWindow(self):
        for row in self.label_grid:
            for square in row:
                square.config(bg=self.light_color)
                square.val = 0
        self.mid_point = int(self.grid_size / 2)
        self.ant_x = int(self.mid_point)
        self.ant_y = int(self.mid_point)
        # Initial Placement of "ant"
        self.label_grid[self.ant_x][self.ant_y]["bg"] = self.ant_color
        self.step_speed = 500
        self.stopMoving()

    def movementLoop(self):
        if self.do_steps.get():
            self.antStep()
            self.antTurn()
            self.parent.after(self.step_speed, self.movementLoop)

    # Speed up the movement of the ant - up to a maximum speed
    def startMoving(self):
        self.do_steps.set(1)
        self.start_stop["text"] = "Stop"
        self.movementLoop()

    # Stop the movement of the ant - wherever it may be
    def stopMoving(self):
        self.do_steps.set(0)
        self.start_stop["text"] = "Start"

    # Slow down the movement of the ant - down to a minimum speed
    def slowDown(self):
        self.step_speed = int(self.step_speed * 2) if self.step_speed <= self.slowest_speed else self.step_speed

    # Start the movement of the ant - wherever it may be
    def speedUp(self):
        self.step_speed = int(self.step_speed / 2) if self.step_speed >= self.fastest_speed else self.step_speed


def main():
    # Get os's root window from Tk
    root = Tk()
    # Send it to our class
    app = Langton(root)
    # Start the gui process
    root.mainloop()


main()
