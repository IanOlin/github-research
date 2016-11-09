import csv
import pandas as pd
import os

""" Run on linux. Set an import path and an export path to folders.
Will take every file in import directory that is a mathematica generated CSV and
 turn it into a nicely fomatted CSV in Output directory.
"""

importpath = "/home/jwb/Documents/Csvs/"
exportpath="/home/jwb/Documents/Stuff/"

def arrayer(path):
    with open(path, "rt") as f:
        reader = csv.reader(f)
        names = set()
        times = {}
        windows = []
        rownum = 0
        for row in reader:
                newrow = [(i[1:-1],j[:-2]) for i,j in zip(row[1::2], row[2::2])] #Drops the timewindow, and groups the rest of the row into [name, tally]
                rowdict = dict(newrow)
                names.update([x[0] for x in newrow]) #adds each name to a name set
                l=row[0].replace("DateObject[{","").strip("{}]}").replace(",","").replace("}]","").split() #Strips DateObject string
                timestamp=':'.join(l[:3])+'-'+':'.join(l[3:]) #Formats date string
                windows.append(timestamp) #add timestamp to list
                times[timestamp] = rowdict #link results as value in timestamp dict
                rownum += 1

    cols = [[times[k][name] if name in times[k] else ' 0' for name in names ] for k in windows] #put the tally for each name across each timestamp in a nested list of Columns
    data = pd.DataFrame(cols,columns=list(names),index=windows) #Put into dataframe with labels
    return data



for filename in os.listdir(path):
    arrayer(importpath+filename).to_csv(exportpath+filename, encoding='utf-8')
