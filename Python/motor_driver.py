# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 08:09:47 2016

@author:  Teyvon Brooks and Mel Boonya-ananta

This module has necessary functions to control motor driver 1
"""
import pyb
from pyb import Pin, Timer
import math
import time

def start(motor_num):
    """
    This is the initialization method for the three motor drivers. 
    This should happen every startup, and allows the stepper motors to be ran by the pyboard.
    Inputs: motor_num(1-3)
    Outputs: motor statuses - m1,m2,m3  
    """
    m1 = 0
    m2 = 0
    m3 = 0
    global frq
    frq = 250
    if motor_num == 1:
        try: 
            timer1 = Timer(9, freq=frq) #Initializes timer 9 at 1000hz
            clk1 = timer1.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.X4, pulse_width=0) # clock pulse pwm on pin x4
            global dir1
            dir1 = Pin('X2', Pin.OUT_PP) #init pin x2 as output
            step1 = Pin('X3', Pin.OUT_PP) #init pin x3 as output
            phase_a1 = Pin('X1', Pin.IN) #X1 input
            bias1 = Pin('Y12', Pin.OUT_PP) #Y12 output
            OIC1 = Pin('Y11', Pin.OUT_PP) #Y11 output  
            
            dir1.low() # Function = clockwise LOW
            step1.low() #Function = full step LOW
            bias1.high() #Function = outputs assume a low impedence condition
            
            if (step1 == 1):
    
                OIC1.high() #Function = set ouput impedence control
            elif (step1 == 0):
                OIC1.low() #Function = set ouput impedence control
            m1 = 1
            print ("Motor 1 is good to go")
            return (m1) 
        except:
            pass
        else:
            print ("Motor 1 is no good")
            return(m1)
        
    elif motor_num == 2:
        try:        
            timer2 = Timer(1, freq=frq) #Initializes timer 9 at 1000hz
            clk2 = timer2.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.Y6, pulse_width=0) # clock pulse pwm on pin y6
            global dir2
            dir2 = Pin('X10', Pin.OUT_PP) #init pin x2 as output
            step2 = Pin('Y8', Pin.OUT_PP) #init pin x3 as output
            phase_a2 = Pin('X12', Pin.IN) #X1 input
            bias2 = Pin('Y2', Pin.OUT_PP) #Y12 output
        
            step2.low() #Function = full step LOW
            dir2.low() # Function = clockwise LOW
            bias2.high() #Function = outputs assume a low impedence condition
            
            if (step2 == 1):
                OIC2 = Pin('Y4', Pin.OUT_PP) #Y11 output
                OIC2.low() #Function = set ouput impedence control
            elif (step2 == 0):
                OIC2 = Pin('Y4', Pin.OUT_PP) #Y11 output
                OIC2.high() #Function = set ouput impedence control
            
            m2 = 1
            print ("Motor 2 is good to go")
            return (m2)
        except:
            pass
        else:
            print ("Motor 2 is no good bruh")
            return (m2)
        
    elif motor_num == 3:
        try:        
            timer3 = Timer(12, freq=frq) #Initializes timer 9 at 1000hz
            clk3 = timer3.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.Y7, pulse_width=0) # clock pulse pwm on pin y7
            global dir3
            dir3 = Pin('Y3', Pin.OUT_PP) #init pin x2 as output
            step3 = Pin('Y5', Pin.OUT_PP) #init pin x3 as output
            phase_a3 = Pin('Y1', Pin.IN) #X1 input
            bias3 = Pin('X11', Pin.OUT_PP) #Y12 output
        
            step3.low() #Function = full step LOW
            dir3.low() # Function = clockwise LOW
            bias3.high() #Function = outputs assume a low impedence condition
            
            if (step3 == 1):
                OIC = Pin('Y11', Pin.OUT_PP) #Y11 output
                OIC.low() #Function = set ouput impedence control
            elif (step3 == 0):
                OIC = Pin('Y11', Pin.OUT_PP) #Y11 output
                OIC.high() #Function = set ouput impedence control
    
            m3 = 1
            print ("Motor 3 is good to go")
            return (m3)
        except:
            pass
        else:
            print ("Motor 2 is no good bruh")
            return (m3)
            
            
            

def move_motor(timestep,roll,pitch,yaw, theta_last = 0, phi_last = 0, psi_last = 0, mode = 0):
    """
    This function takes in the euler angles and determines the necessary motor
    output for each motor.
    
    mode 0: This mode fixes the pulse frequency for all motors and calculates
    the individual time increments for each data point
    
    mode 1: This mode fixes/synchronizes the time increments for all motors and 
    allows the angular velocity/frequency to vary so each data point happens "simultaneously"
    for all motors.
    """
    global frq
    if mode == 0: #run each axis separately 
        
        for theta in roll:
            
            steps_x = (theta - theta_last)*(180/math.pi/0.9) #calculating steps to next position
            theta_last = theta
            global dir1
            
            if steps_x < 0:
                dir1.high() #counterclockwise
            else:
                dir1.low() #clockwise
            timex = abs(steps_x)/frq #steps/frequency = time to move in milliseconds
            Timer(9).channel(2,pyb.Timer.PWM, pulse_width_percent = 50)
            #print("zzzzzzz" + str(timex) + "for steps of " + str(steps_x))
            time.sleep(timex)
            Timer(9).channel(2,pyb.Timer.PWM, pulse_width_percent = 0)
            #print("stop!!!!")
            
    
        for phi in pitch:
            steps_y = (phi - phi_last)*(180/math.pi/0.9) #calculating steps to next position
            phi_last = phi
            global dir2
            
            if steps_y < 0:
                dir2.high() #counterclockwise
            else:
                dir2.low() #clockwise        
            timey = abs(steps_y)/frq #steps*frequency = time to move in seconds
            pyb.Timer(1).channel(1,pyb.Timer.PWM, pulse_width_percent = 50)
            time.sleep(timey)
            Timer(1).channel(1,pyb.Timer.PWM, pulse_width_percent = 0)

            
        for psi in yaw:
            steps_z = (psi - psi_last)*(180/math.pi/0.9) #calculating steps to next position
            psi_last = psi
            global dir3
            
            if steps_z < 0:
                dir3.high() #counterclockwise
            else:
                dir3.low() #clockwise        
            timez = abs(steps_z)/frq #steps*frequency = time to move in seconds     
            pyb.Timer(12).channel(1,pyb.Timer.PWM, pulse_width_percent = 50)
            time.sleep(timez)
            Timer(12).channel(1,pyb.Timer.PWM, pulse_width_percent = 0)

            
    if mode == 1: #cooperative multitasking - approved my Dr. Murray ^TM
        global t_inc
        t_inc = 0.01 #set the standard time increments
        t_last = 0
        total = 0
        for i in enumerate(timestep): # This is to find the average timestep increment
            del_t = timestep[0] - t_last
            total = del_t + total
            if i[0] == (len(timestep)-1):
                global t_inc                
                t_inc = total/i[0]
                print(t_inc) 
        print(t_inc) 
        for index,value in enumerate(timestep):
            
            # Start calculating all steps to current data point
            steps_x = (roll[index] - theta_last)*(180/math.pi/0.9) #calculating steps to next position
            theta_last = roll[index]
            if steps_x < 0: #This checks for changes in directions
                dir1.high() #counterclockwise
            else:
                dir1.low() #clockwise            
            
            steps_y = (pitch[index] - phi_last)*(180/math.pi/0.9) #calculating steps to next position
            phi_last = pitch[index]
            if steps_y < 0: #This checks for changes in directions
                dir2.high() #counterclockwise
            else:
                dir2.low() #clockwise
                
            steps_z = (yaw[index] - psi_last)*(180/math.pi/0.9) #calculating steps to next position
            psi_last = yaw[index]
            if steps_z < 0: #This checks for changes in directions
                dir3.high() #counterclockwise
            else:
                dir3.low() #clockwise
            
            # Calculaing the frequency for each motor speed            
            freqx = abs(steps_x)/t_inc
            freqy = abs(steps_y)/t_inc
            freqz = abs(steps_z)/t_inc
            
            # Set the new frequencies and start up the timing channels  - starts all motors
            if freqx == 0:
                pass
            else:
                Timer(9, freq=freqx).channel(2,pyb.Timer.PWM, pulse_width_percent = 50)
            if freqy == 0:
                pass
            else:
                Timer(1, freq=freqy).channel(1,pyb.Timer.PWM, pulse_width_percent = 50)
            if freqz == 0:
                pass
            else:
                Timer(12, freq=freqz).channel(1,pyb.Timer.PWM, pulse_width_percent = 50)
            
            # Delay for length of the time increment
            time.sleep(t_inc)
            
            # Stop all pulses/motors until next loop
            Timer(9).channel(2,pyb.Timer.PWM, pulse_width_percent = 0)  
            Timer(1).channel(1,pyb.Timer.PWM, pulse_width_percent = 0)
            Timer(12).channel(1,pyb.Timer.PWM, pulse_width_percent = 0) 






























               