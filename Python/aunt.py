from tkinter import *
import math

__author__ = 'Mochla'


class Langton(Frame):
    """ :class Langton: Encompasses visual and logical elements of a Langton's Ant simulation. """
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Langton's Ant Simulator")

        # Colors
        self.light_color = "white"
        self.dark_color = "black"
        self.ant_color = "green"

        # Member variables
        self.grid_size = 80
        # This will be full of frames later - fill with 0s to set array size now
        self.label_grid = [[0 for x in range(self.grid_size)] for x in range(self.grid_size)]
        self.label_size = 10  # Screen pixels I think? Maybe whatever the OS's window manager thinks is a pixel
        self.mid_point = math.floor(self.grid_size / 2)  # Ant starts here
        self.step_speed = 500  # milliseconds
        self.fastest_speed = 10  # milliseconds - don't want it to be too fast
        self.slowest_speed = 10000  # milliseconds - don't want it to stop entirely
        self.ant_x = int(self.mid_point)
        self.ant_y = int(self.mid_point)
        # Facing : N E S W
        #          0 1 2 3
        self.ant_facing = 0
        self.do_steps = BooleanVar()  # Keeps track of whether or not the ant should be moving
        self.do_steps.set(0)

        # Frames
        self.parent.grid_frame = Frame(self.parent)
        self.parent.grid_frame.grid(row=1, column=1)
        self.parent.ctrl_frame = Frame(self.parent)
        self.parent.ctrl_frame.grid(row=3, column=1)

        # Grid Frame elements
        # Make the labels that compose the grid
        for i in range(self.grid_size):
            self.parent.grid_frame.grid_rowconfigure(i, weight=1)
            for j in range(self.grid_size):
                self.parent.grid_frame.grid_columnconfigure(j, weight=1)
                w = Frame(self.parent.grid_frame, bg=self.light_color, width=self.label_size, height=self.label_size)
                w.bind("<Button-1>", self.onGridClick)  # If a user clicks on a square - toggle the bg
                w.val = 0  # Invisible value keeping track of what the background color should be
                w.grid(row=i, column=j)
                self.label_grid[i][j] = w
                
        # Initial Placement of "ant"
        self.label_grid[self.ant_x][self.ant_y]["bg"] = self.ant_color

        # Control Frame Grid configuration
        self.parent.ctrl_frame.grid_rowconfigure(0, weight=1)
        for k in range(10):
            self.parent.ctrl_frame.grid_columnconfigure(k, weight=1)

        # Control Frame elements
        self.slower = Button(self.parent.ctrl_frame, text="<< Slower", command=self.slowDown)
        self.slower.grid(row=0, column=4)
        self.start_stop = Button(self.parent.ctrl_frame, text="Start", command=self.startOrStop)
        self.start_stop.grid(row=0, column=5)
        self.faster = Button(self.parent.ctrl_frame, text="Faster >>", command=self.speedUp)
        self.faster.grid(row=0, column=6)
        self.reset = Button(self.parent.ctrl_frame, text="Reset", command=self.resetWindow)
        self.reset.grid(row=0, column=10)

        # Parent frame grid configuration
        self.parent.grid_rowconfigure(0, minsize=20)
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_rowconfigure(2, minsize=20)
        self.parent.grid_rowconfigure(3, weight=1)
        self.parent.grid_rowconfigure(4, minsize=20)
        self.parent.grid_columnconfigure(0, minsize=20)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_columnconfigure(2, minsize=20)

        self.centerWindow()

    # Centers initial window on the screen
    def centerWindow(self):
        """ :brief: Helper function to center the app window on the user's screen. """
        # Get total space for window placement
        sw = self.parent.winfo_screenwidth()   # Get OS's parent window width, generally monitor dimensions
        sh = self.parent.winfo_screenheight()  #                        height
        # Get space taken up by the app
        window_width = self.grid_size * self.label_size + 100
        window_height = self.grid_size * self.label_size + 100

        x = (sw - window_width) / 2
        y = (sh - window_height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

    def startOrStop(self):
        """ :brief: Helper function to handle switching the appearance of the start/stop button according to whether the
            ant is moving or not. """
        if self.do_steps.get():
            self.stopMoving()
        else:
            self.startMoving()

    def onGridClick(self, event):
        """ :brief: Toggle the color and value of a square when a user clicks it. """
        if event.widget.val == 0:
            event.widget["bg"] = self.dark_color
            event.widget.val = 1
        else:
            event.widget["bg"] = self.light_color
            event.widget.val = 0

    def antTurn(self):
        """ :brief: Logic for turning the ant on the grid - if the square has a value of 0, turn right.
            Otherwise, turn left. """
        # Light square -> turn right
        if self.label_grid[self.ant_x][self.ant_y].val == 0:
            self.ant_facing = (self.ant_facing + 1) % 4
        # Dark square -> turn left
        else:
            self.ant_facing = (self.ant_facing - 1) % 4

    def antStep(self):
        """ :brief: Contains the logic for moving the ant along the grid, changing the color of the square it just 
            left and the one it's attempting to step to.
            :return: True if the ant is not going out of bounds, False otherwise. """
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
            # This really shouldn't happen, but error behavior just in case
            print("Facing error... facing = " + str(self.ant_facing))
            self.stopMoving()
            return False

        # If we're going out of bounds, stop the movement
        if going_out_of_bounds:
            # In the future, I would like to add a kind of zoom-out feature when the ant hits the current edge, allowing
            # it to keep going up to a point. But just stop the movement for now.
            print("Out of bounds!")
            # Keep the ant where it was
            self.ant_x = startx
            self.ant_y = starty
            self.stopMoving()
        self.label_grid[self.ant_x][self.ant_y]["bg"] = "green"
        return not going_out_of_bounds  # As long as we aren't going out of bounds, advertise that we're ok

    def resetWindow(self):
        """ :brief: Resets the ant and grid properties to their starting states. """
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
        """ :brief: Loop defining the movement of the ant - executes as long as stopMoving() hasn't been called, and the current
            step was successful. """
        if self.do_steps.get():
            if self.antStep():  # If the ant stepped successfully - turn for the next step and loop again
                self.antTurn()
                self.parent.after(self.step_speed, self.movementLoop)

    def startMoving(self):
        """ :brief: Start the movement of the ant - wherever it may be. """
        self.do_steps.set(1)
        self.start_stop["text"] = "Stop"
        self.movementLoop()

    def stopMoving(self):
        """ :brief: Stop the movement of the ant - wherever it may be. """
        self.do_steps.set(0)
        self.start_stop["text"] = "Start"

    def slowDown(self):
        """ :brief: Slow down the movement of the ant - down to a minimum speed. """
        self.step_speed = int(self.step_speed * 2) if self.step_speed <= self.slowest_speed else self.step_speed

    def speedUp(self):
        """ :brief: Speed up the movement of the ant - up to a maximum speed. """
        self.step_speed = int(self.step_speed / 2) if self.step_speed >= self.fastest_speed else self.step_speed


def main():
    # Get os's root window from Tk
    root = Tk()
    root.resizable(width=False, height=False)
    # Send it to our class
    app = Langton(root)
    root.wm_deiconify()
    # Start the gui process
    root.mainloop()


main()
