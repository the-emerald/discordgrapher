import discord
import asyncio
from tqdm import tqdm
from sys import argv

script, fileName = argv
client = discord.Client()

@client.event
async def on_ready():
    print('Connection successful.')
    print('ID: ' + client.user.id)
    print('-----')
    target = open(fileName, 'w')
    print(fileName, 'has been opened.')

    messageCount = 0
    channel = discord.Object(id='107634811132231680')

    print('Scraping messages...')
    with tqdm(leave=True,unit='messages') as scraped:
        async for msg in client.logs_from(channel, 10000000000):
            line = "{} - {}: {}".format(msg.timestamp,msg.author.name, msg.content)
            line = line.encode('utf-8')
            toWrite = "{}".format(line)
            target.write(toWrite)
            target.write("\n")
            #messageCount += 1
            #print(messageCount)
            #print(msg.author,msg.content)
            scraped.update(1)
    print('-----')
    print('Scraping complete.')


#----------------------------

client.run('email', 'password')
