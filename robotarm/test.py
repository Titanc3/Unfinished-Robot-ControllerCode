import network
import espnow
import machine

#init components, keep them disabled though
pCloseClaw = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP) # spin base clockwise
pOpenClaw = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP) # spin base counterclockwise

pBaseCW = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP) # open claw
pBaseCCW = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP) # close claw

pLowerPWR = machine.Pin(21, machine.Pin.OUT) # init bottom servo
pLowerPWR.value(1) # applies to a pnp, so it's disabled
pLowerPWM = machine.PWM(22, freq=50)
lowerPos = 0

pUpperPWR = machine.Pin(23, machine.Pin.OUT) # init top servo
pUpperPWR.value(1)
pUpperPWM = machine.PWM(25, freq=50)
upperPos = 0


pLowerPWR.value(0)

while 1:
    pass