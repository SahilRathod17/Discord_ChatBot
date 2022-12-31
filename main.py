import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

sad_words = [
  "bad", "not good", "feels bad", "sad", "depressed", "sadness", "unhappy",
  "angry", "miserable", "depressing", "unpleasant", "i feel lonely"
]

bloked_words = [
  "http://",
  "https://",
  "www.",
  "http://www.google.com",
]

starter_encouragement = [
  "cheer up", "hang in there", "keep trying",
  "you are a great person / bot (like me)",
  "you are a good person / bot (like me)", "do your best!", "you can do it!",
  "keep it up"
]

greet_que = [
  "how are you",
  "how you doin",
  "how are you doing",
  "i am fine, what about you",
  "how's it going",
]

greet_ans = [
  "I am good. what about you ?",
  "I am fine. thanks for asking.",
  "Fast as ever!!",
  "Good as meme!",
]

if "responding" not in db.keys():
  db["responding"] = True

intro_que = [
  "what are you", "what is your name ", "who created you", "hello", "hey",
  "hi", "hii", "hiii", "yo"
]

intro_words = [
  "Hello, I'm a bot that can help you with a few things.",
  "Welcome to the bot! I'm a bot that helps you to improve your life. Thanks to sahil.",
  "Hello, I'm a bot created by Sahil.",
  "Hello, my name Bot. I'm created by sahil.",
  "Hello, I'm a bot created by Sahil. I'm a bot that helps you to improve your life.",
]

outro_words = ["bye", "goodbye", "bye bye"]

outro_ans = [
  "bye, have a nice day.",
  "bye, have a good day.",
  "see you soon.",
]


# fetch random quotes from the zenquotes
def get_quote():
  response = requests.get('http://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)


# fetch jokes from  API
def get_joke():
  response = requests.get('https://backend-omega-seven.vercel.app/api/getjoke')
  json_data = json.loads(response.text)
  joke = json_data[0]['question'] + "\n" + json_data[0]['punchline']
  return (joke)


def update_encouragement(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [encouraging_message]


def delete_encouragement(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements


@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client).format(client))


@client.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(f'Welcome To The Server {member}!')


@client.event
async def on_message_edit(before, after):
  await before.channel.send(f'{before.author} edited {after.content}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  for text in bloked_words:
    if text in msg:
      await message.delete()
      await message.channel.send("You can't use that word. Try something else."
                                 )
      return

  if message.content == '$private':
    await message.delete()
    await message.author.send("Hello in Private, Blink..")

  if message.content.startswith('$inspire'):
    qoute = get_quote()
    await message.channel.send(qoute)

  if message.content.startswith('$joke'):
    joke = get_joke()
    await message.channel.send(joke)

  if any(word in msg for word in outro_words):
    await message.channel.send(random.choice(outro_ans))

  if any(word in msg for word in intro_que):
    await message.channel.send(random.choice(intro_words))

  if any(word in msg for word in greet_que):
    await message.channel.send(random.choice(greet_ans))

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragement))

  if db["responding"]:
    options = []
    if "encouragements" in db.keys():
      options = options + list(db['encouragements'])

    if msg.startswith('$add'):
      encouraging_message = msg.split('$add ', 1)[1]
      update_encouragement(encouraging_message)
      await message.channel.send("message added!")

    if msg.startswith('$del'):
      encouragments = []
      if "encouragements" in db.keys():
        index = int(msg.split('$del', 1)[1])
        delete_encouragement(index)
        encouragments = db['encouragements']
        await message.channel.send(encouragments)

    if msg.startswith('$list'):
      encouragments = []
      if "encouragements" in db.keys():
        encouragments = db['encouragements']
        await message.channel.send(encouragments)

  if msg.startswith('$responding'):
    value = msg.split('$responding ', 1)[1]

    if value.lower() == 'true':
      db["responding"] = True
      await message.channel.send("responding is now On")

    else:
      db["responding"] = False
      await message.channel.send("responding is now Off")


keep_alive()
client.run(os.getenv('TOKEN'))
