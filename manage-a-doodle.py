#Manage-A-Doodle
#@PoShawnified

#************ IMPORT LIBS ************#
try: 
  import RPi.GPIO as GPIO
except ImportError:
  print ("\r\nRPi.GPIO not found... You'll be limited to keystroke input. \r\n\r\n\tArrows = Movement\r\n\tc = Clear Screen\r\n\tq = Quit\r\n")
  GPIO = 0

try:
  #For Python2
  from Tkinter import *
except ImportError:
  #For Python3
  from tkinter import *
#************ END - IMPORT ************#


#************ VARIABLES ************#
canvas_width  = 1280
canvas_height = 720
canvas_pos_X  = 0
canvas_pos_Y  = 0
canvas_color  = "gainsboro"

  #Set the initial cursor position to center canvas
cursorX=canvas_width/2
cursorY=canvas_height/2

  #Set the line color/width/shape. 
  #Includes the BG color to create an "erase" effect
line_colors        = ["black", 
                      "red", 
                      "forestgreen", 
                      "orange", 
                      "purple", 
                      canvas_color, 
                      "royalblue", 
                      "gold", 
                      "fuchsia", 
                      "palegreen"]
line_current_color = line_colors[0]
line_width         = 2
line_length        = 2
line_capstyle      = "round"
line_joinstyle     = "round"
#************ END - VARIABLES ************#


#************ FUNCTIONS ************#
def Clear_Screen(self):
  #Function to clear the screen and reset the cursor

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

def RotaryEnc_Move_Cursor(self, RotatePosition, XY):
  #Function to allow the rotary encoders to call the Move_Cursor() function
  if XY == "vertical":
    while(not GPIO.input(pin_rot_V_dt)):
      CurrentRotateStatus = GPIO.input(pin_rot_V_ck)
      if (RotatePosition == 0) and (CurrentRotateStatus == 1):
        Move_Cursor(self,"down")
        break
      if (RotatePosition == 1) and (CurrentRotateStatus == 0):
        Move_Cursor(self,"up")
        break
  
  if XY == "horizontal":
    while(not GPIO.input(pin_rot_H_dt)):
      CurrentRotateStatus = GPIO.input(pin_rot_H_ck)
      if (RotatePosition == 0) and (CurrentRotateStatus == 1):
        Move_Cursor(self,"right")
        break
      if (RotatePosition == 1) and (CurrentRotateStatus == 0):
        Move_Cursor(self,"left")
        break

#************ END - FUNCTIONS ************#

#************ MAIN ************#
window = Tk()

#Sets, and locks, the window dimensions (width, height, x_position, y_position)
window.geometry('%dx%d+%d+%d' % (canvas_width, canvas_height, canvas_pos_X, canvas_pos_Y))
window.resizable(width=False, height=False)

#Sets the window to "borderless" and hide the mouse
window.attributes('-fullscreen', True)
window.config(cursor="none")

#No longer needed when using attributes('-fullscreen', True)
#window.title("Manage-A-Doodle")

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

if GPIO:
  #Pin assignments
  pin_quit         = 22
  pin_color_right  = 24
  pin_color_left   = 23
  pin_clear_screen = 27
  pin_rot_V_dt     = 17  #Vertical Encoder - DT pin
  pin_rot_V_ck     = 18  #Vertical Encoder - CLK pin
  pin_rot_H_dt     = 11  #Horizontal Encoder - DT pin
  pin_rot_H_ck     = 8   #Horizontal Encoder - CLK pin
  
  GPIO.setmode(GPIO.BCM)
  
  #Vertical Rotary Encoder - Set up rotate and click events
  GPIO.setup(pin_rot_V_dt, GPIO.IN)
  GPIO.setup(pin_rot_V_ck, GPIO.IN)
  GPIO.setup(pin_color_left, GPIO.IN, pull_up_down = GPIO.PUD_UP)
  GPIO.add_event_detect(pin_rot_V_dt, GPIO.FALLING, callback=lambda self:RotaryEnc_Move_Cursor(self, GPIO.input(pin_rot_V_ck), "vertical"))
  GPIO.add_event_detect(pin_color_left, GPIO.FALLING, callback=Change_Color_Left, bouncetime=200)
  
  #Horizontal Rotary Encoder - Set up rotate and click events
  GPIO.setup(pin_rot_H_dt, GPIO.IN)
  GPIO.setup(pin_rot_H_ck, GPIO.IN)
  GPIO.setup(pin_color_right, GPIO.IN, pull_up_down = GPIO.PUD_UP)
  GPIO.add_event_detect(pin_rot_H_dt, GPIO.FALLING, callback=lambda self:RotaryEnc_Move_Cursor(self, GPIO.input(pin_rot_H_ck), "horizontal"))
  GPIO.add_event_detect(pin_color_right, GPIO.FALLING, callback=Change_Color_Right, bouncetime=200)
  
  #Buttons - Set up clear screen and quit
  GPIO.setup(pin_quit, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
  GPIO.setup(pin_clear_screen, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
  GPIO.add_event_detect(pin_quit, GPIO.RISING, callback=Quit, bouncetime=200)
  GPIO.add_event_detect(pin_clear_screen, GPIO.RISING, callback=Clear_Screen, bouncetime=200)

#Open the window
window.mainloop()
#************ END - MAIN ************#