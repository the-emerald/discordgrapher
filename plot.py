from tqdm import tqdm
import argparse
import datetime
import time
import copy

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plotLong(): #Plotting messages/day vs day
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

def plotWeekLegacy(): #Legacy barchart plotting messges/day for a week (combined)
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
    print(plotWeekCountSorted)
    return 0
    fig, ax = plt.subplots()
    daysOfWeek = []
    frequency = []
    for line in plotWeekCount:
        daysOfWeek.append(line[0])
        frequency.append(line[1])
    y_pos = np.arange(len(daysOfWeek))
    plt.bar(y_pos, frequency, align='center', alpha=0.5)
    plt.xticks(y_pos, daysOfWeek)
    plt.ylabel('Messages')
    ax.grid(True)
    plt.show()
    quit()

def plotWeekHour(): #Plotting messges per hour for a week
    print("Ok, now generating a week graph.")
    plotWeekArray = copy.copy(processedArray)
    with tqdm(leave=True, unit= 'messages', total=lineNumber, desc="Preparing") as counter:
        for line in plotWeekArray:
            second = datetime.timedelta(seconds=int((line[0]-345600)%604800))
            h = datetime.datetime(1,1,1)+second
            line[0] = h.hour+((h.day-1)*24)
            counter.update(1)
    for row in plotWeekArray:
        del row[1]
    plotWeekFlat= [item for sublist in plotWeekArray for item in sublist]
    plotWeekHourCount = [[x,plotWeekFlat.count(x)] for x in set(plotWeekFlat)]
    r = np.asarray(plotWeekHourCount)
    r = r[r[:,0].argsort()]
    fig, ax = plt.subplots()
    ax.plot(r[:,0],r[:,1])
    ax.grid(True)
    plt.xlabel("Hour of Week (Starts Sunday 0000UTC)")
    plt.ylabel("Messages")
    plt.xticks(np.arange(min(r[:,0]), max(r[:,0]), 24))
    plt.show()
    quit()


parser = argparse.ArgumentParser(description='Discord channel imager. Remember to scrape using scrape.py first!')
requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-i', '--input', type=str, help='Textfile source. Must be unaltered output from scrape.py.', required=True)
optional = parser.add_argument_group('Plotting arguments, pick one')
optional.add_argument('-l', '--graphlong', action='store_true', help='Graph a long-term graph')
optional.add_argument('-w', '--graphweek', action='store_true', help='Graph a messages per hour over a weekday')
kw = parser.add_argument_group('Graph modifications')
kw.add_argument('-s', '--search', type=str, default="None", help='Search and only plot specific phrase.')

args = parser.parse_args()

with open(args.input, 'r') as textfile:
    textfileArray = [line.strip() for line in textfile]
lineNumber = len(textfileArray)
print("Opened file.")

processedArray = []
with tqdm(leave=True,unit=' messages', total=lineNumber, desc="Processing - Stage 1") as counter:
    for line in textfileArray:
        lineSplitted = line.split(" - ") #lineSplitted[0] is timestamp, lineSplitted[1] is name, discard the rest
        if args.search is not "None":
            processedArray.append([lineSplitted[0],lineSplitted[1],lineSplitted[2]]) #lineSplitted[2] is the message.
        else:
            processedArray.append([lineSplitted[0],lineSplitted[1]])
        counter.update(1)

if args.search is not "None":
    processedArraySearch = []
    with tqdm(leave=True,unit=' messages', total=lineNumber, desc="Filtering keywords") as counter:
        for line in processedArray:
            if args.search in line[2]:
                processedArraySearch.append([line[0],line[1]])
            else:
                pass
            counter.update(1)
    processedArray.clear()
    processedArray = copy.copy(processedArraySearch)
    lineNumber = len(processedArray)

if len(processedArray) is 0:
    print("Nothing found... Aborting.")
    quit()

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

if args.graphlong:
    plotLong()
elif args.graphweek:
    plotWeekHour()
else:
    print("Looks like you forgot to pick a graph... Aborting.")
