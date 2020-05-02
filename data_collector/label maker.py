import csv

file = open("no_touch_face.csv")
reader = csv.reader(file)
length = len(list(reader))

with open("no_touch_face_labels.csv",mode='a+') as movement_data:
    writer = csv.writer(movement_data,delimiter=',')
    #storing data from average_movement into csv
    for i in range(length):
        writer.writerow(["0"])
    movement_data.close()
