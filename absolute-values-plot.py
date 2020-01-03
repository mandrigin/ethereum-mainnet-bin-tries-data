import pandas as pd
import matplotlib.pyplot as plt
import numpy


import sys
import csv


def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x.values, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

adjust_keys = False
try:
    filename_hex = str(sys.argv[1])
    filename_bin = str(sys.argv[2])
    fromblock = int(sys.argv[3])
    toblock = int(sys.argv[4])
    if len(sys.argv) == 6 and sys.argv[5] == 'adjust':
        adjust_keys = True
except:
    print "usage: python absolute-values-plot.py <filename_hex> <filename_bin> <fromblock> <toblock> [adjust]"
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

if False:
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

plt.ylabel("MB")
plt.xlabel("block #")
plt.grid(True)

running_mean_size = 1024


plt.plot(
    df['BlockNumber_hex'].values[running_mean_size-1:],
    running_mean(df['BlockWitnessSize_hex']/1024.0/1024.0, running_mean_size),
    label = "hex witness")
plt.plot(
    df['BlockNumber_bin'].values[running_mean_size-1:],
    running_mean(df['BlockWitnessSize_bin']/1024.0/1024.0, running_mean_size),
    label = "bin witness")

#plt.legend()


plt.show()
