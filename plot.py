from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description='Discord channel imager. Remember to scrape using scrape.py first!')
requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-i', '--input', type=str, help='Textfile source. Must be unaltered output from scrape.py.', required=True)
args = parser.parse_args()

textfile = open(args.input, 'r')
textfileArray = []
lineNumber = sum(1 for line in textfile)

textfile = open(args.input, 'r')
with tqdm(leave=True,unit=' messages',total=lineNumber, desc="Reading file") as counter:
    with textfile as text:
        for line in text:
            line = line.strip()
            textfileArray.append(line)
            counter.update(1)

processedArray = []
with tqdm(leave=True,unit=' messages',total=lineNumber, desc="Processing - Stage 1") as counter:
    for line in textfileArray:
        lineSplitted = line.split(" - ") #line[0] is timestamp, line[1] is name, discard the rest
        processedArray.append([lineSplitted[0],lineSplitted[1]])
        counter.update(1)

