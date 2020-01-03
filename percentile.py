import pandas as pd

import sys
import csv

adjust_keys = False
try:
    filename = str(sys.argv[1])
    fromblock = int(sys.argv[2])
    toblock = int(sys.argv[3])
    if len(sys.argv) == 5 and sys.argv[4] == 'adjust':
        adjust_keys = True
except:
    print "usage: python percentile.py <filename> <fromblock> <toblock> [adjust]"
    exit(1)

series = {}
with open(filename, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        line_count += 1

        if int(row['BlockNumber']) < fromblock:
            continue

        for k, v in row.iteritems():
            if not k in series:
                series[k] = []

            if adjust_keys:
                if k == 'LeafKeysSize':
                    v = int(v) / 8
                if k == 'BlockWitnessSize':
                    leafKeySizeOriginal = int(row['LeafKeysSize'])
                    leafKeySizeAdjusted = int(leafKeySizeOriginal / 8)
                    v = int(v) - leafKeySizeOriginal + leafKeySizeAdjusted

            series[k].append(int(v))
        if int(row['BlockNumber']) > toblock:
            break


        if line_count % 100000 == 0:
            print "processed", line_count, "rows"


df = pd.DataFrame(series)
print df

print "mean", df.BlockWitnessSize.mean()
print "median", df.BlockWitnessSize.median()
print "percentile 90th", df.BlockWitnessSize.quantile(0.9)
print "percentile 95th", df.BlockWitnessSize.quantile(0.95)
print "percentile 99th", df.BlockWitnessSize.quantile(0.99)
print "percentile 100th", df.BlockWitnessSize.quantile(1.0)
