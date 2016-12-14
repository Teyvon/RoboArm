# -*- coding: utf-8 -*-
"""
Created on Mon Dec 05 14:42:55 2016

@author: drumm
""" 
import pyb
from pyb import Pin, UART, LED
from motor_driver import start, move_motor
import time



#uart = UART(1, 9600)                         # init with given baudrate
#uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters

global leds 

print("hey you tell main(on,run) what to do")
def init():
    """
    This function is the inizialization for the mastermind task,
    it allows the board to be initialized for all three motors and LEDs
    powered on for each. If the Blue goes on then all have been initialized
    without any errors.
    """
    #initializes global variables    
    global leds
    
    print ("about to start up motors")
    try:
        state = []    
        print ("hit that startup")
        m1 = start(1) # starts motor 1
        m2 = start(2) # starts motor 1
        m3 = start(3) # starts motor 1
        state = [m1,m2,m3]
    except Exception:
        print ("sad" + str(state))
        #if any error happens print some tears
                
    else: #this checks which motors have successfully been turned on by
          # show of hands from the leds, blue means all good from all 3 motors
        if state[0] == 1:
            LED(1).on()
        if state[1] == 1:
            LED(2).on()
        if state[2] == 1:
            LED(3).on()
        if state.count(1) == 3:
            LED(4).on()
            
            leds = [LED(1),LED(2),LED(3),LED(4)] # init LED list
            print ("you want startz motorz?")
            print ("set inputs to 1: 'main(on,run)'")
            
        else:
            print ("motors on:" + str(state))

def main(on = 0, run = 0): #set tracking to null until user says to start
    # Initializes global variables
    global leds
    if on == 1:
        init()
        on = 0
        time.sleep(2)
        for x in leds:
            x.off()
            print ("turned led", str(x), "off")
        
    else:
        print ("tell tracking to start")
    
    if run == 2:
        """
        Runs an accelerometer in y function, stops on switch press
        """
        switch = pyb.Switch()
        leds = [pyb.LED(i+1) for i in range(4)]
        accel = pyb.Accel()
        
        i = 0
        while not switch():
            y = accel.y()
            i = (i + (1 if y > 0 else -1)) % len(leds)
            leds[i].toggle()
            pyb.delay(10 * max(1, 20 - abs(y)))
        
        print ("that was fun wasn't it?")
        print ("what now...")
        
    if run == 1:
        """
        Runs the document parser to read from the csv file
        """
        try:
            import parse_mod
            print ("about to parse")
            
        except ImportError:
            print ("Show me your passport sir?")
        
        else:
            [t,x,y,z] = parse_mod.p()
            print ("done parsing")  #+ str(x) + str(y) + str(z)
            print ("all your data are belong to us...Praise the robo-overlords")
            move_motor(t,x,y,z,mode = 1) # Set the mode for either: 0=sequential,1=multitasking
            print ("you should have moved")
                    
# rawinput for prompts and blocking
# usb_vcp -> usb.any()



#    return(Pin.phase_a1())







