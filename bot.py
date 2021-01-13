# bot.py
import os
import discord
from dotenv import load_dotenv
from firebase import firebase
from tabulate import tabulate


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DATABASE = os.getenv('DATABASE_URL')

firebase = firebase.FirebaseApplication(DATABASE, None)
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$bet'):
        if "-l" in message.content:
            all_bets = firebase.get("/bets/", None)
            if all_bets:
                rows = ""
                for i in all_bets:
                    r = "ID: " + i + "\n" + "Bet: " + all_bets[i]["Bet"] + "\n" + "Predictor: " + all_bets[i]["Predictor"] + "\n" + "Challenger: " + all_bets[i]["Challenger"] + \
                        "\n" + "Stakes: " + all_bets[i]["Stakes"] + "\n" + "Duration: " + \
                        all_bets[i]["Duration"] + "\n" + \
                        "Status: " + \
                        all_bets[i]["Status"] + "\n\n"
                    rows += r
                await message.channel.send("```" + rows + "```")
            else:
                await message.channel.send("```" + "No bets yet. Start one!" + "```")
        elif "-c" in message.content:
            commands = 'To create a new bet:' + "\n" + '$bet -n "Winnie the Pooh will be the emperor of the world by 2050" -s "0.1 BTC" -d "31-12-2050"' + "\n\n" + 'To list all bets:' + "\n" + '$bet -l' + \
                "\n\n" + 'To accept a bet, look up the 4- char bet ID from the list and:' + "\n" + '$bet -a "XXXX"' + \
                "\n\n" + 'To delete a bet, take the bet ID and:' + "\n" + '$bet -d "XXXX"' + "\n\n" + \
                'The code for this bot is written by a n00b code monkey. Please help us make the bot better! Create a PR at: https://github.com/tusharhq/discord-betting-bot'
            await message.channel.send("```" + commands + "```")
        else:
            cmd = message.content.replace("$bet", "python cli.py")
            print(cmd + " -u " + str(message.author.name))
            result = os.system(cmd + " -u " + str(message.author.name))

            if result == 0:
                await message.channel.send("```" + "Done! Run $bet -l to see changes." + "```")
            else:
                await message.channel.send("```" + "Something went wrong. Please check the command format and try again." + "```")

client.run(TOKEN)
