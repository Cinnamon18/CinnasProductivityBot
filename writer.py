class Writer:
	def __init__(self, discordId):
		self.discordId = discordId

		self.didWriteToday = False
		self.isStreakTracking = False
		self.streakLength = 0
		
		self.crystals = 0
		self.coins = 0
		
		self.currentSprintStartingWords = 0
		self.currentSprintWords = 0

	def __hash__(self):
		return hash(self.discordId)