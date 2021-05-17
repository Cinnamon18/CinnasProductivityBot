from writer import Writer

class BotState():
	def __init__(self):
		self.writers = dict()
		self.dailyMessageSent = False

		#TODO make this work in more than 1 server at once
		self.curSprint = None
		self.lastUsedChannel = None

		self.test = False

	def getUser(self, userId):
		'''Gets a user from the list of writers. If user does not exist, a new one will be created.'''
		if not userId in self.writers:
			self.writers[userId] = Writer(userId)
		
		return self.writers[userId]
	
	def getUserCtx(self, ctx):
		'''Shorthand with a context.'''
		return self.getUser(ctx.author.id)