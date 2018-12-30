#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
__author__ = "Andrey Afanasyev"
__copyright__ = "Copyright 2018, TCP-ZC-NFS"
__license__ = "MIT"
__version__ = "0.0.2"
__email__ = "aafanasyev@os3.nl"
__status__ = "Prototype"

import os
import csv
import matplotlib as mpl
# to work around $DISPLAY error in terminal moder
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.ticker as tck
from matplotlib.ticker import FormatStrFormatter
import numpy as np

path_csv = 'csv/4.19.11-041911-generic-NFS.csv'

x_axis_groups = []
y_axis_values = []
csv_data =[]


with open(path_csv, 'r', encoding='utf-8') as results:
    reader = csv.reader(results, delimiter = ',')
    for row in enumerate(reader):
        if row[0] == 0:
            # group
            x_label = str(row[1][2])
            # values
            y_label = str(row[1][4])
        else:
            csv_data.append((row[1][2], row[1][4]))
print ("Blocksizes by x axis: {}".format(x_label))
print ("Values by y axis: {}".format(y_label))
#print (csv_data)

# separate items from first column
x_data_set=sorted(list(set([rows[0] for rows in csv_data])), key=int)
print(x_data_set)

#Enumerate first column items, add those elements in to y_data and 
#add empty list. Check if element from first column has a related data from 
#second column add this data as float in empty list from of the y_data
y_data = []
for i, element in enumerate(x_data_set):
    y_data.append([element])
    y_data[i].append([])
    #print(y_data[i])
    #print(y_data)
    for j in csv_data:
        #print(j)
        if element == j[0]:
            y_data[i][1].append(round(float(j[1]),3))

y_data_set = [y_data[item][1] for item, element in enumerate(x_data_set)]
#print(y_data_set)

# grid configuration and axes
f = lambda x,pos: str(x).rstrip('0').rstrip('.')
plt.gca().yaxis.grid(color='b', linestyle='--', linewidth=1, alpha=0.1)
plt.gca().yaxis.set_major_locator(plt.MaxNLocator(20))

plt.xlabel(x_label)
plt.ylabel(y_label)

bp = plt.boxplot(x = y_data_set,labels = x_data_set, widths = None, showmeans=True,
    whiskerprops=dict(markerfacecolor='black', markeredgecolor='black', markersize=1, linestyle=':'), 
    capprops=dict(markerfacecolor='black', markeredgecolor='black', markersize=1, linestyle='-'),
    boxprops=dict(color='blue', markersize=1, linestyle='-'),
    medianprops=dict(markerfacecolor='red', markeredgecolor=None, markersize=1, linestyle='-'),
    flierprops = dict(marker='o', markerfacecolor='white', markeredgecolor='black', markersize=1), 
    meanprops=dict(marker='D', markeredgecolor='green', markersize=4))

#set color of boxplot element and display related number.

for element in [key for key, value in bp.items()]:
        if element=='whiskers':
            pass
        elif element=='caps':
            pass
        elif element=='boxes':
            #plt.setp(bp[element], color='blue')
            for line in bp[element]:
                x, y = line.get_xydata()[0] # bottom of left line
                plt.text(x-0.12,y, round((x, y)[1],3), fontdict = {'color':'blue', 'style':'normal', 'weight': 'normal', 'size': 6,},
                        horizontalalignment='center', # centered
                        verticalalignment='top')      # below
                x, y = line.get_xydata()[3] # bottom of right line
                plt.text(x-0.12,y+0.1, round((x, y)[1],3), fontdict = {'color':'blue', 'style':'normal', 'weight': 'normal', 'size': 6,},
                        horizontalalignment='center', # centered
                        verticalalignment='top')  # below
        elif element=='medians':
            #plt.setp(bp[element], color='red')
            for line in bp[element]:
                # get position data for median line
                x, y = line.get_xydata()[1] # top of median line
                # overlay median value
                plt.text(x+0.12, y, round((x, y)[1],3), fontdict = {'color':'red', 'style':'normal', 'weight': 'normal', 'size': 6,},
                        horizontalalignment='center', verticalalignment='top') # draw above, centered
        elif element=='fliers':
            pass
        elif element=='means':
            #plt.setp(bp[element], color='green')
            for line in bp[element]:
                x,y = line.get_xydata()[0]
                plt.text(x+0.35, y+0.05, round((x, y)[1],3), fontdict = {'color':'green', 'style':'italic', 'weight': 'normal', 'size': 6,},
                        horizontalalignment='center', verticalalignment='center')
        else:
            pass


#convert (x(4) y(999)) list to (x(999) y(4))
#for np array

l = []
for i in range (len(y_data_set[0])):
    l.append([])

for i in range(len(x_data_set)):
    #print(y_data_set[i])
    for j in range(len(y_data_set[i])):
        l[j].append(y_data_set[i][j])

#print(l)
y_arr = np.array(l)

print (np.amax(y_arr), np.percentile(y_arr, 50), np.mean(y_arr), np.median(y_arr), np.percentile(y_arr, 25), np.amin(y_arr), np.std(y_arr))
plt.errorbar([i+1 for i,e in enumerate(x_data_set)], np.mean(y_arr, axis=0), yerr=np.std(y_arr, axis=0), color='green', linestyle='-', linewidth=1, alpha=0.50)



median = mlines.Line2D([], [], color='red', markersize=4, label='Median number', linestyle='-')
mean = mlines.Line2D([], [], marker='D', color='green', markersize=4, label='Mean ($μ$) $number$', linestyle = 'None')
boxes = mlines.Line2D([], [], marker='s', markerfacecolor='white', markeredgecolor='blue', markersize=4, label='$_{lower/first} or ^{upper/third} quartiles}$', linestyle = 'None')
meanstd = mlines.Line2D([], [], color='green', label='Standard deviation($σ$)', linestyle='-', linewidth=1, alpha=0.5)

plt.title('Comparison of blocksize (bytes) and write speed (bytes/second) of NFSv4.2 protocol with TCP zero copy. \n 1000 rounds per blocksize', 
            fontsize=8, fontweight='bold')
plt.legend(handles=[median, mean, boxes, meanstd], fontsize=7)

plt.savefig(str('4.19.11-write.png'), format='png', dpi=300)
