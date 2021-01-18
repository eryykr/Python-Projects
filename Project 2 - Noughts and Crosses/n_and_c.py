import time
import os


#function for converting state of game into displayed output
def display(state):
	output = ('''
      |      |      
   {}  |   {}  |   {}  
______|______|______
      |      |
   {}  |   {}  |   {}
______|______|______
      |      |
   {}  |   {}  |   {}
      |      |
'''.format(state[0][0], state[0][1], state[0][2], 
	state[1][0], state[1][1], state[1][2],
	state[2][0], state[2][1], state[2][2]))
	return output 

#function for checking whether there is a winner
def result(state):
	#checking diagonals
	if state[0][0] == state[1][1] == state[2][2] or state[2][0] == state[1][1] == state[0][2]:
		winner = state[1][1]
	else:
		winner = False
	#checking horizontal and vertical stripes
	for i in range(len(state)):
		if state[i][0] == state[i][1] == state[i][2]:
			winner = state[i][0]
		elif state[0][i] == state[1][i] == state[2][i]:
			winner = state[0][i]
		else:
			continue
	return winner

#function for finding other player's symbol
def other(k):
	return list(set(('x', 'o')).difference(set(k)))[0]

#function for partitioning list into sublists
def sub(l):
	return [l[0:3], l[3:6], l[6:9]]

#function for checking whether square is taken
def taken(brd, inp):
	if inp in brd:
		return False
	else:
		return True
	
#CODE FOR MAIN GAME
board = [1,2,3,4,5,6,7,8,9]
print("WELCOME TO NOUGHTS AND CROSSES\n")

p1 = input("Player 1, would you like to be noughts or crosses? Enter x or o:\n")

p2 = other(p1)
now = p1

#instructions
print("Player 1 is "+p1+" and player 2 is "+p2+"\n")
time.sleep(2)
print("When it is your turn, enter a number from 1 to 9 to place a nought or cross\n")
time.sleep(2)
print("Player 1 starts. Game starting in 3 seconds.")
time.sleep(3)
os.system('cls')

#starting a game
turns = 0
while result(sub(board)) == False and turns < 9:
	print("Current player is "+now.upper())
	print(display(sub(board)))
	
	legal = False
	while legal == False:
		pos = int(input("Enter choice: "))
		if taken(board, pos) == False:
			legal = True
		else:
			print("Position taken")

	board[pos-1] = now
	now = other(now)
	os.system('cls')
	turns+=1

if result(sub(board)) != False:
	print(other(now).upper()+" has won!")
	print(display(sub(board)))   
	time.sleep(3)
else:
	print("It's a draw.")
	print(display(sub(board))) 
	time.sleep(3)