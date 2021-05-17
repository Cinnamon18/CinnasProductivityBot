import discord
from writer import Writer

class Card():

	rarityColorTable = {
		'UR': discord.Colour.gold(),
		'SSR': discord.Colour.purple(),
		'SR': discord.Colour.blue(),
		'R': discord.Colour.lighter_grey(),
	}

	pullNewText = {
		'UR': "New UR!!!",
		'SSR': "New SSR!!",
		'SR': "New SR!",
		'R': "New R!",
	}

	pullDupeText = {
		'UR': "Dupe UR!",
		'SSR': "Dupe SSR!",
		'SR': "Dupe SR!",
		'R': "Dupe R!",
	}
	

	def __init__(self, cardJson):
		self.franchise = cardJson['franchise']
		self.img_url = cardJson['img_url']
		self.character = cardJson['character']
		self.card_name = cardJson['card_name']
		self.rarity = cardJson['rarity']
		self.element = cardJson['element']
		self.mechanical_archetype = cardJson['mechanical_archetype']
		self.unit = cardJson['unit']
	
	def toDiscordEmbed(self, isDupe):		
		titleText = Card.pullNewText[self.rarity] if not isDupe else Card.pullDupeText[self.rarity]
		titleText = f'{titleText} {self.character}'

		embed = discord.Embed(
			title=titleText,
			colour=Card.rarityColorTable[self.rarity],
			description=f'''Franchise: {self.franchise}
Card Name: {self.card_name}
Rarity: {self.rarity}
Element: {self.element}
Mechanical Archetype: {self.mechanical_archetype}
Unit: {self.unit}'''
		)
		embed = embed.set_image(url=self.img_url)
		return embed