from tqdm import tqdm
import argparse
import datetime
import time
import copy

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plotLong(): #Plotting messages/day vs day)
    print("OK, now generating a long graph.")
    plotLongArray = copy.copy(processedArray) #A bit inefficient but it'll do.
    with tqdm(leave=True, unit=' messages', total=lineNumber, desc="Preparing") as counter:
        for line in plotLongArray:
            line[0] = datetime.date.fromtimestamp(line[0])
            counter.update(1)
    for row in plotLongArray:
        del row[1]
    print("Now crunching numbers...")
    plotLongDateString2 = [item for sublist in plotLongArray for item in sublist]
    plotLongCount = [[x,plotLongDateString2.count(x)] for x in set(plotLongDateString2)]
    r = np.asarray(plotLongCount)
    r = r[r[:,0].argsort()]
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    yearsFmt = mdates.DateFormatter('%Y')
    fig, ax = plt.subplots()
    ax.plot(r[:,0],r[:,1])
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.grid(True)
    fig.autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel("Messages")
    plt.show()
    quit()

def plotWeek(): #Plotting messges/day for a week (combined)
    print("Ok, now generating a week graph.")
    plotWeekArray = copy.copy(processedArray) #Again, a bit inefficient.
    with tqdm(leave=True, unit=' messages', total=lineNumber, desc="Preparing") as counter:
        for line in plotWeekArray:
            line[0] = datetime.datetime.fromtimestamp(line[0]).strftime('%A')
            counter.update(1)
    for row in plotWeekArray:
        del row[1]
    print("Now crunching numbers...")
    plotWeekString = [item for sublist in plotWeekArray for item in sublist]
    plotWeekCount = [[x,plotWeekString.count(x)] for x in set(plotWeekString)]
    weekdaysDict = {"Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4, "Friday":5, "Saturday":6, "Sunday":7}
    weekdaysDictInverse = {1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday", 7:"Sunday"}
    plotWeekCountInt = []
    for line in plotWeekCount:
        line = [weekdaysDict[n] if n in weekdaysDict else n for n in line]
        plotWeekCountInt.append(line)
    plotWeekCount.clear()
    plotWeekCountSorted = sorted(plotWeekCountInt, key=lambda l:l[0])
    for line in plotWeekCountSorted:
        line = [weekdaysDictInverse[n] if n in weekdaysDictInverse else n for n in line]
        plotWeekCount.append(line)
    #r = np.asarray(plotWeekCount)
    #r = r[r[:,0].argsort()]
    #print(r)

parser = argparse.ArgumentParser(description='Discord channel imager. Remember to scrape using scrape.py first!')
requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-i', '--input', type=str, help='Textfile source. Must be unaltered output from scrape.py.', required=True)
optional = parser.add_argument_group('Optional arguments')
optional.add_argument('-l', '--graphlong', action='store_true', help='Graph long a long-term graph.')

args = parser.parse_args()

textfile = open(args.input, 'r')
textfileArray = []
lineNumber = sum(1 for line in textfile)

textfile = open(args.input, 'r')
with tqdm(leave=True,unit=' messages', total=lineNumber, desc="Reading file") as counter:
    with textfile as text:
        for line in text:
            line = line.strip()
            textfileArray.append(line)
            counter.update(1)

processedArray = []
with tqdm(leave=True,unit=' messages', total=lineNumber, desc="Processing - Stage 1") as counter:
    for line in textfileArray:
        lineSplitted = line.split(" - ") #lineSplitted[0] is timestamp, lineSplitted[1] is name, discard the rest
        processedArray.append([lineSplitted[0],lineSplitted[1]])
        counter.update(1)

with tqdm(leave=True,unit=' messages', total=lineNumber, desc="Processing - Stage 2") as counter:
    for line in processedArray:
        line[0] = line[0][2:] #Get rid of the pesky b' at the front
        stampSplitted = line[0].split(" ")
        dateSplitted = stampSplitted[0].split("-") #dateSplitted is year,month,day
        timeSplitted = stampSplitted[1].split(":") #timeSplitted is hour,minute,second
        if len(timeSplitted[2]) == 9:
            timeSplitted[2] = timeSplitted[2][:-7]
        else:
            pass
        dateSplitted = [int(x) for x in dateSplitted]
        timeSplitted = [int(x) for x in timeSplitted]
        dateString = datetime.date(dateSplitted[0],dateSplitted[1],dateSplitted[2])
        timeString = datetime.time(timeSplitted[0], timeSplitted[1], timeSplitted[2])
        combined = datetime.datetime.combine(dateString,timeString)
        line[0] = time.mktime(combined.timetuple())
        counter.update(1)

plotWeek()
if args.graphlong:
    plotLong()
else:
    pass
