/*
 * This script should be very similar to scrapeLoveLive.js bc both services use the same backing service.
 */

fetch("https://bandori.party/api/cards/").then((response) => {
	response.json().then((loveLiveCards) => {
		let pageCount = Math.ceil(loveLiveCards.count / loveLiveCards.results.length);
		loadAllCards(pageCount)
	})
});

async function loadAllCards(pageCount) {
	let output = []

	// API is 1 indexed.
	for (let i = 1; i <= pageCount; i++) {
		let cards = await (await fetch(`https://bandori.party/api/cards/?page=${i}`)).json();
		console.log(cards)
		for (let card of cards.results) {
			let ourCard = {}
			ourCard.uid = "bang_dream_" + card.id
			ourCard.franchise = "BanG Dream"
			ourCard.img_url = card.art_trained ? card.art_trained : card.art
			ourCard.character = bangDreamMemberIntToName[card.member]
			ourCard.card_name = card.name ? card.name : card.japanese_name
			ourCard.rarity = bangDreamRarityToCinnaRarity[card.i_rarity]
			ourCard.element = card.i_attribute
			ourCard.mechanical_archetype = card.i_skill_type
			ourCard.unit = bangDreamMemberIntToBand[card.member]
			ourCard.credit = "bandori.party"
			output.push(ourCard);
		}
	}

	console.log(JSON.stringify(output));
}

const bangDreamRarityToCinnaRarity = {
	4: "UR",
	3: "SSR",
	2: "R",
	1: "R"
};

// WHO ARE THE HIDDEN FIRST 5 BANG DREAM MEMBERS????
const bangDreamMemberIntToName = {
	6: "Kasumi Toyama",
	7: "Tae Hanazono",
	8: "Rimi Ushigome",
	9: "Saaya Yamabuki",
	10: "Arisa Ichigaya",
	11: "Ran Mitake",
	12: "Moca Aoba",
	13: "Himari Uehara",
	14: "Tomoe Udagawa",
	15: "Tsugumi Hazawa",
	16: "Kokoro Tsurumaki",
	17: "Kaoru Seta",
	18: "Hagumi Kitazawa",
	19: "Kanon Matsubara",
	20: "Misaki Okusawa",
	21: "Aya Maruyama",
	22: "Hina Hikawa",
	23: "Chisato Shirasagi",
	24: "Maya Yamato",
	25: "Eve Wakamiya",
	26: "Yukina Minato",
	27: "Sayo Hikawa",
	28: "Lisa Imai",
	29: "Ako Udagawa",
	30: "Rinko Shirokane",
	31: "Mashiro Kurata",
	32: "Touko Kirigaya",
	33: "Nanami Hiromachi",
	34: "Tsukushi Futaba",
	35: "Rui Yashio",
	36: "LAYER",
	37: "LOCK",
	38: "MASKING",
	39: "PAREO",
	40: "CHU²",
};

const bangDreamMemberIntToBand = {
	6: "Poppin' Party",
	7: "Poppin' Party",
	8: "Poppin' Party",
	9: "Poppin' Party",
	10: "Poppin' Party",
	11: "Afterglow",
	12: "Afterglow",
	13: "Afterglow",
	14: "Afterglow",
	15: "Afterglow",
	16: "Hello, Happy World",
	17: "Hello, Happy World",
	18: "Hello, Happy World",
	19: "Hello, Happy World",
	20: "Hello, Happy World",
	21: "Pastel Palettes",
	22: "Pastel Palettes",
	23: "Pastel Palettes",
	24: "Pastel Palettes",
	25: "Pastel Palettes",
	26: "Roselia",
	27: "Roselia",
	28: "Roselia",
	29: "Roselia",
	30: "Roselia",
	31: "Morfonica",
	32: "Morfonica",
	33: "Morfonica",
	34: "Morfonica",
	35: "Morfonica",
	36: "RAISE A SUILEN",
	37: "RAISE A SUILEN",
	38: "RAISE A SUILEN",
	39: "RAISE A SUILEN",
	40: "RAISE A SUILEN",
};