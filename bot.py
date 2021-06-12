# bot.py
import os
import logging
logging.basicConfig(level=logging.INFO)

import discord
import time
from datetime import datetime
import asyncio
import traceback
import threading
import re

from discord.ext import commands
from dotenv import load_dotenv
from botState import BotState
from user import User
from config import Config
from gacha import Gacha
from goal import Goal
from util import idsFromPings
from serialization import Serialization

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')
killThreads = False

botState = Serialization.loadData(Config.saveFileName)
if not botState:
	botState = BotState()
botState.test = False

gacha = Gacha(botState.enabledFranchises)

# Just to shut up Azure lmao
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"




@bot.event
async def on_ready():
	for guild in bot.guilds:
		print(f"{bot.user} is connected to server {guild} with members {guild.members}")

@bot.event
async def on_error(event, *args, **kwargs):
	with open('err.log', 'a') as f:
		if event == 'on_message':
			f.write(f'Unhandled message: {args[0]}\n')
		else:
			raise

@bot.command(name="setStreakTracking", help="`setStreakTracking y` or `setStreakTracking n`. When streak tracking is enabled, the bot will reward you for completing your daily goals with ever increasing amounts of crystals! When streak tracking is off your streak will neither increase nor decrease.")
async def setStreakTracking(ctx, setStreakTracking: bool):
	botState.getUserCtx(ctx).isStreakTracking = setStreakTracking

	streakTrackStatus = "enabled" if setStreakTracking else "disabled"
	await ctx.send(f"Streak tracking {streakTrackStatus} for user {ctx.author}")
	await ctx.send(f"Current streak: {botState.getUserCtx(ctx).streakLength}")

@bot.command(name="gachaInfo", help="Get info about the gacha rules.")
async def gachaInfo(ctx):
	await ctx.send(f'''__**Gacha rules:**__

**Gacha**
Crystals per pull: {Config.crystalsPerPull}
Pitty: Not implemented
Sparking: {Config.pullsToSpark} Cinnamon Sparks = 1 banner character of your choice. Sparks reset at daily reset. Unused sparks are converted to coins at a rate of {Config.coinsPerUnusedSpark} coins per spark.

Banner UR count: {Config.rateUpURCount}
Chance of pulling banner UR if UR pulled: {Config.rateUpURRates}
Banner SSR count: {Config.rateUpSSRCount}
Chance of pulling banner SSR if SSR pulled: {Config.rateUpSSRRates}
Overall probabilities: {Config.probabilities}

**Misc**
Daily reset time: 0{Config.dayResetTime}:00 UTC
''')

@bot.command(name="pull", help=f"Consumes {Config.crystalsPerPull} crystals to do one gacha pull.")
async def pull(ctx):
	user = botState.getUserCtx(ctx)
	pull, isDupe = gacha.soloPull(user)

	if not pull:
		await ctx.send(f"You only have {user.crystals} crystals. You need {Config.crystalsPerPull} to pull. Achieve your daily goals to get more crystals!")
		return

	await ctx.send(embed=pull.toDiscordEmbed(isDupe))

@bot.command(name="tenPull", help=f"Consumes {Config.crystalsPerPull * 10} crystals to do 10 pulls.")
async def tenPull(ctx):
	user = botState.getUserCtx(ctx)
	if user.crystals < Config.crystalsPerPull * 10:
		await ctx.send(f"You only have {user.crystals} crystals. You need {Config.crystalsPerPull * 10} to ten pull. Achieve your daily goals to get more crystals!")

	for i in range(10):
		pull, isDupe = gacha.soloPull(user)
		await ctx.send(embed=pull.toDiscordEmbed(isDupe))

@bot.command(name="myCards", help=f"Prints out all your cards! Optional argument for a given rarity (only print UR cards, SSR, etc.)")
async def myCards(ctx, rarity:str = ""):
	user = botState.getUserCtx(ctx)
	cards = []
	for cardUID in user.gachaCardsUIDs:
		cards.append(gacha.cardsByUID[cardUID])
	
	if rarity:
		cards = [card for card in cards if card.rarity == rarity]
	
	if len(cards) > 25:
		await ctx.send("Too many cards to send! Please wait until I implement pagination. Consider using a rarity filter if you are not.")
		return
	
	for card in cards:
		await ctx.send(embed=card.toDiscordEmbed(True))

@myCards.error
async def myCards(ctx, error):
	print(error)
	print(traceback.format_exc())
	await ctx.send(f"Error handling my cards request.")


@bot.command(name="spark", help="`!spark exusiai` or `!spark arknights_3`. Sparks for a given character! Consumes 100 cinnamon sparks, which you can get by pulling.")
async def spark(ctx, sparkSearchString:str):
	user = botState.getUserCtx(ctx)

	card = gacha.fuzzySearchForCard(sparkSearchString, rateUpOnly=True)
	if not card:
		await ctx.send("I couldn't understand which character you're trying to spark. enter `!spark characterUID` or `!spark \"Character Name\"")
	
	sparkedCard, isDupe = gacha.spark(user, card)
	if not sparkedCard:
		await ctx.send(f"You only have {user.sparks} Cinnamon Sparks, need {Config.pullsToSpark}.")
	else:
		await ctx.send("Spark successful!")
		await ctx.send(embed=pull.toDiscordEmbed(isDupe))

@spark.error
async def spark(ctx, error):
	print(error)
	print(traceback.format_exc())
	await sendBannerAnnouncement(ctx.message.channel)
	await ctx.send(f'''I couldn't understand your spark request! Double check you entered a sparkable character.''')

@bot.command(name="checkCrystals", help="Prints out how many crystals you have")
async def giveMeCrystals(ctx):
	await ctx.send(f"User <@!{ctx.author.id}>, you currently have {botState.getUserCtx(ctx).crystals} crystals")

@bot.command(name="createDaily", help="`!createDaily write` or `!createDaily write w` or `!createDaily write w @Sprinto`. Creates a daily goal, which the bot will ask you to complete daily.")
async def createDaily(ctx, goalName:str, shorthand:str = "", botIntegrationStr: str = ""):
	user = botState.getUserCtx(ctx)

	if not botIntegrationStr and not shorthand:
		user.goals.append(Goal(goalName))
		await ctx.send(f"Successfully created goal {goalName}")
	elif not botIntegrationStr and shorthand:
		user.goals.append(Goal(goalName, shorthand))
		await ctx.send(f"Successfully created goal {goalName} with abbreviation {shorthand}")
	elif idsFromPings(botIntegrationStr) in Goal.botIntegrations:
		user.goals.append(Goal(goalName, shorthand, Goal.botIntegrations[idsFromPings(botIntegrationStr)]))
		await ctx.send(f"Successfully created goal {goalName} integrated into bot <@!{botIntegrationStr}>")
	else:
		await ctx.send(f"Sorry, no integration found for bot <@!{botIntegrationStr}>")

@createDaily.error
async def createDailyError(ctx, error):
	print(error)
	print(traceback.format_exc())
	await ctx.send(f'''I couldn't understand your daily goal format! Please phrase it as `!createDaily \"Goal name\"`, for example `!createDaily "Exercise every day!"
	If you wish to use a bot integration, you can instead use `!createDaily \"Goal Name" @bot`, for example `!createDaily "Write once a day!" @Sprinto#2517`
	''')

@bot.command(name="completeDaily", help="`!completeDaily write`. Marks your goal as completed, and rewards you with crystals for doing such at the day roll over.")
async def completeDaily(ctx, goalName:str):
	user = botState.getUserCtx(ctx)

	foundGoal = False

	for goal in user.goals:
		if goal.name == goalName or goal.shorthand == goalName:
			goal.didGoalToday = True
			foundGoal = True
			await ctx.send(f"Completed goal {goal.name}!")

	if not foundGoal:
		await ctx.send(f"Couldn't find any daily goals with name or shorthand {goalName}")


@bot.command(name="banner", help="Check today's rate up cards")
async def tba(ctx):
	await sendBannerAnnouncement(ctx.message.channel)

# @bot.event
# async def on_message(message):
# 	if message.author == bot.user:
# 		return
	
# 	print(message.content)
# 	print(message.author)

# 	for botIntegration in botState.botIntegrations:
# 		botIntegration.detectBotHook(message, botState)

# TEST COMMANDS NOT FOR PRODUCTION

@bot.command(name="triggerDailyReset", help="")
async def triggerDailyReset(ctx):
	botState.lastUsedChannel = ctx.message.channel
	botState.test = True
	await ctx.send("Triggered daily reset!")

@bot.command(name="giveMeCrystals", help="")
async def giveMeCrystals(ctx, crystalCount:int):
	botState.getUserCtx(ctx).crystals += crystalCount
	await ctx.send(f"Gave user <@!{ctx.author.id}> {crystalCount} crystals")





async def sendMsg(message, channel = None):
	if not channel:
		print("No channel object, can't send message D:")

	await bot.wait_until_ready() 
	if channel:
		await channel.send(message)
	else: 
		await botState.lastUsedChannel.send(message)

async def sendEmbed(embed, channel = None):
	if not channel:
		print("No channel object, can't send embed D:")

	await bot.wait_until_ready()  
	if channel:
		await channel.send(embed=embed)
	else: 
		await botState.lastUsedChannel.send(embed=embed)

async def sendBannerAnnouncement(channel):
	await sendMsg("**New banner!**", channel)
	await sendMsg("Today's Banner URs:", channel)
	for card in gacha.rateUpURs:
		await sendEmbed(card.toDiscordEmbed(False), channel)
	await sendMsg("Today's Banner SSRs:", channel)
	for card in gacha.rateUpSSRs:
		await sendEmbed(card.toDiscordEmbed(False), channel)

async def mainLoop():
	while(True):
		await asyncio.sleep(10)

		if botState.test or (datetime.utcnow().time().hour == Config.dayResetTime and datetime.utcnow().time().minute == 0 and not botState.dailyMessageSent):
			botState.dailyMessageSent = True

			if any(user.isStreakTracking for user in botState.users.values()) and botState.lastUsedChannel:
				await sendMsg("Congrats all our users! Today's streak maintainers:")
				for user in botState.users.values():
					if not user.isStreakTracking:
						break

					unaccomplishedGoals = user.getUnaccomplishedGoals()

					if unaccomplishedGoals:
						user.streakLength = 0
						await sendMsg(f"<@!{user.discordId}>: streak broken D:\nMissed goals: {', '.join([goal.name for goal in unaccomplishedGoals])}" )
					else:
						user.crystals += user.calculateDailyRewards()
						await sendMsg(f"<@!{user.discordId}>: {user.streakLength} day streak! You recieved: {user.calculateDailyRewards()} crystals for your efforts. You now have {user.crystals} crystals total.")
						user.streakLength += 1

			botState.dailyReset(gacha)
			Serialization.saveData(botState, Config.saveFileName)
			
			await sendBannerAnnouncement(botState.lastUsedChannel)
			botState.test = False

			await asyncio.sleep(120)
			botState.dailyMessageSent = False

bot.loop.create_task(mainLoop())
bot.run(TOKEN)