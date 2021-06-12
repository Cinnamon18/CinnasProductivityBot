from user import User
from card import Card
from botIntegration import Sprinto
from config import Config

class BotState():
	def __init__(self):
		self.users = dict()
		self.dailyMessageSent = False

		#TODO make this work in more than 1 server at once
		self.lastUsedChannel = None

		self.enabledFranchises = set(["bang_dream", "love_live", "arknights"])

		self.test = False

		self.botIntegrations = 	{
			"421646775749967872": Sprinto()
		}

	def getUser(self, userId) -> User:
		'''Gets a user from the list of users. If user does not exist, a new one will be created.'''

		userId = str(userId) # Lmao this is causing me headaches so i'm gonna solve it this way.
		if not userId in self.users:
			self.users[userId] = User(userId)

		return self.users[userId]
	
	def getUserCtx(self, ctx):
		'''Shorthand with a context.'''
		self.lastUsedChannel = ctx.message.channel
		return self.getUser(ctx.author.id)
	
	def dailyReset(self, gacha):
		gacha.generateRateUpCards()

		for user in self.users.values():
			user.coins += Config.coinsPerUnusedSpark * user.sparks
			user.sparks = 0
			for goal in user.goals:
				goal.didGoalToday = False

	# If we ever change the details on a card, we will have to call this
	def updateCard(self, oldUID: str, newCard: Card):
		for user in self.users:
			for card in user.gachaCardsUIDs:
				if(card.uid == oldUID):
					user.gachaCardsUIDs.remove(card)
					break
			user.gachaCardsUIDs.add(newCard.uid)