from time import sleep
import Adafruit_LSM303
import numpy as np
import RPi.GPIO as GPIO
import csv
#setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#pin 20 for button
GPIO.setup(20,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# Create a LSM303 instance.
lsm303 = Adafruit_LSM303.LSM303()

#csv info
file_name = "fill in"

#find magnitude of acceleration vector
def magnitude(current,previous):
    distance = 0
    for i in range(len(current)):
        distance += (current[i]-previous[i])**2
    return distance**0.5

previous_accel = [0,0,0]
movement_array = []
movement_tolerance = 180
while True:
    if GPIO.input(20) == GPIO.LOW:
        # Read the X, Y, Z axis acceleration values and print them.
        accel, mag = lsm303.read()
        accel,mag = list(accel),list(mag)
        total_magnitude = magnitude(accel,previous_accel)
        
        if total_magnitude > movement_tolerance:
            #when there is important hand movement
            #print("MOVED! \t X:%s Y:%s Z:%s \t Xmag:%s Ymag:%s Zmag:%s"%(accel_x,accel_y,accel_z,mag_x,mag_y,mag_z))
            movement_array.append(accel+mag)
        else:
            #print(movement_array)
            if len(movement_array) > 0:
                #take average of movement
                average_movement = np.average(movement_array, axis=0)
            print(average_movement)
            #save data
            with open(file_name,mode='w') as movement_data:
                writer = csv.writer(movement_data,delimiter=',')
                #storing data from average_movement into csv
                for ax,ay,az,mx,my,mz in average_movement:
                    writer.writerow([str(ax),str(ay),str(az),str(mx),str(my),str(mz)])
                movement_data.close()
            #clear movement array for next move
            movement_array = []
            
        previous_accel = accel
        sleep(0.1)
        
    sleep(0.1)
