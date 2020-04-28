from time import sleep
import Adafruit_LSM303
import numpy as np

# Create a LSM303 instance.
lsm303 = Adafruit_LSM303.LSM303()

#find magnitude of acceleration vector
def magnitude(vector):
    distance = 0
    for i in range(len(vector)):
        distance += (vector[i])**2
    return distance**0.5

def single_distance(current,previous):
    distance = [0,0,0]
    for i in range(len(current)):
        distance[i] = current[i] - previous[i]
    return distance

axis = ["X","Y","Z"]
previous_accel = [0,0,0]
#tell if acceleration magnitude is a real movement
movement_tolerance = 180
while True:
    # Read the X, Y, Z axis acceleration values and print them.
    accel, mag = lsm303.read()
    accel,mag = list(accel),list(mag)
    #absolute value to find biggest value
    mag = np.absolute(mag)
    movement = single_distance(accel,previous_accel)
    total_magnitude = magnitude(movement)
    #get rid of noise and unimportant movements
    if total_magnitude > movement_tolerance:
        #print("MOVED! \t X:%s Y:%s Z:%s \t Xmag:%s Ymag:%s Zmag:%s"%(accel_x,accel_y,accel_z,mag_x,mag_y,mag_z))
        #find which side is facing up based on biggest value
        side_up = np.where(mag == np.amax(mag))[0][0]
        direction = np.where(movement == np.amax(movement))[0][0]
        #print(axis[side_up])
        #print(axis[direction])

        
    previous_accel = accel
    sleep(0.2)
