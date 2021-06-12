# Ideally one day we'll put this in a json instead of compiled code but.
# Actually. This is python. There aren't builds. We can just swap out this file. Wtf.

class Config():
	dayResetTime = 5 # Daily reset is 1am EDT (5am UTC)\

	crystalsPerPull = 25
	rateUpURCount = 2
	rateUpURRates = 0.5
	rateUpSSRCount = 3
	rateUpSSRRates = 0.25

	pullsToSpark = 100
	coinsPerUnusedSpark = 10

	rarities = ["UR", "SSR", "SR", "R"]
	probabilities = [0.05, 0.1, 0.2, 0.8]

	saveFileName = "botSave.json"