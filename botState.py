from writer import Writer
from card import Card

class BotState():
	def __init__(self):
		self.writers = dict()
		self.dailyMessageSent = False

		#TODO make this work in more than 1 server at once
		self.curSprint = None
		self.lastUsedChannel = None

		self.enabledFranchises = set(["bang_dream", "love_live", "arknights"])


		self.test = False

	def getUser(self, userId):
		'''Gets a user from the list of writers. If user does not exist, a new one will be created.'''
		if not userId in self.writers:
			self.writers[userId] = Writer(userId)
		
		return self.writers[userId]
	
	def getUserCtx(self, ctx):
		'''Shorthand with a context.'''
		return self.getUser(ctx.author.id)


	# If we ever change the details on a card, we will have to call this
	def updateCard(self, oldUID: str, newCard: Card):
		for writer in self.writers:
			for card in writer.gachaCards:
				if(hash(card) == oldUID):
					writer.gachaCards.remove(card)
					break
			writer.gachaCards.add(hash(newCard))