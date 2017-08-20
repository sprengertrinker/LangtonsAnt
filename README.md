########################################################################################################################
#                                                    Langton's Ant                                                     #
########################################################################################################################

I got the idea for this project from a video: https://www.youtube.com/watch?v=NWBToaXK5T0
It seemed like a simple and fun idea that I could complete reasonably quickly, and also expand in the future to allow
for more complex and interesting simulations.

Langton's Ant is a Cellular Automaton in the same vein as The Game of Life. The ant moves across its grid
with the following rules:
- When it moves onto a light square, it turns 90 degrees to the right.
- When it moves onto a dark square, it turns 90 degrees to the left.
- It moves forward one unit at a time.
- It flips the color of the square it was on previously as it leaves it.

Notable Characteristics:
- Initially, the ant creates a random-looking pattern without much order.
- After ~10,000 steps, the ant starts building a recurrent "highway" pattern 104 steps long that repeats indefinitely.
- Langton's ant was determined to be Turing complete!


Notes on the app in its current state:
- There is an unresolved bug that the app takes an inordinate amount of time to start up and close. Some patience is
  required.