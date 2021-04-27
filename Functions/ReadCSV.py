import csv

def datainput(array):
    datafile = open('File Name Here','r')
    datareader = csv.reader(datafile, delimiter=',')
    for row in datareader:
        array.append(row)