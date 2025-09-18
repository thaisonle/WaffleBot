import asyncio
import discord
from discord import Forbidden, HTTPException, ChannelType
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import json
import random
import webserver
from DuckRace import DuckRace

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='../../ProofBot/discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

retired_role = "Retired"

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    dollar_words = ["$", "dollar", "dollars"]

    if any(i in message.content.lower() for i in dollar_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please use :deer: or something else.")

    await bot.process_commands(message)

@bot.command()
async def start(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    async def promptForInput(content, timeout=20.0, image=False):
        returnValue = None
        try:
            prompt = await ctx.send(content=content)
            response = await bot.wait_for("message", timeout=timeout, check=check)
        except asyncio.TimeoutError:
            await prompt.delete()
            raise asyncio.TimeoutError
        else:
            if image:
                try:
                    returnValue = await response.attachments[0].to_file()
                except HTTPException:
                    await ctx.channel.send("Something went wrong.")
            else:
                returnValue = response.content

            await prompt.delete()
            await response.delete()
            return returnValue

    try:
        await ctx.message.delete()
        raceSetupText = await ctx.send('Setting up race...')

        duckrace = DuckRace(bot)
        duckrace.photo = await promptForInput(content="Please provide timestamped picture of bottle(s):", timeout=25.0, image=True),
        duckrace.title = await promptForInput(content="Please provide title for race:", timeout=25.0),
        duckrace.ducks = await promptForInput(content="How many :duck:(s)?"),
        duckrace.bucks = await promptForInput(content="How much :deer: per :duck:?"),
        duckrace.user = await promptForInput(content="Which user is providing the :tumbler_glass:?"),
        duckrace.venmo = await promptForInput(content="What is their Venmo @?"),
        duckrace.last4 = await promptForInput(content="What is their last 4?")

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Canceled race start...")
    else:
        thread = await ctx.channel.create_thread(
            name=race["title"],
            type=ChannelType.public_thread
        )
        await raceSetupText.delete()
        duckrace.id = thread.id
        await thread.send(content=f"{race["title"]} [Race ID: {duckrace.id}] \n\
\n\
{race["ducks"]} :duck: {race["bucks"]} :deer: :ship:'d CONUS \n\
\n\
Courtesy of {race["user"]} \n\
\n\
!NO SIPS TILL FULL! \n\
\n\
DISCORD NAME ONLY IN VENMO COMMENTS \n\
\n\
:v: {race["venmo"]} \n\
:telephone: Last 4: {race["last4"]} \n\
\n\
List to be shuffled at least 10x for the race. \n\
\n\
Type x<number> to claim spots in the active race (Ex: x5) \n\
\n\
Spots not confirmed by bot will not be honored.", file=race["photo"]
        )

@bot.command()
async def close(ctx, thread_id, winner):
    message = await ctx.channel.fetch_message(thread_id)
    thread = message.thread
    if thread:
        if ctx.message.attachments and len(ctx.message.attachments) > 1:
            files = []
            for a in ctx.message.attachments:
                try:
                    file = await a.to_file()
                except HTTPException:
                    await ctx.channel.send("Something went wrong.")
                else:
                    files.append(file)
            if files:
                await ctx.message.delete()
                await thread.send(content=f"Congrats to {winner}", files=files)
                await thread.send(f"{thread.name} race is closed.")
                await thread.edit(archived=True)
            else:
                await ctx.channel.send("Error has occurred, no files found.")
        else:
            await ctx.message.delete()
            await ctx.send(content="Screenshot and results file required.")
    else:
        await ctx.send("That race could not be found.")

@bot.command()
async def retire(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.content.lower().trim() in ['yes', 'no']

    prompts = [
        "Oh, yeah, because typing 'x2' was such a tough financial decision?",
        "So this time you’re really done, not just taking a ‘break’?",
        "Should I alert Relo that their raffle numbers will finally dip by one?",
        "Are you retiring undefeated at losing?",
        "Should the ducks send you a thank-you card for quitting?",
        "So you’re good with never paying 10 :deer: for disappointment again?"
    ]

    random_prompt = random.choice(prompts)
    await ctx.send(f"{random_prompt} Just type Yes or No, you quitter.")

    try:
        response = await bot.wait_for("message", timeout=20.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Guess you still have money left, let me know.")
    else:
        cleaned_response = response.content.strip().lower()
        if cleaned_response == "yes":
            role = discord.utils.get(ctx.guild.roles, name=retired_role)
            if role:
                await ctx.author.add_roles(role)
                await ctx.send(f"You have been retired from races. You can no longer enter any races.")
            else:
                await ctx.send("Role doesn't exist")
        else:
            await ctx.send("Guess you still have money left, let me know.")

@bot.command()
@commands.has_role(retired_role)
async def unretire(ctx):
    prompts = [
        "Oh, so you missed the thrill of paying for disappointment?",
        "Are you hoping Candace will finally take a day off just for you?",
        "So your wallet was feeling too heavy, huh?",
        "You’re excited to lose in style again?",
        "Is this just your way of donating to WiseVision?",
        "Do you think this time you’ll actually win, or do you just like pain?",
        "So you’re officially back on the ‘professional duck race loser’ career path?",
        "You missed that dopamine crash, didn’t you?",
        "Are you sure disappointment looks good on you?"
    ]

    confirmations = [
        "Type Yes to continue being a degenerate or type No for the best decision you'll make in the next 5 minutes.",
        "Type Yes to donate or type No to keep your money.",
        "Type Yes if you want disappointment or type No if you want fomo.",
        "Type Yes for broke or type No for woke.",
        "Type Yes to fuel duck race servers or type No to fuel your savings.",
        "Type Yes for another L or type No for an actual W.",
        "Type Yes if you love pain or type No if you love gains.",
        "Type Yes to keep gambling or type No to keep your dignity."
    ]

    random_prompt = random.choice(prompts)
    random_confirmation = random.choice(confirmations)
    await ctx.send(f"{random_prompt} {random_confirmation}")
    role = discord.utils.get(ctx.guild.roles, name=retired_role)

    def check(message):
        if role in ctx.author.roles:
            return message.author == ctx.author and message.channel == ctx.channel
        else:
            ctx.send("Role not found on user")
            return False

    try:
        response = await bot.wait_for("message", timeout=20.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send(f"Guess you weren't ready yet, {ctx.author.mention}.")
    else:
        cleaned_response = response.content.strip()
        if cleaned_response.lower() == "yes":
            await ctx.author.remove_roles(role)
            await ctx.send("Welcome back, degenerate! You can now enter races again.")
        elif cleaned_response.lower() == "no":
            await ctx.send("No? Smart choice.")
        else:
            await ctx.send(f"{cleaned_response}? What's that supposed to mean? Sounds like a quitter.")

@unretire.error
async def unretire_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Unretire? You never retired in the first place!!!!!")

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)