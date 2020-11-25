import csv

def createCSVfromBounds(name, bounds):

    with open(name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(bounds)