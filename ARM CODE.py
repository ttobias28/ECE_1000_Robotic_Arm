# This code was written by Teagan Tobias
# Email: ttobias42@tntech.edu
# ECE 1000 Explorations in ECE Final Project
# Professor: Dr. Bhattacharya
# Joystick Controlled Robot Arm

# reference used to learn basic codes for servos/PWM - https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf
# reference used to learn other basic codes for servo control - https://randomnerdtutorials.com/raspberry-pi-pico-servo-motor-micropython/
# reference used to understand functions necessary for arm movement - https://www.instructables.com/DIY-Robotic-Arm-Snake-Game-With-Raspberry-Pi-Pico-/
# reference used to wire and code joystick - https://www.tomshardware.com/how-to/raspberry-pi-pico-joystick
# used ChatGPT as refrence for lines 46-48 (how to convert angle to duty)

# imports required
import machine
import time
from machine import Pin, PWM, ADC
from time import sleep

# set up joystick
joy_x = ADC(26)
joy_y = ADC(27)
joy_btn = Pin(28, Pin.IN, Pin.PULL_UP)

# set up servos 1-4
servo1_pin = machine.Pin(0)
servo1 = PWM(servo1_pin)

servo2_pin = machine.Pin(1)
servo2 = PWM(servo2_pin)

servo3_pin = machine.Pin(2)
servo3 = PWM(servo3_pin)

servo4_pin = machine.Pin(3)
servo4 = PWM(servo4_pin)

# set PWM frequency for servos
servo1.freq(50)
servo2.freq(50)
servo3.freq(50)
servo4.freq(50)

# initial servo positions
positions = [90, 90, 90, 90]

# convert angle in degrees to PWM duty cycle value
def angle_to_duty(angle):
    return int(2000 + (angle/180) * 8000)

# updates position of whichever servo. servo is the PWM object, index is servo motor index, value is change in position
def update_servo(servo, index, value):
    positions[index] = min(max(positions[index] + value, 0), 180)
    servo.duty_u16(angle_to_duty(positions[index]))

while True:
    # read joystick
    x_val = joy_x.read_u16()
    y_val = joy_y.read_u16()
    btn_val = joy_btn.value()
    
    # base rotation controlled by x-axis
    if x_val > 40000:
        update_servo(servo1, 0, 5)
    elif x_val < 20000:
        update_servo(servo1, 0, -5)
        
    # vertical movement controlled by y-axis
    if y_val > 40000:
        update_servo(servo2, 1, 5)
        update_servo(servo3, 2, 5)
    elif y_val < 20000:
        update_servo(servo2, 1, -5)
        update_servo(servo3, 2, -5)
    
    # claw/whatever at end controlled by button
    if btn_val == 0:
        update_servo(servo4, 3, 5)
    else:
        update_servo(servo4, 3, -5)

# prevent overload
sleep(0.1)