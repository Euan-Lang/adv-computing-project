import csv
def dataoutput(Data):
    datafile = open('File Name','w')
    dataWriter = csv.writer(datafile, delimiter=',')
    dataWriter.writerows(Data)