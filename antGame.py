# antGame
# By Jina Sung https://github.com/ToasT1ng
# Released under a "Simplified BSD" license

import numpy as np
import random

class Ant :
	def __init__(self,game) :
		self.game = game
		self.ant = np.zeros([20,20])
		self.state = np.zeros([20,20])

	def set(self) : # Initial Setting
		for i in range(0,20) :
			for j in range(0,20) :
				if (self.game[i,j] == 1) :
					self.ant[i,j] = 1
					self.state[i,j] = 1

	def setCount(self,i,j):
		self.ant[i,j] = 1

	def count(self):
		for i in range(0,20) :
			for j in range(0,20) : 
				if (self.ant[i,j] >= 1) :
					self.ant[i,j] += 1

	def breed(self,i,j):
		if (self.ant[i,j] % 3 == 1) : return True
		else : return False

	def remove(self,i,j):
		self.ant[i,j] = 0

	def change(self,changeI,changeJ,i,j):
		self.ant[changeI,changeJ] = self.ant[i,j]
		self.ant[i,j] = 0
		self.state[changeI,changeJ] = self.state[i,j]
		self.state[i,j] = 0

	def changeState(self,i,j):
		self.state[i,j] = 2

	def resetState(self):
		for i in range(0,20) :
			for j in range(0,20) : 
				if (self.state[i,j] == 2):
					self.state[i,j] = 1

	def currentState(self,i,j):
		return self.state[i,j]	

	def showAnt(self):
		return self.ant


class Doodle :
	def __init__(self,game) :
		self.game = game
		self.doodle = np.zeros([20,20])
		self.starveCount = np.zeros([20,20])
		self.state = np.zeros([20,20])

	def set(self) : # Initial Setting
		for i in range(0,20) :
			for j in range(0,20) :
				if (self.game[i,j] == 2) :
					self.doodle[i,j] = 1
					self.starveCount[i,j] = 1
					self.state[i,j] = 1

	def count(self):
		for i in range(0,20) :
			for j in range(0,20) : 
				if (self.doodle[i,j] >= 1) :
					self.doodle[i,j] += 1

	def starveCounting(self):
		for i in range(0,20) :
			for j in range(0,20) : 
				if (self.starveCount[i,j] >= 1) :
					self.starveCount[i,j] += 1

	def setCount(self,i,j):
		self.doodle[i,j] = 1

	def resetStarve(self,i,j):
		self.starveCount[i,j] = 1

	def removeDoodle(self,i,j):
		self.starveCount[i,j] = 0
		self.doodle[i,j] = 0

	def starve(self,i,j):
		if (self.starveCount[i,j] == 5) : return True
		else : return False	

	def breed(self,i,j):
		if (self.doodle[i,j] % 8 == 1) : return True
		else : return False

	def change(self,changeI,changeJ,i,j):
		self.doodle[changeI,changeJ] = self.doodle[i,j]
		self.doodle[i,j] = 0	
		self.starveCount[changeI,changeJ] = self.starveCount[i,j]
		self.starveCount[i,j] = 0	
		self.state[changeI,changeJ] = self.state[i,j]
		self.state[i,j] = 0		

	def changeState(self,i,j):
		self.state[i,j] = 2

	def resetState(self):
		for i in range(0,20) :
			for j in range(0,20) : 
				if (self.state[i,j] == 2):
					self.state[i,j] = 1

	def currentState(self,i,j):
		return self.state[i,j]

	def showDoodle(self):
		return self.doodle

	def showStarve(self):
		return self.starveCount

def main():
	game = np.zeros([20,20])
	time = 0

	makeAnt(game) 
	makeDoodle(game) # Initial Settings
	
	ant = Ant(game)
	doodle = Doodle(game)
	ant.set()
	doodle.set() # Making Objects

	printStatus(game,time)
	time += 1
	while True :
		flag = input("Press Enter.")
		if (flag != ""): break # If not just press 'Return/Enter' Key
		runGame(game,time,ant,doodle) # Running Game
		time += 1

def runGame(game,time,ant,doodle):
	ant.count()
	doodle.count()
	doodle.starveCounting()
	
	for i in range(0,20):
		for j in range(0,20):
			## Starve
			if (doodle.starve(i,j)):
				doodle.removeDoodle(i,j)
				game[i,j] = 0

			## Move
			# Doodle Move
			if (game[i,j]==2 and doodle.currentState(i,j)==1): 
				direction = random.randint(1,4)
				if (direction==1 and i-1>=0 and game[i-1,j]!=2 ): # Up
					if (game[i-1,j]==1 and game[i,j]==2) :
						doodle.resetStarve(i,j)
						ant.remove(i-1,j)
					doodle.change(i-1,j,i,j)
					doodle.changeState(i-1,j)
					game[i-1,j] = game[i,j]
					game[i,j] = 0

				if (direction==2 and j-1>=0 and game[i,j-1]!=2): # Left
					if (game[i,j-1]==1 and game[i,j]==2) :
						doodle.resetStarve(i,j)
						ant.remove(i,j-1)
					doodle.change(i,j-1,i,j)
					doodle.changeState(i,j-1)
					game[i,j-1] = game[i,j]
					game[i,j] = 0

				if (direction==3 and j+1<=19 and game[i,j+1]!=2): # Right
					if (game[i,j+1]==1 and game[i,j]==2) :
						doodle.resetStarve(i,j)
						ant.remove(i,j+1)
					doodle.change(i,j+1,i,j)
					doodle.changeState(i,j+1)
					game[i,j+1] = game[i,j]
					game[i,j] = 0

				if (direction==4 and i+1<=19 and game[i+1,j]!=2): # Down
					if (game[i+1,j]==1 and game[i,j]==2) :
						doodle.resetStarve(i,j)
						ant.remove(i+1,j)
					doodle.change(i+1,j,i,j)
					doodle.changeState(i+1,j)	
					game[i+1,j] = game[i,j]
					game[i,j] = 0

			# Ant Move	
			if (game[i,j]==1 and ant.currentState(i,j)==1): 
				direction = random.randint(1,4)
				if (direction==1 and i-1>=0 and game[i-1,j]==0): # Up
					ant.change(i-1,j,i,j)
					ant.changeState(i-1,j)
					game[i-1,j] = game[i,j]
					game[i,j] = 0
				if (direction==2 and j-1>=0 and game[i,j-1]==0): # Left
					ant.change(i,j-1,i,j)
					ant.changeState(i,j-1)
					game[i,j-1] = game[i,j]
					game[i,j] = 0
				if (direction==3 and j+1<=19 and game[i,j+1]==0): # Right
					ant.change(i,j+1,i,j)
					ant.changeState(i,j+1)
					game[i,j+1] = game[i,j]
					game[i,j] = 0
				if (direction==4 and i+1<=19 and game[i+1,j]==0): # Down
					ant.change(i+1,j,i,j)
					ant.changeState(i+1,j)
					game[i+1,j] = game[i,j]
					game[i,j] = 0
			
			## Breed
			# Ant Breed
			breedDirect = random.randint(1,4)
			if (ant.breed(i,j)) : 
				if (breedDirect==1 and i-1>=0 and game[i-1,j]==0): # Up
					game[i-1,j] = 1
					ant.setCount(i-1,j)
				elif (breedDirect == 2 and j-1>=0 and game[i,j-1]==0): # Left
					game[i,j-1] = 1
					ant.setCount(i,j-1)
				elif (breedDirect == 3 and j+1<=19 and game[i,j+1]==0): # Right
					game[i,j+1] = 1
					ant.setCount(i,j+1)
				elif (breedDirect == 4 and i+1<=19 and game[i+1,j]==0): # Down
					game[i+1,j] = 1
					ant.setCount(i+1,j)
			# Doodle Breed
			breedDirect = random.randint(1,4)
			if (doodle.breed(i,j)) :
				if (breedDirect==1 and i-1>=0 and game[i-1,j]==0): # Up
					game[i-1,j] = 2
					doodle.setCount(i-1,j)
				elif (breedDirect == 2 and j-1>=0 and game[i,j-1]==0): # Left
					game[i,j-1] = 2
					doodle.setCount(i,j-1)
				elif (breedDirect == 3 and j+1<=19 and game[i,j+1]==0): # Right
					game[i,j+1] = 2
					doodle.setCount(i,j+1)
				elif (breedDirect == 4 and i+1<=19 and game[i+1,j]==0): # Down
					game[i+1,j] = 2
					doodle.setCount(i+1,j)

	doodle.resetState()
	ant.resetState()
	# print("-------------")
	# print("-------------")
	# printObject(ant.showAnt())
	# print("-------------")
	# printObject(doodle.showDoodle())
	# print("-------------")
	# printObject(doodle.showStarve())
	# print("-------------")
	printStatus(game,time)

def makeAnt(game):
	number = 0
	while (number != 100) :
		position = random.randint(1,400)
		x_position = position % 20
		y_position = position // 20
		if (game[x_position-1,y_position-1]	!= 1) :
			game[x_position-1,y_position-1]	= 1
			number += 1

def makeDoodle(game):
	number = 0
	while (number != 5) :
		position = random.randint(1,400)
		x_position = position % 20
		y_position = position // 20
		if (game[x_position-1,y_position-1] != 1) and (game[x_position-1,y_position-1] != 2):
			game[x_position-1,y_position-1] = 2
			number += 1

def printStatus(game,time):
	firstLine = "  "
	for index in range(1,21):
		firstLine += str(index).rjust(5)
	print(firstLine + "   Time : " + str(time))
	for i in range(0,20) :
		line = str(i+1).rjust(2)
		for j in range(0,20) :
			if (game[i,j] == 1) :
				line += "O".rjust(5) 
			elif (game[i,j] == 2) :
				line += "X".rjust(5)
			else :
				line += " ".rjust(5)
		print(line)
	

def printObject(game):
	firstLine = "  "
	for index in range(1,21):
		firstLine += str(index).rjust(5)
	print(firstLine)
	for i in range(0,20) :
		line = str(i+1).rjust(2)
		for j in range(0,20) :
			if (game[i,j] >= 1) :
				line += str(game[i,j]).rjust(5) 
			else :
				line += " ".rjust(5)
		print(line)

if __name__ == '__main__':
    main()

# main()
