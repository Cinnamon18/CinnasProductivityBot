import json
import random

class Gacha():
	enabledFranchises = set(["bang_dream", "love_live", "arknights"])
	cards = dict()
	
	rarities = ["UR", "SSR", "SR", "R"]
	probabilities = [0.05, 0.1, 0.2, 0.8]

	def __init__(self):
		for franchise in Gacha.enabledFranchises:
			
			for rarity in Gacha.rarities:
				Gacha.cards[rarity] = []

			with open(f"gachaAssets/{franchise}.json") as franchiseFile:
				cards = json.load(franchiseFile)

				for card in cards:
					for rarity in Gacha.rarities:
						if card['rarity'] == rarity:
							Gacha.cards[rarity].append(card)
				

	def soloPull(self):
		cardRarity = random.choices(Gacha.rarities, Gacha.probabilities)
		cardRarity = "UR"
		print(Gacha.cards[cardRarity])
		return random.choice(Gacha.cards[cardRarity])

	def pullMultiple(self, pulls):
		pulledCards = []
		for i in range(pulls):
			pulledCards.append(soloPull())
		return pulledCards
