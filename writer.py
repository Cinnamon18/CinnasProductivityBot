import math

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

		self.gachaCardsUIDs = set()

	def __hash__(self):
		return hash(self.discordId)

	
	# 25 at streak 0, then increases as a linearithmic.
	# https://www.wolframalpha.com/input/?i=plot+%28log1.5%28x+%2B+1%29+*+10%29+*+0.8+%2B+%282x%29+*+0.2+from+0+to+100
	def calculateDailyRewards(self):
		logrithmicTerm = math.log(self.streakLength + 1, 1.5) * 10
		linearTerm = 2 * self.streakLength
		return 25 + (0.8 * logrithmicTerm) + (0.2 * linearTerm)

	def addCard(self, card):
		self.gachaCardsUIDs.add(hash(card))