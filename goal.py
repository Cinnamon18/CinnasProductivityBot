from botIntegration import BotIntegration, Sprinto

class Goal():

	def __init__(self, name, botIntegration: BotIntegration = None):
		self.name = name
		self.didGoalToday = False
		self.botIntegration = botIntegration