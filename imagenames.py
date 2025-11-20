import os
import csv

path = r"/Users/momuychayis/Documents/Python courses/Ventas_casa/images"
csv_filename = "imagenames.csv"
images = []
for dirpath, dirnames, filenames in os.walk(path):
    for filename in filenames:
        images.append(filename)

with open(csv_filename, "w", newline="") as file:
    writer = csv.writer(file)
    for image in images:
        writer.writerow([image])
