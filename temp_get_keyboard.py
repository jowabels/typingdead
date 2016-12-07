#!/usr/bin/python
#
# This is a terminal-based typing game written in Python. The goal
# is to slaugher thy enemies and drink their blood. Kidding. Type the
# words that fall in the screen before they reach the bottom. Butcher
# enemies afterwards.
#
# This is to showcase synchronization and threading methods.
# Author: joa

import curses


def main(stdscr):
	# do not wait for input when calling getch
	stdscr.nodelay(1)
	while True:
		# get keyboard input, returns -1 if none available
		c = stdscr.getch()
		if c != -1:
			# print numeric value
			stdscr.addstr(str(c) + "-")
			stdscr.refresh()


if __name__ == "__main__":
	curses.wrapper(main)
