#!/usr/bin/python

from curses import *
import random, time
import threading

condition = threading.Condition()

class wordobj(object):					# object for a word and its coordinates in the screen
	def __init__(self, x, y, word):
		self.posx = x
		self.posy = y
		self.word = word
	def __repr__(self):
		return "%s" % self.word

class wordbuffer(object):				# object for word buffer (queue for words visible in the screen, words are consumed when word gets bottom of the screen
	def __init__(self):					# or when keyboard listener find a match)
		self.list = []
		self.length = len(self.list)
	def addword(self, word):
		self.list.append(word)

class WordGenerator(object):			# object for the word generator
	def __init__(self, ngram):
		self.worddiff = int(ngram)
		self.dict = []
		self.filtered = []
		
	def getdictionary(self):			# get all words from txt file
		textFile = open("words.txt")
		for word in textFile:
			word = word.strip()
			self.dict.append(word)
		textFile.close()
	
	def filterwords(self):				# filter dictionary based on the value of n-gram
		for word in self.dict:
			if len(word) >= self.worddiff:
				self.filtered.append(word)

	def generateword(self, wordbuffer, stdscr):					# generate word and put it in word buffer
		condition.acquire()
		if len(wordbuffer.list) == int(stdscr.height/2):		# lock for the generator when word buffer is full
			condition.wait()
		self.nextword = random.choice(self.filtered)
		wordpos = random.choice(range(3, stdscr.width-2-len(self.nextword))) 	# generate random position for word
		word = wordobj(wordpos, 5, self.nextword)
		wordbuffer.addword(word)
		condition.notify()
		condition.release()
		time.sleep(60/stdscr.gendiff)							# control rate of generation based on wpm

	
class screen(object):											# object for screen
	def __init__(self, wpm, difficulty):
		self.gendiff = float(wpm)
		self.speeddiff = float(difficulty)
		self.bg = " "
		self.mistakes = 0
		self.score = 0

	def initializescreen(self, stdscr, gen):					# initialize screen and present initial status
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
			for y in range(5, self.height-2): 				# vertical r: y-axis
				stdscr.addstr(y, x, self.bg, color_pair(1))

		n = "Minimum word length: "
		r = "Word generation rate (word per minute): "
		sp = "Difficulty (word drop speed): "
		miss = "miss:   /10"

		stdscr.addstr(1, 3, n)
		stdscr.addstr(2, 3, r)
		stdscr.addstr(3, 3, sp)
		stdscr.addstr(1, 3+len(n), str(gen.worddiff))
		stdscr.addstr(2, 3+len(r), str(self.gendiff)) 
		stdscr.addstr(3, 3+len(sp), str(self.speeddiff))
	
		stdscr.addstr(1, self.width - 3 - len(miss), miss)
		stdscr.addstr(2, self.width - 14, "Your Score:")

	def animatescreen(self, wordbuffer, stdscr):				# function for step-wise animation of the words in word buffer
		while self.mistakes < 10:
			condition.acquire()
			if len(wordbuffer.list) == 0:						# lock when word buffer is empty
				condition.wait()

			for word in wordbuffer.list:
				if word.posy == self.height-2:

					for i in range(word.posx, word.posx + len(word.word)):
						stdscr.addstr(word.posy-1, i, self.bg, self.clearcolor)
						#stdscr.addstr(word.posy, i, self.bg)

					wordbuffer.list.remove(word)				# eliminate word from buffer when it reaches bottom of the screen
					self.mistakes = self.mistakes + 1
					stdscr.addstr(1, self.width - 8, str(self.mistakes))

				elif word.posy == 5:
					stdscr.addstr(word.posy, word.posx, word.word, self.contentcolor)
					word.posy = word.posy + 1

				else:
					stdscr.addstr(word.posy, word.posx, word.word, self.contentcolor)
						
					for i in range(word.posx, word.posx + len(word.word)):
						stdscr.addstr(word.posy-1, i, self.bg, self.clearcolor)

					word.posy = word.posy + 1

			stdscr.refresh()
			condition.notify()
			condition.release()
			time.sleep(1/self.speeddiff)					# control animation speed based on difficulty

class welcome(object):										# object for welcome screen
	def fetchdata(self):									# get user input for difficulty settings
		n = "Please enter minimum word length: "
		r = "Please enter word generation rate (word per minute): "
		sp = "Please input difficulty (word drop speed): "
		title = "TYPING DEAD"
		names = "by Anjilo, Joa, Rosselle, Windsor"
		inst = "10 misses only. Make sure CapsLock isn't on."

		screen = initscr()
		curs_set(0)

		scrlength = screen.getmaxyx()
		screenheight = scrlength[0]
		screenwidth = scrlength[1]

		screen.addstr(screenheight/4, screenwidth/2 - len(title)/2, title)
		screen.refresh()
		time.sleep(0.75)
		screen.addstr(screenheight/4 + 1, screenwidth/2 - len(names)/2, names)
		screen.refresh()
		time.sleep(0.75)
		screen.addstr(screenheight/4 + 2, screenwidth/2 - len(inst)/2, inst)
		screen.refresh()
		time.sleep(0.75)

		screen.addstr(screenheight/2 - 1, screenwidth/15, n)
		screen.refresh()
		ngram = screen.getstr()

		screen.addstr(screenheight/2, screenwidth/15, r)
		screen.refresh()
		wpm = screen.getstr()

		screen.addstr(screenheight/2 + 1, screenwidth/15, sp)
		screen.refresh()
		difficulty = screen.getstr()

		self.ngram = ngram
		self.wpm = wpm
		self.difficulty = difficulty

class closing(object):										# object for showing game results
	def showresults(self, show):
		sp = "Your Score"
		over = "GAME OVER"
		inst = "Hit Enter to Exit"

		screen = initscr()
		curs_set(0)

		scrlength = screen.getmaxyx()
		screenheight = scrlength[0]
		screenwidth = scrlength[1]

		screen.addstr(screenheight/3, screenwidth/2 - len(over)/2, over)
		screen.refresh()
		time.sleep(0.5)

		screen.addstr(screenheight/2, screenwidth/2 - len(sp)/2, sp)
		screen.addstr(screenheight/2 + 1, screenwidth/2 - len(str(show.score))/2, str(show.score))
		screen.refresh()
		time.sleep(0.25)

		screen.addstr(screenheight/2+4, screenwidth/2 - len(inst)/2, inst)
		screen.refresh()
		
		return 0

# THREADS

class listener(threading.Thread):								# thread for keyboard listener
	def __init__(self, screen, animscr, wordbuffer):
		threading.Thread.__init__(self)
		self.scr = screen
		self.animscr = animscr
		self.wordbuffer = wordbuffer
	def run(self):
		myInput = ''

		while self.scr.mistakes < 10:
			myInput = self.animscr.getstr()

			condition.acquire()									# lock when word buffer is empty
			if len(self.wordbuffer.list) == 0:
				condition.wait()
			for word in self.wordbuffer.list:
				if word.word == myInput:
					self.animscr.addstr(word.posy, word.posx, self.scr.bg, self.scr.contentcolor)
						
					for i in range(word.posx, word.posx + len(word.word)):
						self.animscr.addstr(word.posy-1, i, self.scr.bg, self.scr.clearcolor)

					self.wordbuffer.list.remove(word)			# eliminate word from buffer when a match is found
					self.scr.score = self.scr.score + 1
					stdscr.addstr(3, self.scr.width - 14, str(self.scr.score))

			condition.notify()
			condition.release()


class GeneratorThread(threading.Thread):					# thread for word producer
	def __init__(self, generator, wordbuffer, screen):
		threading.Thread.__init__(self)
		self.generator = generator
		self.wbuffer = wordbuffer
		self.screen = screen
	def run(self):
		while self.screen.mistakes < 10:
			self.generator.generateword(self.wbuffer, self.screen)

class AnimatorThread(threading.Thread):						# thread for animation
	def __init__(self, wordbuffer, screen):
		threading.Thread.__init__(self)
		self.wbuffer = wordbuffer
		self.screen = screen
	def run(self):
		s.animatescreen(self.wbuffer, self.screen)

# MAIN PROGRAM

start = welcome()								# show welcome screen
start.fetchdata()								# fetch data from welcome screen

g = WordGenerator(start.ngram)					# initialize objects from difficulty settings
s = screen(start.wpm, start.difficulty)
w = wordbuffer()

g.getdictionary()								# get dictionary and filter words
g.filterwords()

stdscr = initscr()								# initialize screen to be animated
s.initializescreen(stdscr, g)					# pass dynamic attributes to object s

genthread = GeneratorThread(g, w, s)			# thread instances
animthread = AnimatorThread(w, stdscr)
listener = listener(s, stdscr, w)

threadlist = []						

genthread.start()								# start threads
animthread.start()
listener.start()

threadlist.append(genthread)					# update thread list
threadlist.append(animthread)
threadlist.append(listener)

for thread in threadlist:						# wait for threads to finish (when 10 mistakes are done)
	thread.join()

stdscr.clear()									# show closing screen (results)
bye = closing()
bye.showresults(s)

stdscr.getkey()									# wait for keyboard and exit
endwin()
		

			
			

