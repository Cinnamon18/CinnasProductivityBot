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

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
botState = BotState()
killThreads = False

gacha = Gacha(botState.enabledFranchises)



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

@bot.command(name="setStreakTracking", help="Should the bot remind you if you forget to write for a day?")
async def setStreakTracking(ctx, setStreakTracking: bool):
	botState.getUserCtx(ctx).isStreakTracking = setStreakTracking

	streakTrackStatus = "enabled" if setStreakTracking else "disabled"
	await ctx.send(f"Streak tracking {streakTrackStatus} for user {ctx.author}")
	await ctx.send(f"Current streak: {botState.getUserCtx(ctx).streakLength}")

@bot.command(name="uwu", help="Should the bot remind you if you forget to write for a day?")
async def uwu(ctx):
	botState.lastUsedChannel = ctx.message.channel
	botState.test = True
	# botState.lastUsedChannel = ctx.message.channel
	# botState.users[ctx.author.id] = User(ctx.author.id)
	# botState.users[ctx.author.id].isStreakTracking = True
	# botState.users[ctx.author.id].goals = []
	# botState.users[ctx.author.id].goals.append(Goal("write!"))
	# botState.users[ctx.author.id].goals[0].didGoalToday = True
	# botState.users[ctx.author.id].streakLength = 5
	await ctx.send("uwu")

@bot.command(name="gachaInfo", help="Get info about the gacha rules.")
async def gachaInfo(ctx):
	await ctx.send(f'''**Gacha rules:**
Crystals per pull: {Config.crystalsPerPull}
Pitty: Not implemented
Sparking: Not implemented
''')

@bot.command(name="pull", help="Should the bot remind you if you forget to write for a day?")
async def pull(ctx):
	user = botState.getUserCtx(ctx)
	pull, isDupe = gacha.soloPull(user)

	if not pull:
		await ctx.send(f"You only have {user.crystals} crystals. You need {Config.crystalsPerPull} to pull. Achieve your daily goals to pull more!")
		return

	await ctx.send(embed=pull.toDiscordEmbed(isDupe))

@bot.command(name="giveMeCrystals", help="Should the bot remind you if you forget to write for a day?")
async def giveMeCrystals(ctx, crystalCount:int):
	botState.getUserCtx(ctx).crystals += crystalCount
	await ctx.send(f"Gave user <@!{ctx.author.id}> {crystalCount} crystals")

@bot.command(name="createDaily", help="Should the bot remind you if you forget to write for a day?")
async def createDaily(ctx, goalName:str, botIntegrationStr: str = ""):
	user = botState.getUserCtx(ctx)

	if not botIntegrationStr:
		user.goals.append(Goal(goalName))
		await ctx.send(f"Successfully created goal {goalName}")
	elif idsFromPings(botIntegrationStr) in Goal.botIntegrations:
		user.goals.append(Goal(goalName, Goal.botIntegrations[idsFromPings(botIntegrationStr)]))
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

@bot.command(name="completeDaily", help="Should the bot remind you if you forget to write for a day?")
async def completeDaily(ctx, goalName:str):
	user = botState.getUserCtx(ctx)

	foundGoal = False

	for goal in user.goals:
		if goal.name == goalName:
			goal.didGoalToday = True
			foundGoal = True
			await ctx.send(f"Completed goal {goal.name}!")

	if not foundGoal:
		await ctx.send(f"Couldn't find any daily goals with name {goalName}")


@bot.command(name="tba")
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




async def sendMsg(message, channel = None):
	await bot.wait_until_ready() 
	if channel:
		await channel.send(message)
	else: 
		await botState.lastUsedChannel.send(message)

async def sendEmbed(embed, channel = None):
	await bot.wait_until_ready()  
	if channel:
		await channel.send(embed=embed)
	else: 
		await botState.lastUsedChannel.send(embed=embed)

async def sendBannerAnnouncement(channel):
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
						await sendMsg(f"<@!{user.discordId}>: {user.streakLength} day streak! You recieved: {user.calculateDailyRewards()} crystals for your efforts.")
						user.crystals += user.calculateDailyRewards()
						user.streakLength += 1


			botState.setAllGoalsFalse()
			
			await sendBannerAnnouncement(botState.lastUsedChannel)

			await asyncio.sleep(120)
			botState.dailyMessageSent = False
		
		botState.test = False
		

bot.loop.create_task(mainLoop())
bot.run(TOKEN)