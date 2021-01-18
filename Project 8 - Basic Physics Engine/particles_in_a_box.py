import tkinter as tk
import random

#FUNCTIONS
#distance between 2 points
def vector_dot(a, b):
	return a[0]*b[0] + a[1]*b[1]
#difference between vectors
def vector_subract(a,b):
	return [a[0]-b[0], a[1]-b[1]]
#distance between points
def distance(a,b):
	return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5
#scalar multiplication
def vector_multiplication(vec, a):
	new = []
	for i in vec:
		new.append(i*a)
	return new

#PARTICLE BOX PROPERTIES
HEIGHT = 600
WIDTH = 600
BACKGROUND_COLOUR = "black"
PARTICLE_COLOUR = "red"
PARTICLE_RADIUS = 30

#ANIMATION SETTINGS
dt = 0.1
frame_time = 10
particle_amount = 5

#CANVAS WIDGET FOR PARTICLE BOX
window = tk.Tk()
window.title("PARTICLES")
window.resizable(False, False)
box = tk.Canvas(master=window, height=HEIGHT, width=WIDTH, background=BACKGROUND_COLOUR)
box.pack()


#FUNCTION FOR DISPLAYING PARTICLES
def draw_particle(position, radius):
	box.create_oval(position[0]-radius, (HEIGHT-position[1])-radius, 
					position[0]+radius, (HEIGHT-position[1])+radius,
					fill=PARTICLE_COLOUR, outline=PARTICLE_COLOUR)


#'GAS' OBJECT CLASS
class Gas:
	#initial positions and velocities of gas paricles
	def __init__(self, positions, velocities):
		self.positions = positions
		self.velocities = velocities
		self.PLAY = True
	#updating the display
	def update(self):
		box.delete("all")
		for i in self.positions:
			draw_particle(i, PARTICLE_RADIUS)
	#moving the particles
	def move(self):
		if self.PLAY == True:
			new_positions = []
			for i, j in zip(self.positions, self.velocities):
				new_x = i[0] + j[0]*dt
				new_y = i[-1] + j[-1]*dt #(we subtract due to this coordinate system)
				new_positions.append([new_x, new_y])
			self.positions = new_positions
	#checking for collisions with walls
	def check_wall_collision(self):
		new_velocities = []
		for i, j in zip(self.positions, self.velocities):
			#checking every wall
			if i[0]+PARTICLE_RADIUS >= WIDTH:
				new_velocities.append([-j[0], j[-1]])
			elif i[0]-PARTICLE_RADIUS <= 0:
				new_velocities.append([-j[0], j[-1]])
			elif i[-1]+PARTICLE_RADIUS >= HEIGHT:
				new_velocities.append([j[0], -j[-1]])
			elif i[-1]-PARTICLE_RADIUS <= 0:
				new_velocities.append([j[0], -j[-1]])
			else:
				new_velocities.append([j[0], j[-1]])
		self.velocities = new_velocities
	#checking for collisions between particles
	def check_particle_collision(self):
		#finding indices of colliding particles
		collided = []
		for i in self.positions:
			for j in self.positions:
				if distance(i,j) <= 2*PARTICLE_RADIUS and distance(i,j) > 0:
					collided.append(self.positions.index(i))
		#changing velocities
		if len(collided) > 0:
			i1 = collided[0]
			i2 = collided[1]
			x1 = self.positions[i1]
			x2 = self.positions[i2]
			v1 = self.velocities[i1]
			v2 = self.velocities[i2]
			
			dot1 = vector_dot(vector_subract(v1,v2), vector_subract(x1,x2))
			mag1 = vector_dot(vector_subract(x1,x2), vector_subract(x1,x2))
			diff1 = vector_subract(x1,x2)
			delta1 = vector_multiplication(diff1, dot1/mag1)
			new_v1 = vector_subract(v1, delta1)

			dot2 = vector_dot(vector_subract(v2,v1), vector_subract(x2,x1))
			mag2 = vector_dot(vector_subract(x2,x1), vector_subract(x2,x1))
			diff2 = vector_subract(x2,x1)
			delta2 = vector_multiplication(diff2, dot2/mag2)
			new_v2 = vector_subract(v2, delta2)

			self.velocities[i1] = new_v1
			self.velocities[i2] = new_v2

	#checking for out of bounds
	def check_bounds(self):
		new_positions = []
		for i in self.positions:
			if i[0]+PARTICLE_RADIUS > WIDTH:
				new_positions.append([WIDTH-PARTICLE_RADIUS-0.01, i[-1]])
			elif i[0]-PARTICLE_RADIUS < 0:
				new_positions.append([PARTICLE_RADIUS+0.01, i[-1]])
			elif i[-1]+PARTICLE_RADIUS > HEIGHT:
				new_positions.append([i[0], HEIGHT-PARTICLE_RADIUS-0.01])
			elif i[-1]-PARTICLE_RADIUS < 0:
				new_positions.append([i[0], PARTICLE_RADIUS+0.01])
			else:
				new_positions.append([i[0], i[-1]])

		self.positions = new_positions

	#pausing and playing the animation
	def play_pause(self, event):
		if self.PLAY == False:
			self.PLAY = True
		elif self.PLAY == True:
			self.PLAY = False
	#closing window
	def quit(self, event):
		window.quit()

			

#SETTING INITIAL CONDITIONS	
positions = []
velocities = []
for i in range(particle_amount):
	positions.append([random.randint(100,500), random.randint(100,500)])
	velocities.append([random.randint(-50, 50), random.randint(-50, 50)])

gas = Gas([[100,100], [200,200], [300,300], [400,400], [500, 500]], velocities)

#KEY BINDINGS
window.bind("<space>", gas.play_pause)
window.bind("<Escape>", gas.quit)

#ANIMATING
def animate():
	gas.check_wall_collision()
	gas.check_particle_collision()
	gas.check_bounds()
	gas.move()
	gas.update()
	box.after(frame_time, animate)
animate()
window.mainloop()

