from tqdm import tqdm
import argparse
import datetime
import time

parser = argparse.ArgumentParser(description='Discord channel imager. Remember to scrape using scrape.py first!')
requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-i', '--input', type=str, help='Textfile source. Must be unaltered output from scrape.py.', required=True)
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

for x in processedArray:
    if x[0] != int(x[0]):
        print(x)
