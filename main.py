import discord
from discord.ext import commands
import re
import json
import os




if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": "x-", "bannedWords": []}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]
bannedWords = configData["bannedWords"]

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print("TheEye is online")


@bot.command()
@commands.has_permissions(administrator=True)
async def addbannedword(ctx, word):
    if word.lower() in bannedWords:
        await ctx.send(f"{word} is already banned from this server")
    else:
        bannedWords.append(word.lower())

        with open("./config.json", "r+") as f:
            data = json.load(f)
            data["bannedWords"] = bannedWords
            f.seek(0)
            f.write(json.dumps(data))
            f.truncate()

            await ctx.message.delete()
            await ctx.send(f"{word} has been added to the list of banned words")


@bot.command()
@commands.has_permissions(administrator=True)
async def removebannedword(ctx, word):
    if word.lower() in bannedWords:
        bannedWords.remove(word.lower())

        with open(os.getcwd() + "/config.json", "r+") as f:
            data = json.load(f)
            data["bannedWords"] = bannedWords
            f.seek(0)
            f.write(json.dumps(data))
            f.truncate()

            await ctx.message.delete()
            await ctx.send(f"{word} has been removed from the list of banned words")\

def msg_contains_word(msg, word):
    return re.search(fr'\b({word})\b', msg) is not None

@bot.event
async def on_message(message):
    messageAuthor = message.author

    if bannedWords is not None and (isinstance(message.channel, discord.channel.DMChannel) == False):
        for bannedWord in bannedWords:
            if msg_contains_word(message.content.lower(), bannedWord):
                await message.delete()
                embed = discord.Embed(title= "Banned Word Contained", colour=0xE74C3C, description=f"{messageAuthor.mention} the message you have sent in {message.channel} is banned in this server. Please refrain from using these kinds of words or you will be subject to punishment as seen fit by server staff")
                await message.channel.send(embed=embed)

    await bot.process_commands(message)
bot.run(token)
