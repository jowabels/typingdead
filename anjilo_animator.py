#!/usr/bin/python

from curses import *
import random, time

class wordobj(object):
	def __init__(self, x, y, word):
		self.posx = x
		self.posy = y
		self.word = word

class WordGenerator(object):
	def __init__(self, ngram):
		self.worddiff = int(ngram)
		self.dict = []
		self.filtered = []
		
	def getdictionary(self):
		textFile = open("words.txt")
		for word in textFile:
			word = word.strip()
			self.dict.append(word)
		textFile.close()
	
	def filterwords(self):
		for word in self.dict:
			x = len(word)
			if len(word) > self.worddiff:
				self.filtered.append(word)

	def releaseword(self):
		self.nextword = random.choice(self.filtered)
		self.filtered.remove(self.nextword)
	
class screen(object):
	def __init__(self, wpm, difficulty):
		self.gendiff = float(wpm)
		self.speeddiff = float(difficulty)
		self.screenwords = []
		self.bg = " "

	def initializescreen(self, stdscr):
		curs_set(0)
		noecho()
		
		start_color()
		init_pair(1, COLOR_WHITE, COLOR_WHITE)
		init_pair(2, COLOR_BLUE, COLOR_WHITE)
		self.contentcolor = color_pair(2)
		self.clearcolor = color_pair(1)

		stdscr.clear() # clear above line
		scrlength = stdscr.getmaxyx()
		self.height = scrlength[0]
		self.width = scrlength[1]

		for x in range(3, self.width-3): 					# horizontal c: x-axis
			for y in range(3, self.height-3): 				# vertical r: y-axis
				stdscr.addstr(y, x, self.bg, color_pair(1))

	def animatescreen(self, word, stdscr):
		s.initializescreen(stdscr)
		scrlength = stdscr.getmaxyx()

		self.screenwords.append(word)
		wordpos = random.choice(range(3, self.width-2))
		word = wordobj(wordpos, 4, word)

		for j in range(4, self.height-2):

				if j == self.height-3:
					stdscr.addstr(j, word.posx, self.bg)
				else:
					stdscr.addstr(j, word.posx, word.word, self.contentcolor)

				for i in range(word.posx, word.posx + len(word.word)):
					stdscr.addstr(j-1, i, self.bg, self.clearcolor)

				stdscr.refresh()
				time.sleep(1/self.speeddiff)

n = raw_input("Please enter word length threshold:")
r = raw_input("Please enter word generation difficulty:")
sp = raw_input("Please input difficulty:")

g = WordGenerator(n)
s = screen(r, sp)

g.getdictionary()
g.filterwords()
stdscr = initscr()

while len(g.filtered) != 0:
	g.releaseword()
	s.animatescreen(g.nextword, stdscr)

stdscr.getkey()
endwin()

		

			
			

