import tkinter as tk
import time
import random


#GAME PARAMETERS
square_size = 30
grid_height = 20
grid_width = 20
HEIGHT = square_size*grid_height
WIDTH = square_size*grid_width
background_colour = 'black'
snake_colour = 'red'
food_colour = 'green'


#CREATING GAME WINDOW
window = tk.Tk()
window.title("SNAKE")
c = tk.Canvas(master=window, width=WIDTH, height=HEIGHT, background=background_colour)
c.pack()

#CREATING SNAKE OBJECT CLASS
class Snake:
	def __init__(self, position, food_position):
		self.position = position[1:len(position)]
		self.direction = position[0]
		self.food_position = food_position

	#CHECKING IF SNAKE HAS EATEN FOOD
	def eaten(self):
		if self.position[0] == self.food_position:
			
			#EXTENDING SNAKE
			square_one = self.position[0]
			if self.direction == 'u':
				self.position.insert(0, [square_one[0], square_one[1]-1])
			elif self.direction == 'd':
				self.position.insert(0, [square_one[0], square_one[1]+1])
			elif self.direction == 'l':
				self.position.insert(0, [square_one[0]-1, square_one[1]])
			elif self.direction == 'r':
				self.position.insert(0, [square_one[0]+1, square_one[1]])
			
			#GENERATING NEW FOOD SQUARE
			corners = [[1,1], [1,grid_height], [grid_width, 1], [grid_width, grid_height]]
			chosen = False
			while chosen == False:
				new_food_position = [random.randint(1, grid_width), random.randint(1, grid_height)]
				if new_food_position not in self.position and new_food_position not in corners:
					self.food_position = new_food_position
					chosen = True

    #DISPLAYING SNAKE AND FOOD
	def display(self):
		for i in self.position:
			c.create_rectangle((i[0]-1)*square_size, (i[1]-1)*square_size, i[0]*square_size, i[1]*square_size,
				fill=snake_colour)

		c.create_rectangle((self.food_position[0]-1)*square_size, (self.food_position[1]-1)*square_size,
		                    self.food_position[0]*square_size, self.food_position[1]*square_size, fill=food_colour)
    
    #SNAKE MOVEMENT
	def auto_move(self):
		#WHEN FIRST TWO SQUARES VERTICAL
		if self.direction == 'd':
			square_one = [self.position[0][0], self.position[0][1]+1]
			del self.position[len(self.position)-1]
			self.position.insert(0, square_one)
		elif self.direction == 'u':
			square_one = [self.position[0][0], self.position[0][1]-1]
			del self.position[len(self.position)-1]
			self.position.insert(0, square_one)
		
		#WHEN FIRST TWO SQUARES HORIZONTAL
		if self.direction == 'r':
			square_one = [self.position[0][0]+1, self.position[0][1]]
			del self.position[len(self.position)-1]
			self.position.insert(0, square_one)
		if self.direction == 'l':
			square_one = [self.position[0][0]-1, self.position[0][1]]
			del self.position[len(self.position)-1]
			self.position.insert(0, square_one)
			
    #DIRECTION CHANGES
	def up(self, event):
		if self.direction == 'l' or 'r':
			self.direction = 'u'

	def down(self, event):
		if self.direction == 'l' or 'r':
			self.direction = 'd'

	def left(self, event):
		if self.direction == 'u' or 'd':
			self.direction = 'l'

	def right(self, event):
		if self.direction == 'u' or 'd':
			self.direction = 'r'

	#CHECKING IF SNAKE HAS COLLIDED WITH WALL OR ITSELF
	def check(self):
		#WALLS
		if self.position[0][0] > grid_width or self.position[0][0] < 1:
			window.quit()
		if self.position[0][1] > grid_height or self.position[0][1] < 1:
			window.quit()
		#ITSELF
		if any(self.position.count(x) > 1 for x in self.position) == True:
			window.quit()


snek = Snake(['u',[5,10], [5,11], [5,12]], [10, 10])
snek.display()

#ANIMATING SNAKE
def draw():
	c.delete("all")
	snek.auto_move()
	snek.eaten()
	snek.display()
	snek.check()
	c.after(100, draw)

#CONTROLS
window.bind("<Up>", snek.up)
window.bind("<Down>", snek.down)
window.bind("<Left>", snek.left)
window.bind("<Right>", snek.right)

draw()
window.mainloop()
