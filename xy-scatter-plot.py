import pandas as pd
import matplotlib.pyplot as plt


import sys
import csv

adjust_keys = False
try:
    filename_hex = str(sys.argv[1])
    filename_bin = str(sys.argv[2])
    fromblock = int(sys.argv[3])
    toblock = int(sys.argv[4])
    if len(sys.argv) == 6 and sys.argv[5] == 'adjust':
        adjust_keys = True
except:
    print "usage: python xy-scatter-plot.py <filename_hex> <filename_bin> <fromblock> <toblock> [adjust]"
    exit(1)

series = {}
with open(filename_hex, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        line_count += 1

        if int(row['BlockNumber']) < fromblock:
            continue
        for k, v in row.iteritems():
            k = k + "_hex"

            if not k in series:
                series[k] = []

            if adjust_keys:
                if k == 'LeafKeysSize_hex':
                    v = int(v) / 2
                if k == 'BlockWitnessSize_hex':
                    leafKeySizeOriginal = int(row['LeafKeysSize'])
                    leafKeySizeAdjusted = int(leafKeySizeOriginal / 2)
                    v = int(v) - leafKeySizeOriginal + leafKeySizeAdjusted

            series[k].append(int(v))
        if int(row['BlockNumber']) > toblock:
            break

        if line_count % 100000 == 0:
            print "processed hex", line_count, "rows"

with open(filename_bin, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        line_count += 1

        if int(row['BlockNumber']) < fromblock:
            continue

        for k, v in row.iteritems():
            k = k + "_bin"

            if not k in series:
                series[k] = []

            if adjust_keys:
                if k == 'LeafKeysSize_bin':
                    v = int(v) / 8
                if k == 'BlockWitnessSize_bin':
                    leafKeySizeOriginal = int(row['LeafKeysSize'])
                    leafKeySizeAdjusted = int(leafKeySizeOriginal / 8)
                    v = int(v) - leafKeySizeOriginal + leafKeySizeAdjusted

            series[k].append(int(v))
        if int(row['BlockNumber']) > toblock:
            break

        if line_count % 100000 == 0:
            print "processed bin", line_count, "rows"


df = pd.DataFrame(series)
print df

plt.ylabel("bin, MB")
plt.xlabel("hex, MB")
plt.xlim(xmax=4)
plt.ylim(ymax=4)
plt.grid(True)
s=[1 for n in range(len(df['BlockWitnessSize_hex']))]
plt.scatter(df['BlockWitnessSize_hex']/1024/1024.0, df['BlockWitnessSize_bin']/1024/1024.0, s=s)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()