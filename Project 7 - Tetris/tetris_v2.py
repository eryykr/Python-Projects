import tkinter as tk 
import time
import random


#GAME PARAMETERS         
square_size = 35
grid_height = 22
grid_width = 12
HEIGHT = square_size*grid_height
WIDTH = square_size*(grid_width+7)

background_colour = 'black'
border_colour = 'white'


t_normal = 150
t_quick = 10     


#MISCELLANEOUS FUNCTIONS
#finding height of block(y-coordinate of lowest square)
def height(block):
	y = 0
	for i in block:
		if i[1] > y:
			y = i[1]
	return y
#finding x-coordinate of left-most square
def leftmost(block):
	leftmost = 12
	for i in block:
		if i[0] < leftmost:
			leftmost = i[0]
	return leftmost
#finding x-coordinate of right-most square
def rightmost(block):
	rightmost = 0
	for i in block:
		if i[0] > rightmost:
			rightmost = i[0]
	return rightmost
#generating list of positions of settled squares
def squares_only(t_list):
	coords = []
	for i in t_list:
		for ii in i[0]:
			coords.append(ii)
	return coords
#splitting settled-pieces list by individual squares
def single_squares(t_list):
	new = []
	for i in t_list:
		for ii in i[0]:
			new.append([[ii], i[-1]])
	return new


#FUNCTION FOR DDRAWING SQUARES
def draw(coordinates, colour):
	for i in coordinates:
		c.create_rectangle((i[0]-1)*square_size, (i[1]-1)*square_size,
		i[0]*square_size, i[1]*square_size, fill=colour)

#GAME WINDOW
#main window
window = tk.Tk()
window.title("TETRIS")
window.resizable(False, False)
c = tk.Canvas(master=window, height=HEIGHT, width=WIDTH, background=background_colour)
c.pack()
#border
border_list = []
for i in range(grid_height):
	border_list.append([1,i])
	border_list.append([grid_width, i])
	border_list.append([i, grid_height])
	border_list.append([grid_width+7, i])
for i in range(grid_width, grid_width+7):
	border_list.append([i, 1])
	border_list.append([i, 8])
	border_list.append([i, 15])
draw(border_list, border_colour)
#text
c.create_text(30,30,fill="white",font="Times 20 italic bold",
                        text="Click the bubbles that are multiples of two.")

#CREATING TETROMINOS
colours = ["cyan", "blue", "orange", "yellow", "green", "red", "purple"]
def new_piece(n):
	i_block = [[5,0], [6,0], [7,0], [8,0]]
	j_block = [[6,-1], [6,0], [7,0], [8,0]]
	l_block = [[5,0], [7,0], [6,0], [7,-1]]
	o_block = [[6,-1], [7,-1], [6,0], [7,0]]
	s_block = [[5,0], [6,0], [6,-1], [7,-1]]
	z_block = [[6,-1], [7,0], [7,-1], [8,0]]
	t_block = [[5,0], [6,0], [7,0], [6,-1]]
	#placing blocks and their respective colours into lists
	blocks = [i_block, j_block, l_block, o_block, s_block, z_block, t_block]
	return blocks[n]

#version for "NEXT" window
def new_piece_next(n):
	i_block = [[14,5], [15,5], [16,5], [17,5]]
	j_block = down(right(rotate([[14,4], [14,5], [15,5], [16,5]])))
	l_block = down(rotate([[13,5], [15,5], [14,5], [15,4]]))
	o_block = [[15,4], [16,4], [15,5], [16,5]]
	s_block = down(left(rotate([[15,5], [16,5], [16,4], [17,4]])))
	z_block = rotate([[14,5], [15,6], [15,5], [16,6]])
	t_block = rotate([[14,6], [15,6], [16,6], [15,5]])
	#placing blocks and their respective colours into lists
	blocks = [i_block, j_block, l_block, o_block, s_block, z_block, t_block]
	return blocks[n]



#MANIPULATING THE TETROMINOS
#shifting up
def up(block):
	for i in block:
		i[1] = i[1]-1
	return block
#shifting down
def down(block):
	for i in block:
		i[1] = i[1]+1
	return block
#shifting right
def right(block):
	for i in block:
		i[0] = i[0]+1
	return block
#shifting left
def left(block):
	for i in block:
		i[0] = i[0]-1
	return block
#rotation
def rotate(block):
	initial_height = height(block)
	#performing rotation
	centre = block[1]
	for i in block:
		if i != centre:
			x = i[0]-centre[0]
			y = i[1]-centre[1]
			i[0] = -y+centre[0]
			i[1] = x+centre[1]
	#making sure height remains the same
	while initial_height != height(block):
		if initial_height > height(block):
			block = down(block)
		else:
			block = up(block)
	return block

#CREATING GAME OBJECT CLASS
class Game:
	#INITIAL TETROMINO
	def __init__(self):
		t_index = random.randint(0,6)
		self.t_index_next = random.randint(0,6)
		self.tetromino_shape = new_piece(t_index)
		self.tetromino_colour = colours[t_index]
		self.settled_tetrominos = []
		self.frame_time = t_normal

		self.LINES = 0
		self.SCORE = 0

	#DRAWING TETROMINOS AND BORDER
	def display(self):
		c.delete("all")
		#settled
		if len(self.settled_tetrominos) > 0:
			for i in self.settled_tetrominos:
				draw(i[0], i[-1])
		#falling
		draw(self.tetromino_shape, self.tetromino_colour)
		#border
		draw(border_list, border_colour)
		#text
		c.create_text(523,52,fill="white",font="Lucida 30 bold", text="NEXT")
		c.create_text(523,297,fill="white",font="Lucida 30 bold", text="SCORE")
		c.create_text(523,543,fill="white",font="Lucida 30 bold", text="LINES")

		c.create_text(523,385,fill="white",font="Lucida 30 bold", 
						text="0"*(8-len(str(self.SCORE)))+str(self.SCORE))
		c.create_text(523,630,fill="white",font="Lucida 30 bold", 
						text="0"*(8-len(str(self.LINES)))+str(self.LINES))
        
		#next piece
		draw(new_piece_next(self.t_index_next), colours[self.t_index_next])

	#MANIPULATING THE FALLING TETRONIMO
	def move_right(self, event):
		if rightmost(self.tetromino_shape) < grid_width-1:
			self.tetromino_shape = right(self.tetromino_shape)
			#making sure pieces cannot move into each other
			if len(self.settled_tetrominos) > 0:
				all_squares = squares_only(self.settled_tetrominos) + self.tetromino_shape
				if any(all_squares.count(x) > 1 for x in all_squares) == True:
					self.tetromino_shape = left(self.tetromino_shape)
			#updating screen
			c.delete("all")
			self.display()

	def move_left(self, event):
		if leftmost(self.tetromino_shape) > 2:
			self.tetromino_shape = left(self.tetromino_shape)
			#making sure pieces cannot move into each other
			if len(self.settled_tetrominos) > 0:
				all_squares = squares_only(self.settled_tetrominos) + self.tetromino_shape
				if any(all_squares.count(x) > 1 for x in all_squares) == True:
					self.tetromino_shape = right(self.tetromino_shape)
			#updating screen
			c.delete("all")
			self.display()

	def move_down(self, event):
		self.frame_time = t_quick
		
	def turn(self, event):
		c.delete("all")
		self.tetromino_shape = rotate(self.tetromino_shape)
		#making sure not out of bounds
		if rightmost(self.tetromino_shape) > grid_width-1:
			self.tetromino_shape = left(self.tetromino_shape)
		elif leftmost(self.tetromino_shape) == 1 or 0:
			self.tetromino_shape = right(self.tetromino_shape)
		self.display()

	#EXITING GAME
	def exit(self, event):
		window.quit()

	#CHECKING FOR WHETHER TETROMINO HAS SETTLED
	def check_fallen(self):
		#checking whether falling tetromino is on top of another
		settled_squares = squares_only(self.settled_tetrominos).copy()
		falling_squares = self.tetromino_shape.copy()
		#counting squares on top of other squares
		n = 0
		for i in settled_squares:
			for j in falling_squares:
				if i[0] == j[0] and i[1] - j[1] == 1:
					n = n + 1
		if n > 0:
			#appending to list of settled tetrominos
			self.settled_tetrominos.append([self.tetromino_shape, self.tetromino_colour])
			#generating new tetromino
			new_t_index = self.t_index_next
			self.tetromino_shape = new_piece(new_t_index)
			self.tetromino_colour = colours[new_t_index]
			self.frame_time = t_normal
			#new next tetromino
			self.t_index_next = random.randint(0,6)


		#checking whether falling tetromino touches bottom of well
		elif height(self.tetromino_shape) == grid_height-1:
			#appending to list of settled tetrominos
			self.settled_tetrominos.append([self.tetromino_shape, self.tetromino_colour])
			#generating new tetromino
			new_t_index = self.t_index_next
			self.tetromino_shape = new_piece(new_t_index)
			self.tetromino_colour = colours[new_t_index]
			self.frame_time = t_normal
			#new next tetromino
			self.t_index_next = random.randint(0,6)

	#CHECKING WHETHER THERE IS A HORIZONTAL LINE OF SQUARES
	def check_line(self):
		#list for storing positions of lines
		lines = []
		#checking if any tetrominos have settled
		if len(self.settled_tetrominos) > 0:
			#list of all squares which have settled
			settled_squares = squares_only(self.settled_tetrominos)
			#iterating over all horizontal lines, from the bottom up
			for i in range(21,0,-1):
				n = 0
				#counting squares along horizontal
				for ii in settled_squares:
					if ii[1] == i:
						n = n + 1
				#removing unwanted squares
				if n == 10:
					lines.append(i)
					new = []
					for j in self.settled_tetrominos:
						new_sub = []
						for jj in j[0]:
							if jj[-1] != i:
								new_sub.append(jj)
						new.append([new_sub, j[-1]])
					self.settled_tetrominos = new
		
		#updating on-screen metrics
		#no.of lines:
		self.LINES = self.LINES + len(lines)
		#score:
		if len(lines) > 0:
			spacing = ""
			for i in range(0, len(lines)-1):
				spacing=spacing+str(lines[i]-lines[i+1])

			#case of a tetris
			if "111" in spacing:
				self.SCORE = self.SCORE + 1200
			#case of triple lines
			elif "11" in spacing:
				self.SCORE = self.SCORE + 300
			#all other cases
			else:
				if "1" in spacing:
					self.SCORE = self.SCORE + (100*spacing.count("1"))
					self.SCORE = self.SCORE + (100*((len(lines)-1)-spacing.count("1")))
				else:
					self.SCORE = self.SCORE + (40*len(lines))				
		self.display()

		#shifting remaining squares down
		lines.reverse()
		new = []
		self.settled_tetrominos = single_squares(self.settled_tetrominos)
		if len(lines) > 0:
			for i in lines:
				for ii in self.settled_tetrominos:
					x = ii[0][0][0]
					y = ii[0][0][-1]
					colour = ii[-1]
					if y < i:
						new.append([[[x, y+1]],colour])
					else:
						new.append([[[x, y]],colour])
				
				self.settled_tetrominos = new.copy()
				new = []
		
					                    				
	#AUTOMATICALLY MOVING FALLING TETROMINO DOWN
	def auto_move(self):
		down(self.tetromino_shape)

	#CHECKING THAT FALLING TETROMINO WITHIN BOUNDS
	def check_bounds(self):
		while leftmost(self.tetromino_shape) < 2:
			self.tetromino_shape = right(self.tetromino_shape)
		while rightmost(self.tetromino_shape) > grid_width-1:
			self.tetromino_shape = left(self.tetromino_shape)

	#CHECKING FOR GAME OVER
	def check_gameover(self):
		for i in squares_only(self.settled_tetrominos):
			if i[-1] == 1:
				window.quit()
				#print("GAME OVER")
				#self.settled_tetrominos = [] 
	


#INSTANTIATING GAME OBJECT
game = Game()
game.display()

#KEY BINDINGS FOR CONTROLS
window.bind("<Right>", game.move_right)
window.bind("<Left>", game.move_left)
window.bind("<Up>", game.turn)
window.bind("<space>", game.move_down)
window.bind("<Return>", game.exit)


#ANIMATING
def animate():

	game.check_bounds()
	game.check_gameover()
	game.display()
	game.check_fallen()
	game.check_line()
	game.auto_move() 

	c.after(game.frame_time, animate)

animate()
window.mainloop()