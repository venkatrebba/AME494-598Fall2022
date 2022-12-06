"""
Author: Venkatarao Rebba <rebba498@gmail.com>
This script aimed to send a Discord message through a bot
"""

import requests
import discord
from os import path
import urllib.request
from google.cloud import storage

def hello_gcs(data, context):
     fle = data
     root = path.dirname(path.abspath(__file__))
     try:
          file_path = '/tmp/' + 'img.png'
          file_path = path.join(root, file_path)
          storage_client = storage.Client()
          bucket = storage_client.get_bucket(data['bucket'])
          blob = bucket.blob(data['name'])
          blob.download_to_filename(file_path)
     except Exception as e:
          print("Exception", e)

     intents = discord.Intents.all()
     client = discord.Client(intents=intents)

     @client.event
     async def on_ready():
          print('We have logged in as {0.user}'.format(client))
          channel = client.get_channel(1038588980616253450)
          await channel.send("Hello Humans , this is your new security Agent from second program")
          await channel.send(file=discord.File(file_path))
          exit()

     client.run('MTAzODYwNDI3OTUxNjI1NDI0OQ.GPliEH.Fso0EbdkNvQSrfSGvtL-dCopgaON5E-5fjg8Jc')
     print('Finished success')

