from botIntegration import BotIntegration, Sprinto

class Goal():

	def __init__(self, name, shorthand, botIntegration: BotIntegration = None):
		self.name = name
		self.shorthand = shorthand if shorthand else None
		self.didGoalToday = False
		self.botIntegration = botIntegration