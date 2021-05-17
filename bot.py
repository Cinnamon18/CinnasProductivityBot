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

from discord.ext import commands
from dotenv import load_dotenv
from sprint import Sprint, SprintPhase
from botState import BotState
from writer import Writer
from config import Config
from gacha import Gacha

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='_')
botState = BotState()
killThreads = False

gacha = Gacha()

def startClient():
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	bot.run(TOKEN)



@bot.event
async def on_ready():
	for guild in bot.guilds:
		print(str(bot.user) + " is connected to server " + str(guild))

@bot.event
async def on_error(event, *args, **kwargs):
	print(event)
	with open('err.log', 'a') as f:
		if event == 'on_message':
			f.write(f'Unhandled message: {args[0]}\n')
		else:
			raise

@bot.command(name="sprint", help="Starts a writing sprint")
async def sprint(ctx, sprintLength: int=0):
	if not botState.curSprint == None:
		await ctx.send("Sprint already in progress!")
		return

	if sprintLength == 0:
		sprintLength = Config.defaultSprintLength

	await ctx.send("Starting a " + str(sprintLength) + " minute sprint! Join with _join!")
	botState.curSprint = Sprint(ctx.guild, ctx.message.channel, time.time(), 60 * sprintLength)
	await waitForUsersToJoin()

@sprint.error
async def sprint_error(ctx, error):
	print(error)
	print(traceback.format_exc())
	await ctx.send("Bot encountered an error D: let @Cinnamon18#1729 know. They should alr have all the logs if u send them the time it happened.")

@bot.command(name="join", help="Joins a writing sprint")
async def join(ctx, wordCount: int=0):
	if(not botState.curSprint or not botState.curSprint.sprintPhase == SprintPhase.JOIN):
		await ctx.send("Can't join a sprint right now!")
		return

	botState.getUserCtx(ctx).currentSprintStartingWords = wordCount
	botState.curSprint.participants.add(botState.getUserCtx(ctx))
	await ctx.send(f"{ctx.author.mention} joined the sprint with {wordCount} words!")


@bot.command(name="wc", help="")
async def wc(ctx, wordCount: int):
	if(not botState.curSprint or not botState.curSprint.sprintPhase == SprintPhase.REPORT_WORDCOUNT):
		await ctx.send("Can't report word count right now!")
		return
	
	botState.getUserCtx(ctx).currentSprintWords = wordCount
	await ctx.send(f"{ctx.author.mention} wrote {wordCount} words!")


@bot.command(name="setStreakTracking", help="Should the bot remind you if you forget to write for a day?")
async def setStreakTracking(ctx, setStreakTracking: bool):
	botState.getUserCtx(ctx).isStreakTracking = setStreakTracking

	streakTrackStatus = "enabled" if setStreakTracking else "disabled"
	await ctx.send(f"Streak tracking {streakTrackStatus} for user {ctx.author}")
	await ctx.send(f"Current streak: {botState.getUserCtx(ctx).streakLength}")

# This is such an unscalable way of doing this. But for now, to get it off the ground,
async def waitForUsersToJoin():
	await asyncio.sleep(Config.timeToWaitForSprintStart)
	await botState.curSprint.channel.send("Get writing!!!")
	botState.curSprint.sprintPhase = SprintPhase.WRITE
	await asyncio.sleep(botState.curSprint.sprintLength)
	await botState.curSprint.channel.send("That concludes the sprint! Drop your word counts here.")
	botState.curSprint.sprintPhase = SprintPhase.REPORT_WORDCOUNT
	await asyncio.sleep(Config.timeToWaitForWordCounts)
	await botState.curSprint.channel.send("Congrats everyone!")
	for participant in botState.curSprint.participants:
		wordsWritten = participant.currentSprintWords - participant.currentSprintStartingWords
		await botState.curSprint.channel.send(f"@{participant.discordId}: {wordsWritten} words ({wordsWritten / botState.curSprint.sprintLength:.0f} wpm)")

	botState.lastUsedChannel = botState.curSprint.channel
	botState.curSprint = None

@bot.command(name="uwu", help="Should the bot remind you if you forget to write for a day?")
async def uwu(ctx):
	botState.test = True
	botState.lastUsedChannel = ctx.message.channel
	botState.writers[ctx.author.id] = Writer(ctx.author.id)
	botState.writers[ctx.author.id].isStreakTracking = True
	botState.writers[ctx.author.id].didWriteToday = True
	botState.writers[ctx.author.id].streakLength = 5
	await ctx.send("uwu")

@bot.command(name="pull", help="Should the bot remind you if you forget to write for a day?")
async def pull(ctx, pullCount:int = 0):
	pull = gacha.soloPull()

	await ctx.send(f"{pull}")





async def sendMsg(message):
	send_fut = asyncio.run_coroutine_threadsafe(sendMsgHelper(message), botThread)
	send_fut.result()

async def sendMsgHelper(message):
	await botState.lastUsedChannel.send(message)

def mainLoop():
	asyncio.run(mainLoopCoroutine())

async def mainLoopCoroutine():
	while(not killThreads):
		print(botState.test)
		if botState.test or (datetime.utcnow().time().hour == Config.dayResetTime and datetime.utcnow().time().minute == 0 and not botState.dailyMessageSent):
			print('b')
			botState.dailyMessageSent = True

			if any(writer.isStreakTracking for writer in botState.writers.values()) and botState.lastUsedChannel:
				await sendMsg("Congrats all our writers! Today's streak maintainers:")
				for writer in botState.writers.values():
					if not writer.isStreakTracking:
						break

					if writer.didWriteToday:
						writer.streakLength += 1
					else:
						writer.streakLength = 0
					
					if not writer.didWriteToday:
						await botState.lastUsedChannel.send("@" + str(writer.discordId) + ": streak broken D: " )
					else:
						await botState.lastUsedChannel.send("@" + str(writer.discordId) + ": " + str(writer.streakLength) + " day streak! " )


			await asyncio.sleep(120)
			botState.dailyMessageSent = False
		
		await asyncio.sleep(2)

# mainThread = threading.Thread(target=mainLoop)
# mainThread.start()

botThread = threading.Thread(target=startClient)
botThread.start()

mainLoop()

print("Joining main thread")
# killThreads = True
# mainThread.join()
# print("Main thread joined successfully")