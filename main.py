import discord
import sqlite3

calendar_filename = "./calendar.db"

token = open("key.txt", "r").readline()

client = discord.Client()

conn= None
cur = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
