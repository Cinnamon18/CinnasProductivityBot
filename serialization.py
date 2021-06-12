# One day we should probably use JSON so users can't inject code. But for now.
# TODO before widespread deployment.

from types import SimpleNamespace
from botState import BotState
import jsonpickle

class Serialization():
	@staticmethod
	def saveData(botState, fileName):
		with open(fileName, "w", encoding="utf8") as botStateFile:
			# Channel is some complicated datatype pickle doesn't wanna serialize.
			tempLastChannel = botState.lastUsedChannel
			botState.lastUsedChannel = None
			botStateJson = jsonpickle.encode(botState)
			botStateFile.write(botStateJson)
			botState.lastUsedChannel = tempLastChannel

			print("Saved successfully!")
			return botState



	@staticmethod
	def loadData(fileName) -> BotState:
		try:
			with open(fileName, "r", encoding="utf8") as botStateFile:
				botState = jsonpickle.decode(botStateFile.read())
				print("Loaded data successfully!")
				return botState
		except FileNotFoundError as error:
			print(f"Couldn't find file {fileName}")
			print(error)
			return None
		except json.decoder.JSONDecodeError as decodeError:
			print("Unable to load bot save. Making new bot.")
			return None
			