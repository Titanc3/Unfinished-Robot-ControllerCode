import machine
from machine import Pin

import network # also for e-e comms
import espnow # esp-esp comms
import time

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.WLAN.IF_STA)  # Or network.WLAN.IF_AP
sta.active(True)
sta.disconnect()      # For ESP8266

e = espnow.ESPNow() # prepare wireless comms
e.active(True)
peer = b'\xa8B\xe3\x91Qh'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()


def initialize():
    # IO 10&12 binary counting
    # up to 4 arm ids
    # poll input pin first, then check arm part id
    
    # blue-4
    # green-5
    # red-6 (dim)
    # 0=led on
    
    global pRed
    global pGreen
    global pBlue
    global pOut
    global pIn
    global pUp
    global pDown
    global pID1
    global pID2
    
    pRed = Pin(6, Pin.OUT)
    pGreen = Pin(5, Pin.OUT)
    pBlue = Pin(4, Pin.OUT)

    pOut = Pin(18, Pin.OUT) #(15-c1)
    pIn = Pin(17, Pin.IN, Pin.PULL_DOWN) # flipper-dev comms (16-c0)

    pUp = Pin(11, Pin.IN, Pin.PULL_DOWN) # up input (2-a7)
    pDown = Pin(13, Pin.IN, Pin.PULL_DOWN) # down input (3-a6)

    pID1 = Pin(12, Pin.IN, Pin.PULL_DOWN) # binary id (msb - left) 0 or 1 (4-a4)
    pID2 = Pin(10, Pin.IN, Pin.PULL_DOWN) # binary id (lsb - right) 0 or 1 (5-b3)

    pRed.value(1)
    pGreen.value(1)
    pBlue.value(1)
    
    pOut.value(1) # signal that it is waiting
    
    pRed.value(0) # visually show waiting on connection

    while not pIn.value(): # while pIn volt=0
        machine.idle() # wait 1ms
        
    pRed.value(1)
    pOut.value(0) # reset pin, connection ensured


def rgbOff():
    pRed.value(1)
    pGreen.value(1)
    pBlue.value(1)

def pollpInput():
    while not pIn.value(): # while pIn volt=0
        time.sleep(0.5) # wait .5s

initialize()

time.sleep(0.1)

pBlue.value(0)

while 1: # main script
    pBlue.value(0) # show waiting
    print("waiting")
    time.sleep(0.02) # give time for flipper pins to reset
    pollpInput() # wait for data indicator
    rgbOff()
    print("got output")

    binaryID = str(pID1.value())+str(pID2.value()) # create a readable binary string

    print("binaryID: " + binaryID)

    if pUp.value() == 1 and pDown.value() == 1:
        rgbOff()
        break # exit, couldn't be bothered to do it better
    
    pRed.value(0) # msg recieved indicator
    
    if binaryID == "11": # farthest forward part id (dcmotor)
        pOut.value(1) # tell flipper message recieved
        rgbOff()
        pGreen.value(0) # doing instructions
        
        if pUp.value() == 1:
            e.send(peer, b'11 1') # id 11, speed 1
            while pUp.value() == 1:
                pass # avoid sending same msg, wait for change
        if pDown.value() == 1:
            e.send(peer, b'11 -1') # id 11, speed -1
            while pDown.value() == 1:
                pass
            
        e.send(peer, b'11 0') # id 11, speed 0
        pOut.value(0) # reset output
        
    if binaryID == "10": #(servo)
        rgbOff()
        pGreen.value(0) # msg being done
        
        if pUp.value() == 1:
            e.send(peer, b'10 15') # id 10, +15 deg
        else:
            e.send(peer, b'10 -15') # id 10, +15 deg
            
        pOut.value(1) # tell flipper message recieved (specific to servo instructions) //DO NOT PUT THESE IN THE OTHER ORDER
        time.sleep(0.05) # prevent quick repetition of input, exclude yourself from input //DO NOT PUT THESE IN THE OTHER ORDER
        
    elif binaryID == "01": #(servo)
        rgbOff()
        pGreen.value(0) # doing instructions
        
        if pUp.value() == 1:
            e.send(peer, b'01 15')
        else:
            e.send(peer, b'01 -15')
            
        pOut.value(1) # tell flipper message recieved
        time.sleep(0.05) # prevent quick repetition of input, exclude yourself from input
        
    elif binaryID == "00": # farthest back part id (dcmotor)
        pOut.value(1) # tell flipper message recieved
        rgbOff()
        pGreen.value(0) # doing instructions
        
        if pUp.value() == 1:
            e.send(peer, b'00 1')
            while pUp.value() == 1:
                pass
        if pDown.value() == 1:
            e.send(peer, b'00 -1')
            while pDown.value() == 1:
                pass
        e.send(peer, b'00 0')
        pOut.value(0) # reset output
    
    rgbOff()
    pOut.value(0)


