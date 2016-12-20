#!/usr/bin/python

from curses import *
import random, time
import threading

class wordobj(object):
	def __init__(self, x, y, word):
		self.posx = x
		self.posy = y
		self.word = word
	def __repr__(self):
		return "%s" % self.word

class wordbuffer(object):
	def __init__(self):
		self.list = []
		self.length = len(self.list)
	def addword(self, word):
		self.list.append(word)

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
			if len(word) >= self.worddiff:
				self.filtered.append(word)

	def generateword(self, wordbuffer, stdscr):
		self.nextword = random.choice(self.filtered)
		wordpos = random.choice(range(3, stdscr.width-2-len(self.nextword)))
		word = wordobj(wordpos, 4, self.nextword)
		wordbuffer.addword(word)
		#self.filtered.remove(self.nextword)
		time.sleep(60/stdscr.gendiff)

	
class screen(object):
	def __init__(self, wpm, difficulty):
		self.gendiff = float(wpm)
		self.speeddiff = float(difficulty)
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

	def animatescreen(self, wordbuffer, stdscr):
		while len(wordbuffer.list) != 0:
	
			for word in wordbuffer.list:
				if word.posy == self.height-3:
					stdscr.addstr(word.posy, word.posx, self.bg)

					for i in range(word.posx, word.posx + len(word.word)):
						stdscr.addstr(word.posy-1, i, self.bg, self.clearcolor)

					wordbuffer.list.remove(word)

				else:
					stdscr.addstr(word.posy, word.posx, word.word, self.contentcolor)
						
					for i in range(word.posx, word.posx + len(word.word)):
						stdscr.addstr(word.posy-1, i, self.bg, self.clearcolor)

					word.posy = word.posy + 1

			stdscr.refresh()
			time.sleep(1/self.speeddiff)

class listener(threading.Thread):
	def __init__(self, screen, animscr, wordbuffer):
		threading.Thread.__init__(self)
		self.scr = screen
		self.animscr = animscr
		self.wordbuffer = wordbuffer
	def run(self):
		myInput = ''

		while myInput != 'quitgame':

			myInput = self.animscr.getstr()

			for word in self.wordbuffer.list:
				if word.word == myInput:
					self.animscr.addstr(word.posy, word.posx, self.scr.bg, self.scr.contentcolor)
						
					for i in range(word.posx, word.posx + len(word.word)):
						self.animscr.addstr(word.posy-1, i, self.scr.bg, self.scr.clearcolor)

					self.wordbuffer.list.remove(word)

		stdscr.getkey()
		endwin()



class GeneratorThread(threading.Thread):
	def __init__(self, generator, wordbuffer, screen):
		threading.Thread.__init__(self)
		self.generator = generator
		self.wbuffer = wordbuffer
		self.screen = screen
	def run(self):
		while len(self.generator.filtered) != 0:
			self.generator.generateword(self.wbuffer, self.screen)

class AnimatorThread(threading.Thread):
	def __init__(self, wordbuffer, screen):
		threading.Thread.__init__(self)
		self.wbuffer = wordbuffer
		self.screen = screen
	def run(self):
		s.animatescreen(self.wbuffer, self.screen)

n = raw_input("Please enter word length threshold:  ")
r = raw_input("Please enter word generation difficulty (WORDS per MINUTE):  ")
sp = raw_input("Please input difficulty (SPEED of DROP per SECOND. 1/{input}):  ")

g = WordGenerator(n)
s = screen(r, sp)
w = wordbuffer()

g.getdictionary()
g.filterwords()

stdscr = initscr()
s.initializescreen(stdscr)

genthread = GeneratorThread(g, w, s)
animthread = AnimatorThread(w, stdscr)
listener = listener(s, stdscr, w)

genthread.start()
animthread.start()
listener.start()

		

			
			

