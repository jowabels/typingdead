from curses import *
import random, time
from falling_words import Word

def main(stdscr):
  myWord = Word()
  #TODO put the animator in a separate class and method
  start_color()
  stdscr.clear() # clear above line
  stdscr.addstr(1, 3, "Rain Text", A_BOLD)
  init_pair(10, COLOR_WHITE, COLOR_WHITE)
  init_pair(1, COLOR_RED, COLOR_WHITE)
  init_pair(2, COLOR_BLUE, COLOR_WHITE)
  init_pair(3, COLOR_YELLOW, COLOR_WHITE)
  init_pair(4, COLOR_MAGENTA, COLOR_WHITE)
  init_pair(5, COLOR_CYAN, COLOR_WHITE)
  # first draw a white square as a "background"
  bg = " " # background is blank
  for x in range(3, 3+75): # horizontal c: x-axis
    for y in range(4, 4+20): # vertical r: y-axis
      stdscr.addstr(y, x, bg, color_pair(10))
  stdscr.refresh() # refresh screen to reflect changes
  stdscr.addstr(28, 0, "Press Key to exit")
  # Raining
  while True: # runs forever
    drop = random.choice(myWord.getListOfWords())
    xl = random.sample(range(3, 3+75), 25) # generate 25 random positions
    for y in range(5, 4+20): # vertical
      for x in xl:
        stdscr.addstr(y-1, x, bg, color_pair(10)) # clear drops at previous row
        stdscr.addstr(y, x, drop, color_pair(random.randint(1,5)))
      stdscr.refresh() # refresh each time, # ^^ add drops at next row
      time.sleep(0.5)
    for x in xl: # clear last row, make blank
      stdscr.addstr(23, x, " ", color_pair(10))
  stdscr.getkey()

if __name__ == "__main__":
  wrapper(main)