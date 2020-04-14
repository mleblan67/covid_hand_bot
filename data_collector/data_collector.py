from time import sleep
import Adafruit_LSM303

# Create a LSM303 instance.
lsm303 = Adafruit_LSM303.LSM303()

#find magnitude of acceleration vector
def magnitude(current,previous):
    distance = 0
    for i in range(len(current)):
        distance += (current[i] - previous[i])**2
    return distance**0.5

previous_accel = [0,0,0]
#tell if acceleration magnitude is a real movement
movement_tolerance = 17
while True:
    # Read the X, Y, Z axis acceleration values and print them.
    accel, mag = lsm303.read()
    # Grab the X, Y, Z components from accel and mag
    accel_x, accel_y, accel_z = accel
    mag_x, mag_y, mag_z = mag
    movement = magnitude(accel,previous_accel)
    #get rid of noise and unimportant movements
    if movement > movement_tolerance:
        print("MOVED!")

    previous_accel = accel
    sleep(0.1)
