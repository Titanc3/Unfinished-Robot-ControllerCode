import flipperzero as f0 # this is a trimmed down version of a script with cooler sprites
import time # needed to limit memory usage

# enabling >3 pins disables buttons in exchange, input buttons changed
f0.gpio_init_pin(f0.GPIO_PIN_PC0, f0.GPIO_MODE_OUTPUT_PUSH_PULL) # output comms
f0.gpio_init_pin(f0.GPIO_PIN_PC1, f0.GPIO_MODE_INPUT, f0.GPIO_PULL_DOWN) # input comms

f0.gpio_init_pin(f0.GPIO_PIN_PA7, f0.GPIO_MODE_OUTPUT_PUSH_PULL) # up output
f0.gpio_init_pin(f0.GPIO_PIN_PA6, f0.GPIO_MODE_OUTPUT_PUSH_PULL) # down output

f0.gpio_init_pin(f0.GPIO_PIN_PA4, f0.GPIO_MODE_OUTPUT_PUSH_PULL) # pinID msd output
f0.gpio_init_pin(f0.GPIO_PIN_PB3, f0.GPIO_MODE_OUTPUT_PUSH_PULL) # pinID lsd output


m_exit = False

techIndex = 1

inputUp = True #just means that the arrow for that input is on,
inputDown = True #doesn't mean that there is input, except if only one is on

@f0.on_input
def input_handler(button, type):
  global m_exit
  global techIndex
  global inputUp
  global inputDown


  if button == f0.INPUT_BUTTON_BACK and type == f0.INPUT_TYPE_LONG:
      m_exit = True
      
  elif button == f0.INPUT_BUTTON_LEFT:
    inputDown = True
    inputUp = False

      
  elif button == f0.INPUT_BUTTON_RIGHT:
    inputDown = False
    inputUp = True

      
  elif button == f0.INPUT_BUTTON_UP:
    if type == f0.INPUT_TYPE_SHORT:
        techIndex+=1
        if techIndex == 5:
          techIndex = 1
    elif type == f0.INPUT_TYPE_LONG:
        techIndex-=1
        if techIndex == 0:
          techIndex = 4
      
      
  if type == f0.INPUT_TYPE_RELEASE:
    inputUp = True
    inputDown = True


def draw_line(x1, y1, x2, y2): # change origin to 1,1
    f0.canvas_draw_line(x1-1, y1-1, x2-1, y2-1)
    
def draw_frame(x1, y1, x2, y2): # change origin to 1,1
    f0.canvas_draw_frame(x1-1, y1-1, x2-1, y2-1)

def draw_box(x1, y1, x2, y2): # change origin to 1,1
    f0.canvas_draw_box(x1-1, y1-1, x2-1, y2-1)

def draw_dot(x, y): # change origin to 1,1
    f0.canvas_draw_dot(x-1, y-1)

def draw_circle(x, y, r): # change origin to 1,1
    f0.canvas_draw_circle(x-1, y-1, r)

def resetLED():
    f0.light_set(f0.LIGHT_GREEN, 0)
    f0.light_set(f0.LIGHT_RED, 0)
    f0.light_set(f0.LIGHT_BLUE, 0)

def draw_arrow(x, y, up):
    if up:
      draw_line(x+2, y, x, y+2)
      draw_line(x+3, y, x+5, y+2)
    else:
      draw_line(x+2, y+5, x, y+3)
      draw_line(x+3, y+5, x+5, y+3)

def draw_bg():
    draw_frame(5, 1, 121, 65)
    for y in range(1, 33): # create dotted lines
        draw_dot(6, y*2-1)# account for offset
        draw_dot(35, y*2)
        draw_dot(64, y*2)
        draw_dot(65, y*2-1)
        draw_dot(94, y*2)
        draw_dot(123, y*2-1)
    
def draw_arm():
    #back
    draw_line(108, 23, 108, 42)
    draw_line(109, 23, 109, 42)
    
    #staff
    draw_line(107, 32, 82, 32)
    draw_line(107, 33, 82, 33)
    
    #extension1
    draw_line(81, 32, 50, 18)
    draw_line(81, 33, 50, 19)
    
    #extension2
    draw_line(49, 19, 28, 33)
    draw_line(49, 20, 28, 34)
    
    #grabber
    draw_line(16, 36, 21, 29)# left segment
    draw_line(16, 37, 21, 30)
    
    draw_line(21, 29, 31, 37) # middle segment
    draw_line(21, 30, 30, 37)
    
    draw_line(31, 37, 24, 42) # right segment
    draw_line(30, 37, 23, 42)
    
    draw_dot(27, 33) # fill in hole
    

def draw_data(index, arrowUp, arrowDown): # index: 1-4
    if index == 1: # claw
        draw_line(6, 2, 6, 63)
        draw_line(35, 2, 35, 63) # "highlight" selection

        draw_circle(23, 36, 10)
        x=18
            
    elif index == 2:
        draw_line(35, 2, 35, 63)
        draw_line(64, 2, 64, 63) # "highlight" selection
        
        draw_circle(51, 19, 3)
        x=47
        
    elif index == 3:
        draw_line(65, 2, 65, 63)
        draw_line(94, 2, 94, 63) # "highlight" selection
        
        draw_circle(80, 32, 4)
        x=77
        
    else: #index == 4
        draw_line(94, 2, 94, 63)
        draw_line(123, 2, 123, 63) # "highlight" selection
        
        draw_circle(108, 32, 13)
        x=106
        
    if arrowUp:
        draw_arrow(x, 8, True)
    if arrowDown:
        draw_arrow(x, 52, False)

while not m_exit and f0.gpio_get_pin(f0.GPIO_PIN_PC1) == False: # check for devboard
  time.sleep(0.1)


f0.vibro_set(True)
f0.light_blink_start(f0.LIGHT_GREEN, 150, 100, 200)
time.sleep(0.5)
f0.vibro_set(False)
f0.light_blink_stop()

time.sleep(3) # account for time devboard takes to initialize

f0.gpio_set_pin(f0.GPIO_PIN_PC0, True) # tell devboard flipper exists
time.sleep(0.1)
f0.gpio_set_pin(f0.GPIO_PIN_PC0, False)
  
while not m_exit:
    f0.canvas_clear()
    draw_bg()
    draw_arm()
    draw_data(techIndex, inputUp, inputDown)
    if inputUp != inputDown: # if there's actually input
        f0.gpio_set_pin(f0.GPIO_PIN_PA7, inputUp) # set inputs first
        f0.gpio_set_pin(f0.GPIO_PIN_PA6, inputDown)
      
      
        if techIndex == 2 or techIndex == 3:# check for servo vs motor (servos)
            binaryID = "01"
            if techIndex == 3:
                binaryID = "10"
              
            f0.gpio_set_pin(f0.GPIO_PIN_PA4, bool(int(binaryID[0]))) # convert ids to pin outputs
            f0.gpio_set_pin(f0.GPIO_PIN_PB3, bool(int(binaryID[1])))
          
            f0.gpio_set_pin(f0.GPIO_PIN_PC0, True) # report info
          
            while not m_exit and f0.gpio_get_pin(f0.GPIO_PIN_PC1) == False: # check for devboard response
                time.sleep_ms(10)
          
          
        else: # (motors)
            binaryID = "00"
            if techIndex == 4:
                binaryID = "11"
              
            f0.gpio_set_pin(f0.GPIO_PIN_PA4, bool(int(binaryID[0]))) # convert ids to pin outputs
            f0.gpio_set_pin(f0.GPIO_PIN_PB3, bool(int(binaryID[1])))
          
            f0.gpio_set_pin(f0.GPIO_PIN_PC0, True) # report info
              
            while inputUp != inputDown: # while button being held, keep doing nothing
                time.sleep_ms(10)
            
    f0.gpio_set_pin(f0.GPIO_PIN_PC0, False) # reset pins
    f0.gpio_set_pin(f0.GPIO_PIN_PA4, False)
    f0.gpio_set_pin(f0.GPIO_PIN_PB3, False)
    f0.gpio_set_pin(f0.GPIO_PIN_PA7, False)
    f0.gpio_set_pin(f0.GPIO_PIN_PA6, False)
            
    f0.canvas_update()
    time.sleep_ms(15)
  
f0.gpio_set_pin(f0.GPIO_PIN_PC0, True)#tell devboard info incoming

f0.gpio_set_pin(f0.GPIO_PIN_PA7, True)#set input up & down positive, tell board to end
f0.gpio_set_pin(f0.GPIO_PIN_PA6, True)

time.sleep(0.5) # ensure devboard gets info