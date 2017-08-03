#Etch-a-Sketchy
from tkinter import*
#Set variables
canvas_height = 720
canvas_width = 1280
canvas_pos_X = 400
canvas_pos_Y = 400
canvas_color = "gray"

#Set the initial cursor start position
posX=canvas_width/2
posY=canvas_height/2

#Set the line color/width
line_color="black"
line_width = 2
line_length = 2

#functions:
def Move_N(self):
	global posY
	if posY > 0:
		canvas.create_line(posX,posY,posX,(posY-line_length), width=line_width, fill=line_color)
		posY=posY-line_length

def Move_E(self):
	global posX
	if posX < (canvas_width - (line_width/2)):
		canvas.create_line(posX,posY,posX + line_length, posY, width=line_width, fill=line_color)
		posX=posX + line_length

def Move_S(self):
	global posY
	if posY < canvas_height:
		canvas.create_line(posX,posY,posX,posY+line_length, width=line_width, fill=line_color)
		posY = posY + line_length

def Move_W(self):
	global posX
	if posX > 0:
		canvas.create_line(posX, posY, posX - line_length, posY, width=line_width, fill=line_color)
		posX = posX - line_length

def forget(self):
	global canvas
	global posX
	global posY
	canvas.destroy()
	canvas = Canvas(bg=canvas_color, height=canvas_height, width=canvas_width, highlightthickness=0)
	canvas.pack()
	posX=canvas_width/2
	posY=canvas_height/2

#main:
window = Tk()

#Sets, and locks, the window dimensions (width, height, x_position, y_position)
window.geometry('%dx%d+%d+%d' % (canvas_width, canvas_height, canvas_pos_X, canvas_pos_Y))
window.resizable(width=False, height=False)

#Sets the window to "borderless"
window.overrideredirect(1)

#No longer needed when using overrideredirect
#window.title("Etch-a-Sketchy")

canvas = Canvas(bg=canvas_color, height=canvas_height, width=canvas_width, highlightthickness=0)
canvas.pack()

#Create the key bindings 
window.bind("<Up>",Move_N)
window.bind("<Right>",Move_E)
window.bind("<Down>",Move_S)
window.bind("<Left>",Move_W)
window.bind("s",forget)
window.bind("q",exit)

#Open the window
window.mainloop()
