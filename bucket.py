#!/usr/bin/env python3

import sys
import argparse
from math import ceil, floor
from statistics import mean, stdev
from functools import reduce

def reducer(low, high, interval, buckets):
    def f(acc, x):
        i = min(int((x - low) / interval), buckets)
        acc[i] = acc.get(i, 0) + 1
        return acc
    return f

def display_stats(ns):
    print('mean:', mean(ns))
    print('standard deviation:', stdev(ns))

def display_results(n, low, interval, buckets, bucketed):
    for i in range(int(buckets) + 1):
        lower = i * interval + low
        count = bucketed.get(i, 0)

        if i < buckets:
            print('{}-{}\t{}\t{}%'.format(lower, lower + interval, count, round(count / n * 100, 1)))
        else:
            print('rest\t{}\t{}%'.format(count, round(count / n * 100, 1)))

def main(ns, stats, target_buckets=10, interval=None, start=None, stop=None):
    n = float(len(ns))
    low = start or floor(min(ns))
    high = stop or ceil(max(ns))
    interval = interval or round((high - low) / (target_buckets - 1))
    buckets = round((high - low) / interval)
    print('buckets', buckets, interval)
    bucketed = reduce(reducer(low, high, interval, buckets), ns, {})

    display_results(n, low, interval, buckets, bucketed)
    stats == 'on' and display_stats(ns)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--buckets', type=int, default=10, help='Number of buckets')
    parser.add_argument('--interval', type=int, help='Size of buckets; overrides number')
    parser.add_argument('--start', type=int, help='Range start')
    parser.add_argument('--stop', type=int, help='Range stop')
    parser.add_argument('--stats', type=str, default='on', help='Display stats')
    args = parser.parse_args()

    ns = [float(line.strip()) for line in sys.stdin.readlines()]

    main(ns, args.stats, args.buckets, args.interval, args.start, args.stop)
