/*
 * Halfway through this project I realized I lost all will to do it properly.
 * Past this script INTO YOUR BROWSER CONSOLE asl;dkfj and copy paste the result into love_live.json.
 * I'm sorry. I don't wanna set up node / npm. And I don't wanna deal with python networking.
 */

fetch("https://schoolido.lu/api/cards/").then((response) => {
	response.json().then((loveLiveCards) => {
		let pageCount = Math.ceil(loveLiveCards.count / loveLiveCards.results.length);
		loadAllCards(pageCount)
	})
});

async function loadAllCards(pageCount) {
	let output = []

	// API is 1 indexed.
	for (let i = 1; i <= pageCount; i++) {
		let cards = await (await fetch(`https://schoolido.lu/api/cards/?page=${i}`)).json();
		console.log(cards)
		for (let card of cards.results) {
			if (!card.idol.main_unit || card.rarity == "N") {
				// It's not one of the main units like u's, aqours, etc. Skip the chaff.
				continue;
			}

			let ourCard = {}
			ourCard.uid = "love_live_" + card.id
			ourCard.franchise = "Love Live!"
			ourCard.img_url = card.english_card_idolized_image ? card.english_card_idolized_image : card.card_idolized_image
			ourCard.img_url = ourCard.img_url.replace("//i.schoolido.lu", "https://i.schoolido.lu")
			ourCard.character = `${card.idol.name.split(" ")[1]} ${card.idol.name.split(" ")[0]}` // Database provides names "surname, given name"
			ourCard.card_name = card.translated_collection ? card.translated_collection : ""
			ourCard.rarity = card.rarity // Hey, perfect mapping! What're the chances :b
			ourCard.element = card.attribute
			ourCard.mechanical_archetype = card.skill ? card.skill : ""
			ourCard.unit = card.idol.main_unit
			ourCard.credit = "idol.st"
			output.push(ourCard);
		}
	}

	console.log(JSON.stringify(output));
}

