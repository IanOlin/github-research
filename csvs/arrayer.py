import csv
import pandas as pd
import os

def arrayer(path):
    with open(path, "rt") as f: 
        reader = csv.reader(f)
        names = set()
        times = {}
        windows = []
        rownum = 0
        for row in reader:
                newrow = [(i[1:-1],j[:-2]) for i,j in zip(row[1::2], row[2::2])]
                rowdict = dict(newrow)
                names.update([x[0] for x in newrow])
                l=row[0].replace("DateObject[{","").strip("{}]}").replace(",","").replace("}]","").split()
                timestamp=':'.join(l[:3])+'-'+':'.join(l[3:])
                windows.append(timestamp)
                times[timestamp] = rowdict
                rownum += 1

    cols = [[times[k][name] if name in times[k] else ' 0' for name in names ] for k in windows]
    data = pd.DataFrame(cols,columns=list(names),index=windows)
    return data

importpath = "/home/jwb/Documents/Csvs/"
exportpath="/home/jwb/Documents/Stuff/"

for filename in os.listdir(path):
    arrayer(importpath+filename).to_csv(exportpath+filename, encoding='utf-8')
