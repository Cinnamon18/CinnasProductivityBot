import math

class User:
	def __init__(self, discordId):
		self.discordId = discordId

		self.goals = []
		self.isStreakTracking = True
		self.streakLength = 0
		
		self.crystals = 0
		self.coins = 0
		
		self.gachaCardsUIDs = set()

	def __hash__(self):
		return hash(self.discordId)

	def getUnaccomplishedGoals(self):
		unaccomplished = [goal for goal in self.goals if not goal.didGoalToday]
	
	# 25 at streak 0, then increases as a (weighted) linearithmic.
	# https://www.wolframalpha.com/input/?i=plot+%28log1.5%28x+%2B+1%29+*+10%29+*+0.8+%2B+%282x%29+*+0.2+from+0+to+100
	def calculateDailyRewards(self):
		logrithmicTerm = math.log(self.streakLength + 1, 1.5) * 10
		linearTerm = 2 * self.streakLength
		return math.ceil(25 + (0.8 * logrithmicTerm) + (0.2 * linearTerm))

	def addCard(self, card):
		self.gachaCardsUIDs.add(card.uid)