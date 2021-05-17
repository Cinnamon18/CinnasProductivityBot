import json
import random
import math
from card import Card
from writer import Writer

class Gacha():	
	rarities = ["UR", "SSR", "SR", "R"]
	probabilities = [0.05, 0.1, 0.2, 0.8]

	def __init__(self, enabledFranchises):
		self.cardsByUID = dict()
		self.cardsByRarity = dict()
		
		for franchise in enabledFranchises:
			
			for rarity in Gacha.rarities:
				self.cardsByRarity[rarity] = []

			with open(f"gachaAssets/{franchise}.json") as franchiseFile:
				cards = json.load(franchiseFile)

				for cardDict in cards:
					card = Card(cardDict)
					self.cardsByUID[hash(card)] = card

					for rarity in Gacha.rarities:
						if card.rarity == rarity:
							self.cardsByRarity[rarity].append(card)
				

	def soloPull(self, puller:Writer) -> (Card, bool):
		cardRarity = random.choices(Gacha.rarities, Gacha.probabilities)
		cardRarity = "UR"
		card = random.choice(self.cardsByRarity[cardRarity])
		isDupe = hash(card) in puller.gachaCardsUIDs
		print(hash(card))
		print([id for id in puller.gachaCardsUIDs])
		puller.addCard(card)
		return card, isDupe

	def pullMultiple(self, puller:Writer, pulls):
		pulledCards = []
		for i in range(pulls):
			pulledCards.append(soloPull(puller))
		return pulledCards
