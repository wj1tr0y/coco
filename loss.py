from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
import argparse

def smooth(X, Y, weight=0.85):
    scalar = Y
    last = scalar[0]
    smoothed = []
    for point in scalar:
        smoothed_val = last * weight + (1 - weight) * point
        smoothed.append(smoothed_val)
        last = smoothed_val
    plt.plot(X, smoothed, 'r-')
    
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Plot the loss curve of caffe trian log file.")
    parser.add_argument("--log",
            help="Path of your log file.", required=True)
    parser.add_argument("--weight",
        help = "Smooth weight.", required=True)
    args = parser.parse_args()
    weight = float(args.weight)
    if not os.path.exists(args.log):
        print("{} doesn't exist.".format(args.log))
    X = []
    Y = []
    with open(args.log, 'r') as f:
        for line in f.readlines():
            if 'Iteration' in line and 'loss' in line:
                line = line.split(' ')
                x = line[line.index('Iteration') + 1][0: -1]
                y = line[line.index('loss')+ 2]
                X.append(int(x))
                Y.append(float(y))
    plt.plot(X, Y,'r-',alpha=0.2)
    plt.title('{} Loss Curve'.format(args.log[:-4]))
    smooth(X, Y, weight=weight)

