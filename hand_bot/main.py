from time import sleep
import Adafruit_LSM303
import numpy as np
import csv
import os
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt

# Create a LSM303 instance.
lsm303 = Adafruit_LSM303.LSM303()

#find magnitude of acceleration vector
def magnitude(current,previous):
    distance = 0
    for i in range(len(current)):
        distance += (current[i]-previous[i])**2
    return distance**0.5

#load data
movement_data = pd.read_csv("~/Documents/covid_hand_bot/data_collector/Movement_data.csv")
movement_labels = pd.read_csv("~/Documents/covid_hand_bot/data_collector/Movement_labels.csv")
#train_data,val_data,train_labels,val_labels = train_test_split(movement_data,movement_labels,test_size = 0.2,random_state = 70)

#train model
classifier = KNeighborsClassifier(n_neighbors = 5)
classifier.fit(movement_data,movement_labels)


previous_accel = [0,0,0]
previous_mag = 0
movement_array = []
movement_tolerance = 180
while True:
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
                average_movement = [average_movement]
                #print(average_movement)
            #predict data
            print(classifier.predict(average_movement))
            #clear movement array for next move
            movement_array = []
            
        previous_accel = accel
        previous_mag = total_magnitude
        sleep(0.1)
        
    sleep(0.01)

