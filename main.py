import discord
from discord.ext import commands
from webserver import keep_alive
from random import choice
import re
from discord.utils import get
import time
lands = {
    "The frozen shore": [1, 1, "Beyond the wall"],
    "The fist of the first men": [1, 2, "Beyond the wall"],
    "Craster's keep": [1, 3, "Beyond the wall"],
    "The wall": [1, 4, "The wall"],
    "Last hearth": [2, 1, "The north"],
    "Winterfell": [3, 1, "The north"],
    "Hornwood": [3, 2, "The north"],
    "The dreadfort": [3, 3, "The north"],
    "Karhold": [3, 4, "The north"],
    "The first cliffs": [4, 1, "The north"],
    "Moat Cailin": [4, 2, "The north"],
    "White Harbor": [4, 3, "The north"],
    "Widow's watch": [4, 4, "The north"],
    "Greywater watch": [5, 1, "The north"],
    "Three sisters": [5, 2, "Vale"],
    "Oldstones": [6, 1, "Riverlands"],
    "The eyrie": [6, 2, "Vale"],
    "Pyke": [7, 1, "Iron islands"],
    "Riverrun": [7, 2, "Riverlands"],
    "Saltpans": [7, 3, "Vale"],
    "Gull town": [7, 4, "Vale"],
    "Ashemark": [8, 1, "Westerlands"],
    "Harrenhal": [8, 2, "Riverlands"],
    "Maidenpool": [8, 3, "Riverlands"],
    "Dragonstone": [8, 4, "Crownlands"],
    "Casterly Rock": [9, 1, "Westerlands"],
    "Stony Sept": [9, 2, "Riverlands"],
    "King's landing": [9, 3, "Crownlands"],
    "Golden Grove": [10, 1, "The reach"],
    "Grassy Vale": [10, 2, "The reach"],
    "Storm's end": [10, 3, "Stormlands"],
    "Highgarden": [11, 1, "The reach"],
    "Night song": [11, 2, "Stormlands"],
    "Blackhaven": [11, 3, "Stormlands"],
    "Mistwood": [11, 4, "Stormlands"],
    "Old Town": [12, 1, "The reach"],
    "Blackmont": [12, 2, "Dorne"],
    "Salt Shore": [12, 3, "Dorne"],
    "Sunspear": [12, 4, "Dorne"],
}
allies = []
landslist = lands.keys()
countries = [
    "Beyond the wall", "The wall", "The north", "Vale", "Riverlands",
    "Iron islands", "Westerlands", "Crownlands", "The reach", "Stormlands",
    "Dorne"
]

reactions = {
    "happy": [
        "https://64.media.tumblr.com/1b2b3a63915d8d14184aa053a112bbf1/bf04c465294eb89b-49/s540x810/1dc162e3bdd27d1eb57081fc49b506bc303f61bd.gif",
        "https://preview.redd.it/bfy3nb8i39d91.gif?width=600&auto=webp&s=b175689830a9046c94a3c9ea6faf3c3d1333c7f7",
        "https://media.tenor.com/W1Pc37H3HgcAAAAC/caraxes-dragon.gif"
    ],
    "sad": [
        "https://media.tenor.com/xz7mNL4qLaMAAAAd/hbo-vhagar.gif",
        "https://media.tenor.com/SNyOCuR1COUAAAAC/syrax-dragon.gif"
    ],
    "angry": [
        "https://i.pinimg.com/originals/d1/2a/7f/d12a7f70fcc693832b1f190908f2d6eb.gif",
        "https://media.tenor.com/U462JMrXE5YAAAAC/house-of-the-dragon-dragon.gif",
        "https://pa1.aminoapps.com/8444/31f3c233ff50de501fe5d7ab871534b1610c978br1-600-338_hq.gif"
    ],
    "fighting": [
        "https://64.media.tumblr.com/e11c2dd35deccb4a0c9057580ffe30d4/bda0002c8c0030a6-75/s540x810/.gifv",
        "https://media.tenor.com/Nb9m6mEVkmcAAAAC/house-of-the-dragon-vermax.gif",
        "https://media.tenor.com/rN8wVRgcFagAAAAd/drogon-breathing-fire.gif",
        "https://i.pinimg.com/originals/c5/b4/3c/c5b43c17dcfd0c40d53605e12f2ba739.gif",
        "https://64.media.tumblr.com/147364b7c7a7b3e81ac7a6ef2b106300/7909a55742b3d624-2f/s540x810/.gif"
    ],
    "entry": [
        "https://media.tenor.com/H7GHcBwcCGAAAAAd/house-of-the-dragon-vhagar.gif",
        "https://media.tenor.com/sj1ElaGCh3MAAAAC/house-of-the-dragon-dragon.gif"
    ],
}

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.all())


def nearbyfinder(location_id):
  idlist = location_id
  idlist = [int(i) for i in idlist]
  nearlands = []
  for land in landslist:
    if close(lands[land][0], idlist[0]) and close(
        lands[land][1], idlist[1]) and not (lands[land][:2] == idlist):
      nearlands.append(land + " (" + str(lands[land][0]) + "," +
                       str(lands[land][1]) + ") [" + lands[land][2] + "]")

  return nearlands


def findrole(roleslist, name):
  print(roleslist[0])
  for role in roleslist:

    if role.name == name:
      return role


def nametoid(ctx, name):
  guild = ctx.guild
  role_name = name
  for role in guild.roles:
    if role.name == role_name:
      return role


def is_targ(roleslist):
  for role in roleslist:
    if role.name == "House Targaryen":
      return True
  return False


@bot.event
async def on_message(message):
  if bot.user.mentioned_in(message):
    if is_targ(message.author.roles) and message.author.name == ".preludium.":
      if "dracarys" in message.content.lower():
        await message.channel.send(choice(reactions["fighting"]))
      elif "dohaeras" in message.content.lower():
        await message.channel.send(choice(reactions["happy"]))
      elif "daor" in message.content.lower():
        await message.channel.send(choice(reactions["sad"]))
      elif "fly" in message.content.lower() or  "take me" in message.content.lower() or "lessgo" in message.content.lower() or  "go" in message.content.lower():
        print("flying")
        await message.channel.send("*Flying*")
        time.sleep(500)
        filter = re.compile(r"\d{1,2},\d")
        matches = filter.search(message.content)
        position = matches.group(0)

        loc_id = [int(i) for i in position.split(',')]
        targetland = ""
        targetcountry = ""
        currentland = ""
        currentcountry = ""

        a, b = 0, 0
        print("Goin to")
        for role in message.author.roles:
          if role.name in landslist and a == 0:
            currentland = role
            print(currentland)
            a = 1
          if role.name in countries and b == 0:
            currentcountry = role
            print(currentcountry)
            b = 1
        print("Goin to")

        print("Goin to")
        # if not(close(lands[currentland][0], loc_id[0])  and  close(lands[currentland][1], loc_id[1])):
        #   return None
        print(loc_id[0], "and", loc_id[1])
        for i in lands:
          if lands[i][:2] == loc_id:
            targetland = i
            targetcountry = lands[i][2]
            if str(currentcountry) != str(targetcountry):
              print(currentcountry, targetcountry)
              await message.channel.send("https://i.pinimg.com/originals/21/46/ab/2146ab6d51fdf3e9e8bf00e200513ef8.gif")
            else:
              await message.channel.send(f"Now in {targetland}")
            break
        print("Goin to")

        # await message.author.remove_roles(findrole(message.author.roles,currentland))

        await message.author.remove_roles(currentland)
        await message.author.remove_roles(currentcountry)

        await message.author.add_roles(nametoid(message, targetland))
        await message.author.add_roles(nametoid(message, targetcountry))

        member = get(message.guild.members, name="Vhagar")

        await member.remove_roles(currentcountry, currentland)
        await member.add_roles(nametoid(message, targetland),
                               nametoid(message, targetcountry))

        print("Goin to")
      else:
        await message.channel.send(
            choice(reactions["entry"] + reactions["entry"]))
    else:
      print(message.author.roles)
      await message.channel.send(choice(reactions["angry"]))


keep_alive()

bot.run(
    "MTE4MTc5MzU0OTMxNDk2OTYxMA.Gt_i9U.7I1WhetnVQI7FMrQvQml5cF2SKp-92jCkrq6bA")
