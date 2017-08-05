#Etchy-ah-Sketchy

#Import libs
try: 
  import RPi.GPIO as GPIO
except ImportError:
  print "RPi.GPIO not found... "
  print "You'll be limited to keystroke input"
  
try:
  #For Python2
  from Tkinter import *
except ImportError:
  #For Python3
  from tkinter import *

#****** Set variables ******#
canvas_width  = 1280
canvas_height = 720
canvas_pos_X  = 50
canvas_pos_Y  = 50
canvas_color  = "gainsboro"

  #Set the initial cursor position
cursorX=canvas_width/2
cursorY=canvas_height/2

  #Set the line color/width/shape
line_colors        = ["black", "red", "forestgreen", "royalblue", "gainsboro"]
line_current_color = line_colors[0]
line_width         = 2
line_length        = 2
line_capstyle      = "round"
line_joinstyle     = "round"

#****** Functions ******#
def Clear_Screen(self):
  #Function to clear the screen

	global canvas
	global cursorX
	global cursorY
	global line_current_color
	
	canvas.destroy()
	canvas = Canvas(bg=canvas_color, height=canvas_height, width=canvas_width, highlightthickness=0)
	canvas.pack()
	cursorX = canvas_width/2
	cursorY = canvas_height/2
	line_current_color = line_colors[0]

def Change_Color_Right(self):
  #Function to change the line color 
  #by cycling through the color list

	global line_current_color
	if line_colors.index(line_current_color) == (len(line_colors)-1):
		line_current_color = line_colors[0]
	else:
		line_current_color = line_colors[line_colors.index(line_current_color)+1]

def Change_Color_Left(self):
  #Function to change the line color 
  #by cycling through the color list
	
	global line_colors
	global line_current_color
	if line_colors.index(line_current_color) == line_colors[0]:
		line_current_color = line_colors[len(line_colors)-1]
	else:
		line_current_color = line_colors[line_colors.index(line_current_color)-1]

def Quit(self):
	#Function to quit the GUI
	window.destroy()

def Move_Cursor(self, direction):
	global cursorX
	global cursorY
	global line_capstyle 
	global line_joinstyle 

  #Needed so we don't lose track of the initial cursor position
	pvtX = cursorX
	pvtY = cursorY

  #Select which direction to expand the line
	if direction == "up":
		if cursorY > 0:
			cursorY = (cursorY - line_length)

	if direction == "down":
		if cursorY < canvas_height:
			cursorY = (cursorY + line_length)	

	if direction == "left":
		if cursorX > 0:
			cursorX = (cursorX - line_length)
		
	if direction == "right":
		if cursorX < (canvas_width - (line_width/2)):
			cursorX = (cursorX + line_length)

  #Updates the lines (potential other options: arrow="last", stipple="gray75")
	canvas.create_line(pvtX, 
										 pvtY, 
										 cursorX, 
										 cursorY, 
										 width=line_width, 
										 fill=line_current_color, 
										 capstyle=line_capstyle , 
										 joinstyle=line_joinstyle)


#****** MAIN ******#
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
window.bind_all("<Up>"   , lambda self:Move_Cursor(self,"up"))
window.bind_all("<Down>" , lambda self:Move_Cursor(self,"down"))
window.bind_all("<Left>" , lambda self:Move_Cursor(self,"left"))
window.bind_all("<Right>", lambda self:Move_Cursor(self,"right"))
window.bind_all("1", Change_Color_Left)   #Moves one color to the left
window.bind_all("2", Change_Color_Right)  #Moves one color to the right
window.bind_all("c", Clear_Screen)        #Clears the screen
window.bind_all("q", Quit)                #Obviously used to quit


GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.add_event_detect(22, GPIO.RISING, callback=Quit, bouncetime=300)
GPIO.add_event_detect(23, GPIO.RISING, callback=Change_Color_Left, bouncetime=300)
GPIO.add_event_detect(24, GPIO.RISING, callback=Change_Color_Right, bouncetime=300)
#GPIO.add_event_detect(23, GPIO.RISING, callback=lambda self:Move_Cursor(self, "up"), bouncetime=300)
GPIO.add_event_detect(27, GPIO.RISING, callback=Clear_Screen, bouncetime=300)


  #Open the window
window.mainloop()
