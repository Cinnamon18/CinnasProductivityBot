# One day we should probably use JSON so users can't inject code. But for now.

import pickle
from types import SimpleNamespace

class Serialization(bot):
	@staticmethod
	def saveData(bot):
		pickle.dump(bot, open("savedBotState.p", "wb"))
		print("Saved successfully!")

	@staticmethod
	def loadBot(bot) -> BotState:
		botState = pickle.loads( open ("savedBotState.p", "rb") )
		print("Loaded data successfully!")
		return botState