# Cinnas Productivity Bot
A productivity bot!

### Integrations
Integrations allow other bots to automatically mark a  daily goal complete. 


## Dev Zone

### How to Run
 - Run `python -m pip install -r requirements.txt`
 - Change the token in .env to the bot's real token, which you can get on the discord developer page > Application > Bot > Token
	 - If you're deploying, you can just configure the env variable and the .env will be ignored.
 - You probably wanna `git update-index --skip-worktree .env`

### Card Properties
Cards are stored as JSON objects with the following attributes. All keys are required, use an empty string where a reasonable value cannot be produced. Additionally, the `uid` and `rarity` keys require a value for all cards. This bot is targeted at english speakers, and will attempt to use english wherever possible.

 - uid - The card's primary key. Can be any unique string. The format `franchise_all_lower_without_punctuation_index` is encouraged. For example, `love_love_0`, followed by `love_live_1`, etc.
 - franchise - The source franchise for the character. For example, `Love Live!` or `Granblue Fantasy`
 - img_url - An image URl, perferably from a CDN that won't feel the hot linking :^) (ie, for a bandori card, better you drain twitter's resources than those of fan websites like bandori.party or bestdori.com)
 - character - Name of the character. Given name, then surname. For example, `Maki Nishikino` or `Sandalphon`
 - card_name - Name of the card. For games with delayed releases between servers, authoratative english fan translations (wiki, popular fan resource sites) > Japanese official names where possible.
 - rarity - The cinnabot standardized rarity system recognizes 4 rarities: `UR`, `SSR`, `SR`, and `R`. The draw rates are currently at 5%, 10%, 20%, and 80% respectively. Attempt to match from the source franchise on the basis of rarity caregories and those draw rates.
	 - For example, the original SIF maps perfectly onto the given rarities. Granblue has an `SSR` rate of 3% and an `SR` rate of 15%. We map granblue `SSR`s onto a standard `UR`. The granblue `SR` is equal distance from the standard `SSR` and `SR`, so we must make a judgement call. I have decided to map it onto the standard `SR` because this gacha aims to be relatively generous with it's rates.
 - element - Many games have a concept of element. Granblue has wind, fire, water, earth, dark, light. Bandori has powerful, cool, pure, happy.
 - mechanical_archetype - A higher level mechanical description of the card. Granblue has attackers, defenders, healers, and special units. Arknights has defenders, guards, arts users, etc. SIF has healers, scorers, and perfect lockers (and some others now? I've dropped the game.)
 - unit - The "group" this character is part of. This could be an idol unit, a band, a political faction, etc.

 As this gacha is cross franchise, the above attributes will not perfectly match every franchise's langauge or structure. That's okay! Just follow the examples for a franchise, and if you're making a few franchise, use your judgement.


### Misc
 - Release branch is autodeployed to [https://cinnaswritingbot.azurewebsites.net](https://cinnaswritingbot.azurewebsites.net)