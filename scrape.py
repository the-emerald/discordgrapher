import discord
import asyncio
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description='Discord channel scraper')
requiredNamed = parser.add_argument_group('Required arguments:')
requiredNamed.add_argument('-c', '--channel', type=str, help='Channel to scrape. Requires the channel ID.', required=True)
requiredNamed.add_argument('-o', '--output', type=str, help='Output file in form *.txt. Will be stored in the same directory.', required=True)

args = parser.parse_args()

client = discord.Client()

@client.event
async def on_ready():
    print('Connection successful.')
    print('Your ID: ' + client.user.id)
    target = open(args.output, 'w')
    print(args.output, 'has been opened.')

    messageCount = 0
    channel = discord.Object(id=args.channel)

    print("Scraping messages... Don't send any messages while scraping!")
    with tqdm(leave=True,unit=' messages') as scraped:
        async for msg in client.logs_from(channel, 10000000000):
            line = "{} - {} - {}".format(msg.timestamp,msg.author.name, msg.content)
            line = line.encode('utf-8')
            toWrite = "{}".format(line)
            target.write(toWrite)
            target.write("\n")
            messageCount += 1
            scraped.update(1)
    print('-----')
    print('Scraping complete.')


#----------------------------

client.run('email', 'password')
