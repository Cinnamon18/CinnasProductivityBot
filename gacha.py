import json
import random
import math
from card import Card
from user import User
from config import Config

class Gacha():	

	def __init__(self, enabledFranchises):
		self.cardsByUID = dict()
		self.cardsByRarity = dict()
		
		for rarity in Config.rarities:
			self.cardsByRarity[rarity] = []
		
		for franchise in enabledFranchises:
			

			with open(f"gachaAssets/{franchise}.json") as franchiseFile:
				cards = json.load(franchiseFile)

				for cardDict in cards:
					card = Card(cardDict)
					print(card)
					self.cardsByUID[card.uid] = card
					self.cardsByRarity[card.rarity].append(card)
						
		self.rateUpURs, self.rateUpSSRs = self.getRateUpCards()

				

	def soloPull(self, puller:User) -> (Card, bool):
		'''Performs a solo pull for the given user if they have enough crystals, and adds it to their inventory. If they don't have enough crystals, the method returns (None, None)'''
		if puller.crystals < Config.crystalsPerPull:
			return None, None

		cardRarity = random.choices(Config.rarities, Config.probabilities)
		cardRarity = "UR"

		card = None

		if cardRarity == "UR":
			if random.uniform(0, 1) < Config.rateUpURRates:
				card = random.choice(self.rateUpURs)
		elif cardRarity == "SSR":
			if random.uniform(0, 1) < Config.rateUpURRates:
				card = random.choice(self.rateUpSSRs)

		if card == None:
			card = random.choice(self.cardsByRarity[cardRarity])

		isDupe = card.uid in puller.gachaCardsUIDs
		if not isDupe: # Check should be redundant bc it's a set but just in case I change it to a list down the line and forget.
			puller.addCard(card)
		return card, isDupe

	def pullMultiple(self, puller:User, pulls):
		pulledCards = []
		for i in range(pulls):
			pulledCards.append(soloPull(puller))
		return pulledCards

	def getRateUpCards(self):		
		ursToPick = Config.rateUpURCount if len(self.cardsByRarity['UR']) > Config.rateUpURCount else len(self.cardsByRarity['UR'])
		ssrsToPick = Config.rateUpURCount if len(self.cardsByRarity['SSR']) > Config.rateUpURCount else len(self.cardsByRarity['SSR'])

		rateUpURs = random.choices(self.cardsByRarity['UR'], k=ursToPick)
		rateUpSSRs = random.choices(self.cardsByRarity['SSR'], k=ssrsToPick)
		return rateUpURs, rateUpSSRs
