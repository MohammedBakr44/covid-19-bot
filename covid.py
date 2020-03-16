import discord
import json
import urllib
import asyncio

# Reads first line of token.txt and return it to get the token
def read_token():
  # You can change token.txt with any file you want to use to store the token, unless it's .txt.
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

TOKEN = read_token()
# Client ID, put yours
CHANNEL_ID = 688984938783047696

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord!')



async def corona_world():
  await client.wait_until_ready()
  # Data likn(JSON)
  link = 'https://covid19.mathdro.id/api'
  # Using urllib.request to open the URL
  f = urllib.request.urlopen(link)
  # Read data from the URL(JSON)
  mydata = f.read()
  # Convert JSON to lists in order to make available to work with.
  dataj = json.loads(mydata)

  # Messages to be outputed

  messages = [
    f"Confirmed: {dataj['confirmed']['value']}:sick:",
    f"Recovered: {dataj['recovered']['value']}:green_heart:",
    f"Deaths: {dataj['deaths']['value']}:skull:"
  ]
  # Run the function while the client(bot) is running
  while not client.is_closed():
    # Get the channel ID in order to make post in a specific channel
      channel = client.get_channel(CHANNEL_ID)
      # Loop tgrough messages and send the stats
      for message in messages:
        await channel.send((message))
      # Wait for 3600seconds(1 Hour) and repeat the process
      await asyncio.sleep(3600)
# Display data for Egypt
async def corona_eg():
  await client.wait_until_ready()
  
  while not client.is_closed():
      channel = client.get_channel(CHANNEL_ID)
      """" I had to use another API; the first one has the code for Egypt as EG and it's written like this in the link
           So I had to replace it, and this one doesn't show them in one request, you have to request one of the three params, confirmed, recovered, deaths.
           More infromation: https://covid19api.com/
      """
      # List the cases to be able to make three requests
      cases = ['confirmed', 'recovered', 'deaths']
      # I split up message content because...The easiest way to do it
      # This is what the number means
      messageseg = [
        "Confirmed: ",
        "Recovered: ",
        "Deaths: "
      ]
      # Here's the emotes which will be added at the end of the message
      emotes = [
        ":sick:",
        ":green_heart:",
        ":skull:"
      ]

      # Send message to clearify it's displaying Egypt's stats
      await channel.send("أم الدنيا:flag_eg:")
      for i in range(3):
        eg = 'https://api.covid19api.com/total/country/egypt/status/' + cases[i]

        egf = urllib.request.urlopen(eg)

        egdata = egf.read()

        egj = json.loads(egdata)
        # Displays the whole message eg: Confirmed: 110 :sick:
        await channel.send((f"{messageseg[i]}{egj[-1]['Cases']}{emotes[i]}"))
      # Wait for 5400(90 Minutes) and repeat the process    
      await asyncio.sleep(5400)

    


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # For future featuers

client.loop.create_task(corona_world())
client.loop.create_task(corona_eg())
client.run(TOKEN)