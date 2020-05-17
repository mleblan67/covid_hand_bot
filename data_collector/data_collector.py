from time import sleep
import Adafruit_LSM303
import numpy as np
import RPi.GPIO as GPIO
import csv
import os
from datetime import datetime
#setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#pin 20 for button
GPIO.setup(20,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# Create a LSM303 instance.
lsm303 = Adafruit_LSM303.LSM303()

#csv data
file_name = "Movement_data.csv"
#Label for data
#Change to 1 if touched and 0 if not touched
touched = 0

#find magnitude of acceleration vector
def magnitude(current,previous):
    distance = 0
    for i in range(len(current)):
        distance += (current[i]-previous[i])**2
    return distance**0.5

previous_accel = [0,0,0]
previous_mag = 0
movement_array = []
movement_tolerance = 180
while True:
    if GPIO.input(20) == GPIO.LOW:
        # Read the X, Y, Z axis acceleration values and print them.
        accel, mag = lsm303.read()
        accel,mag = list(accel),list(mag)
        total_magnitude = magnitude(accel,previous_accel)
        #print(total_magnitude)
        if total_magnitude > movement_tolerance:
            #when there is important hand movement
            if total_magnitude > previous_mag-50:
                #when the hand is accelerating
                #print("Moved")
                movement_array.append(accel+mag)
            else:
                #print(movement_array)
                if len(movement_array) > 0:
                    #take average of movement
                    average_movement = np.average(movement_array, axis=0)
                    print(average_movement)
                #save data
                with open(file_name,mode='a+') as movement_data:
                    writer = csv.writer(movement_data,delimiter=',')
                    #storing data from average_movement into csv
                    writer.writerow([str(average_movement[0]),str(average_movement[1]),str(average_movement[2]),str(average_movement[3]),str(average_movement[4]),str(average_movement[5]),str(touched)])
                    movement_data.close()
                print("Saved")
                #clear movement array for next move
                movement_array = []
            
        previous_accel = accel
        previous_mag = total_magnitude
        sleep(0.1)
        
    sleep(0.01)
