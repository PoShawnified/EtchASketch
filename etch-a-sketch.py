#Etchy-ah-Sketchy
try:
    #for Python2
    from Tkinter import *
except ImportError:
    #for Python3
    from tkinter import *

#Set variables
canvas_width  = 1280
canvas_height = 720
canvas_pos_X  = 50
canvas_pos_Y  = 50
canvas_color  = "gainsboro"

#Set the initial cursor start position
cursorX=canvas_width/2
cursorY=canvas_height/2

#Set the line color/width
line_colors = ["black", "red", "forestgreen", "royalblue", "gainsboro"]
current_line_color = line_colors[0]
line_width  = 2
line_length = 2

#functions:
#arrow="last", stipple="gray75"
def Move_Up(self):
	global cursorY
	if cursorY > 0:
		canvas.create_line(cursorX, 
											 cursorY, 
											 cursorX, 
											 (cursorY - line_length), 
											 width=line_width, 
											 fill=current_line_color, 
											 capstyle="round", 
											 joinstyle="round")
		cursorY = (cursorY - line_length)

def Move_Down(self):
	global cursorY
	if cursorY < canvas_height:
		canvas.create_line(cursorX, 
											 cursorY, 
											 cursorX, 
											 (cursorY + line_length), 
											 width=line_width, 
											 fill=current_line_color, 
											 capstyle="round", 
											 joinstyle="round")
		cursorY = (cursorY + line_length)

def Move_Left(self):
	global cursorX
	if cursorX > 0:
		canvas.create_line(cursorX, 
											 cursorY, 
											 (cursorX - line_length), 
											 cursorY, 
											 width=line_width, 
											 fill=current_line_color, 
											 capstyle="round", 
											 joinstyle="round")
		cursorX = (cursorX - line_length)

def Move_Right(self):
	global cursorX
	if cursorX < (canvas_width - (line_width/2)):
		canvas.create_line(cursorX, 
											 cursorY, 
											 (cursorX + line_length), 
											 cursorY, 
											 width=line_width, 
											 fill=current_line_color, 
											 capstyle="round", 
											 joinstyle="round")
		cursorX = (cursorX + line_length)

def Clear_Screen(self):
#function to clear the screen
	global canvas
	global cursorX
	global cursorY
	canvas.destroy()
	canvas = Canvas(bg=canvas_color, height=canvas_height, width=canvas_width, highlightthickness=0)
	canvas.pack()
	cursorX = canvas_width/2
	cursorY = canvas_height/2

def Change_Color_Right(self):
#function to change the line color 
#by cycling through the color list
	global current_line_color
	if line_colors.index(current_line_color) == (len(line_colors)-1):
		current_line_color = line_colors[0]
	else:
		current_line_color = line_colors[line_colors.index(current_line_color)+1]

def Change_Color_Left(self):
#function to change the line color 
#by cycling through the color list
	global line_colors
	global current_line_color
	if line_colors.index(current_line_color) == line_colors[0]:
		current_line_color = line_colors[len(line_colors)-1]
	else:
		current_line_color = line_colors[line_colors.index(current_line_color)-1]
		
#main:
window = Tk()

#Sets, and locks, the window dimensions (width, height, x_position, y_position)
window.geometry('%dx%d+%d+%d' % (canvas_width, canvas_height, canvas_pos_X, canvas_pos_Y))
window.resizable(width=False, height=False)

#Sets the window to "borderless"
#window.attributes('-fullscreen', True)

#No longer needed when using attributes('-fullscreen', True)
#window.title("Etchy-ah-Sketchy")

canvas = Canvas(bg=canvas_color, height=canvas_height, width=canvas_width, highlightthickness=0)
canvas.pack()

#Create the key bindings 
window.bind("<Up>"   , Move_Up)
window.bind("<Down>" , Move_Down)
window.bind("<Left>" , Move_Left)
window.bind("<Right>", Move_Right)

window.bind("1", Change_Color_Left)
window.bind("2", Change_Color_Right)

window.bind("c", Clear_Screen) 

window.bind("q", exit)   #Obviously used to quit

#Open the window
window.mainloop()
