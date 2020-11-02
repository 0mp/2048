import os
import sys
import random


#INDENTATION ------> TABS <----------
'''
TODO:
 - Implement moves
  	-Move & Merge

 - Score
 
 - Rewrite the interface to look nicer

 - High scores using Repl.it Database?
  	 or JSON(possibly easier(just file writing))
  	 can't use JSON because we don't have access to an actual file system
	can use JSON because repl can write and save to a file(try it)
   
'''


# Global variables
cols = 4
rows = 4
board = [[0]*cols for i in range(rows)] # Initialize an array of size rows x cols with zeroes 
#[[0]*cols]*rows does not work, all rows have same pointer
lost = False
score = 0


# spawn a random tile
def spawn_random():
	done = False
	while not done:
		i = random.randint(0, rows-1)
		j = random.randint(0, cols-1)
		# check if block occupied
		if board[i][j] == 0:  	  	  
			# spawn 2 with 90% probability
			if random.randint(0, 9) < 9:
				board[i][j] = 2
			# and 4 with 10%
			else:
				board[i][j] = 4
			done = True


# get the board ready
def prepare_board():
  	global board
  	board = [[0]*cols for i in range(rows)]

  	# spawn two random tiles for starting board
  	spawn_random()
  	spawn_random()


# Print the board
# Maybe rewrite to look nicer?
def print_board():
	for i in range(0, rows):
		for j in range(0, cols):
			b = str(board[i][j])
			b = b.ljust(5) # Add spaces to the end until b has length 5
			print(b, end='')
		print()



# def for random spawn, win condition, 
# hopefully it doesn't break if input doesn't change the board (detect repeat? or no)
# Process a keypress
def do_move(c):
	global lost, score
	# Keypress listener/handler

	#Assuming valid input
	if (c == 'w'):
		# Up 
		for i in range(0, rows):
			for j in range(0, cols):
				if board[i][j] != 0:
					current = board[i][j]
					for k in range(i - 1, -1, -1):
						if k == 0 and board[0][j] == 0:
							board[0][j] = current
							board[i][j] = 0
							break
						elif k == 0 and board[0][j] == current:
							board[0][j] *= 2
							board[i][j] = 0
							break
						elif board[k][j] == current:
							board[k][j] *= 2
							board[i][j] = 0
							break
						else:
							board[k + 1][j] = current
							board[i][j] = 0
							break
		# print(c)
			"""
			rotate counterclockwise
      left
      rotate clockwise
			"""

	elif (c == 'a'):
		# left working [2,2,2,0]=>[4,2,0,0], [2,2,2,2]=>[4,4,0,0]
		for i in range(0, rows):
			for j in range(0, cols-1):
				for k in range(j+1, cols):
					if board[i][j]==0 or board[i][k]==0:
						continue
					if board[i][j]==board[i][k]: 
						board[i][j]*=2
						board[i][k]=0
						score+=board[i][j]
					else:
						break
					#collapse left [4,0,4,0]=>[4,4,0,0]
			board[i]=[j for j in board[i] if j]+[0]*board[i].count(0)

	elif (c == 's'):
		# down
		#initialize board - switch rows and columns
		
		columns = [[0]*cols for i in range(rows)]
		for i in range(0, rows):
			for j in range(0, cols):
				columns[i][cols-j] = board[j][i]
    #now you can treat as if 1 column is a 1d array in columns[][]shifting/merging to the left
		#collapse:
		for i in range(0, columns):
			if (columns[i].contains(0)):
				count = columns[i].count(0)
				columns[i].remove(0)
				for j in range(0,count):
					columns[i].append(0)

		#merge Process
		for i in range(0,cols):
			for j in range(0,cols-1):
				if(columns[i][j] == columns[i][j+1] and columns[i][j]!=0):
					columns[i][j]*=2
					columns[i].pop(j+1) 
					columns[i].append(0)
					j+=2
    	#put back into board
		for i in range(0, rows):
			for j in range(0, cols):
				board[j][i] = columns[i][cols-j]


	elif (c == 'd'):
  	   	# right
		for i in range(0, rows):
			l = [] # list to store all nonzero tiles
			for j in range(0, cols):
				if board[i][j] > 0:
					# last tile is the same as current, then merge
					x = board[i][j]
					while len(l) > 0 and l[-1] == x:
						l.pop()
						x *= 2
						score += x
					l.append(x)
			
			# clear row
			for j in range(0, cols):
				board[i][j] = 0
			
			# refill with list l
			for j in range(0, len(l)):
				board[i][cols-len(l)+j] = l[j]

	else:
		print("invalid move")

	if check_lost():
		lost = True
	
	if not lost:
		spawn_random()


def check_lost():
  #you still need to check if anything is merge-able
  #it might be best if we have a check mergeability function. check every row and column to see if 2 consecutive elements match.
  	for i in range(0, rows):
  		for j in range(0, cols):
  			if (board[i][j] == 0):
  	  			return False
			
  	return True


# Run the game until you lose
def game():
	global lost, score

	# Get everything ready
	lost = False
	score = 0
	prepare_board()
	
	while (not lost):
		os.system('clear') # clear screen
		print_board()

		# Read in keypress using os magic
		# It makes Python instally read the character
		# Without having to press enter
		# Don't edit --------------------
		os.system("stty raw -echo")  	
		c = sys.stdin.read(1)
		os.system("stty -raw echo")
		# -------------------------------
		
		# Do a move
		do_move(c) 
		

		if c == 'l': # For debugging
  	  		lost = True

	os.system('clear') # clear screen
	print_board()
	print("You lost!")

	print("Press any key to continue ...")
	# Read in keypress using os magic
	os.system("stty raw -echo")  	
	c = sys.stdin.read(1)
	os.system("stty -raw echo")

  	  
# Main game loop
while (True):
	game() # run the game