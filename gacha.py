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
			

			with open(f"gachaAssets/{franchise}.json", encoding="utf8") as franchiseFile:
				cards = json.load(franchiseFile)

				for cardDict in cards:
					card = Card(cardDict)
					self.cardsByUID[card.uid] = card
					self.cardsByRarity[card.rarity].append(card)
						
		self.rateUpURs, self.rateUpSSRs = self.generateRateUpCards()

	def checkDupe(self, puller:User, card:Card) -> bool:
		return card.uid in puller.gachaCardsUIDs

	def spark(self, puller:User, card:Card):
		if puller.sparks < Config.pullsToSpark:
			return None 
		else:
			isDupe = self.checkDupe(puller, card)
			if not isDupe: # Check should be redundant bc it's a set but just in case I change it to a list down the line and forget.
				puller.addCard(card)
			return card, isDupe


	def soloPull(self, puller:User) -> (Card, bool):
		'''Performs a solo pull for the given user if they have enough crystals, and adds it to their inventory. If they don't have enough crystals, the method returns (None, None)'''
		if puller.crystals < Config.crystalsPerPull:
			return None, None

		cardRarity = random.choices(Config.rarities, Config.probabilities, k=1)
		cardRarity = cardRarity[0]

		card = None

		if cardRarity == "UR":
			if random.uniform(0, 1) < Config.rateUpURRates:
				card = random.choice(self.rateUpURs)
		elif cardRarity == "SSR":
			if random.uniform(0, 1) < Config.rateUpURRates:
				card = random.choice(self.rateUpSSRs)

		if card == None:
			card = random.choice(self.cardsByRarity[cardRarity])

		isDupe = self.checkDupe(puller, card)
		if not isDupe: # Check should be redundant bc it's a set but just in case I change it to a list down the line and forget.
			puller.addCard(card)
		return card, isDupe

	def pullMultiple(self, puller:User, pulls):
		pulledCards = []
		for i in range(pulls):
			pulledCards.append(soloPull(puller))
		return pulledCards

	def generateRateUpCards(self):		
		ursToPick = Config.rateUpURCount if len(self.cardsByRarity['UR']) > Config.rateUpURCount else len(self.cardsByRarity['UR'])
		ssrsToPick = Config.rateUpURCount if len(self.cardsByRarity['SSR']) > Config.rateUpURCount else len(self.cardsByRarity['SSR'])

		rateUpURs = random.sample(self.cardsByRarity['UR'], k=ursToPick)
		rateUpSSRs = random.sample(self.cardsByRarity['SSR'], k=ssrsToPick)
		return rateUpURs, rateUpSSRs

	def fuzzySearchForCard(self, searchString:str, rateUpOnly:bool) -> Card:
		cardlist = self.rateUpURs + self.rateUpSSRs if rateUpOnly else self.cardsByUID 

		for card in cardlist:
			if card.uid == searchString:
				return card
		
		for card in cardlist:
			if card.character.casefold() == searchString.casefold():
				return card

		return None