import network
import espnow
import machine
from time import sleep as s

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

#init components, keep them disabled though
pCloseClaw = machine.Pin(16, machine.Pin.OUT) # spin base clockwise
pCloseClaw.value(0)
pOpenClaw = machine.Pin(17, machine.Pin.OUT) # spin base counterclockwise
pOpenClaw.value(0)

pBaseCW = machine.Pin(18, machine.Pin.OUT) # open claw
pBaseCW.value(0)
pBaseCCW = machine.Pin(19, machine.Pin.OUT) # close claw
pBaseCCW.value(0)

pLowerPWR = machine.Pin(21, machine.Pin.OUT) # init bottom servo
pLowerPWR.value(1) # applies to a pnp, so it's disabled
pLowerPWM = machine.PWM(22, freq=50, duty_u16=4915)
lowerPos = 90

pUpperPWR = machine.Pin(23, machine.Pin.OUT) # init top servo
pUpperPWR.value(1)
pUpperPWM = machine.PWM(25, freq=50, duty_u16=4915)
upperPos = 90

def angleToPos(deg):
    return int(1802+(deg/180*6062)) # turn deg to u16 pwm duty

def setServo(bid, ctrl):
    global lowerPos
    global upperPos
    if bid == "01":
        upperPos += int(ctrl)
        pUpperPWR.value(0)
        pUpperPWM.duty_u16(angleToPos(upperPos))
        print(upperPos)
        print(angleToPos(upperPos))
    else: # bid 10
        lowerPos += int(ctrl)
        pLowerPWR.value(0)
        pLowerPWM.duty_u16(angleToPos(lowerPos))
        print(lowerPos)
        print(angleToPos(lowerPos))
    s(2)
    pLowerPWR.value(1)
    pUpperPWR.value(1)
            
def setMotor(bid, ctrl):
    if bid == "00": 
        if int(ctrl) == 1:
            pOpenClaw.value(0)
            pCloseClaw.value(1)
        else: # ctrl = -1
            pCloseClaw.value(0)
            pOpenClaw.value(1)

    else: # bid 11
        if int(ctrl) == 1:
            pBaseCCW.value(0)
            pBaseCW.value(1)
        else: # ctrl = -1
            pBaseCW.value(0)
            pBaseCCW.value(1)
            
while True:
    _, msg = esp.recv()
    if msg:             # msg == None if timeout in recv()
        msg = msg.decode().split(" ")
        print(msg)
        binaryID = msg[0]
        cmd = msg[1]
        
        if cmd == "0": # reset command, resets all instead of laced through functions
            pOpenClaw.value(0)
            pCloseClaw.value(0)
            
            pBaseCCW.value(0)
            pBaseCW.value(0)

        
        elif binaryID == "00" or binaryID == "11": # claw/base
            setMotor(binaryID, cmd)
        else: # linkages
            setServo(binaryID, cmd)
            
        