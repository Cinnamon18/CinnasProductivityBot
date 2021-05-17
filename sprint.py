from writer import Writer
from typing import Set
import enum

class Sprint():
	def __init__(self, serverUID, channel, startTime, sprintLength):
		self.serverUID = serverUID
		self.channel = channel
		self.startTime = startTime
		self.sprintLength = sprintLength
		self.participants: Set[Writer] = set()
		self.sprintPhase = SprintPhase.JOIN

class SprintPhase(enum.Enum):
	JOIN = 0,
	WRITE = 1,
	REPORT_WORDCOUNT = 2,