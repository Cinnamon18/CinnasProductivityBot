from enum import Enum
from user import User
from util import idsFromPings

class BotIntegration():
	def __init__(self, discordId: str):
		self.discordId = discordId
	
	def getDiscordUID(self):
		return self.discordId
	
	def detectBotHook(self, message, botState):
		return

class Sprinto(BotIntegration):
	def __init__(self):
		super(Sprinto, self).__init__("421646775749967872")

	def detectBotHook(self, message, botState):
		if message.author == self.discordId:
			if "**CONGRATS EVERYONE**" in message.content:
				userIDs = idsFromPings(message.content)
				if not userIDs:
					return
				
				for userIDs in userIDs:
					goals = botState.getUser(userIDs).goals
					for goal in goals:
						if goal.botIntegration == self:
							goal.didGoalToday = True
