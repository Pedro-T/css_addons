# css_addons
Some of my Counter-Strike: Source addons from a long time ago. Mostly what I created and worked on for a custom Counter-Strike: Source server and community back in 2006-2008 or so. The community and server are long gone and I doubt anyone is running these scripts any more.

If you actually still run CS:S and have a use for these, go ahead and use them. All require the Eventscripts addon framework to function. _Absolutely no support is given_ - I have not worked on these for fourteen years now.


### MarketMod
Adds a simple weapon menu that can be used at any time with the (default) chat command "!market"
* Supports every weapon in the game, but not armor or items
* Flag for using a cost of zero instead
* Requires both EventScripts and ES_Tools - I don't recall what minimum version of either

### A-Spawn
Adds a respawn command to CS:S that costs money to use
* Buy a respawn via !buyspawn
* Use a respawn when dead via !aspawn
* Limit maximum held respawns
* Set price of a respawn
* Requires both EventScripts and ES_Tools - I don't recall what minimum version of either

### Zombie Onslaught
The core addon from the NOTD custom server
* Transforms the AI team into zombies (AKA bots with knives and changed models / health / speed)
* Fast zombies with low health and smaller character models, large slow zombies with extra health, etc.
* Each map would proceed up to twenty rounds / levels, with each level bringing larger numbers of opponents as well as different mixtures of enemy types
* Boss round every five levels would create one particularly strong/fast/tough enemy and remove the rest
* Requires EventScripts-Python and ES_Tools

This is an early version of the mod and unfortunately the only one I still have. Later upgrades included exploding zombies, the ability for a random player or admin to play as the boss, and some other improvements as well as an associated (and lost to time) addon which tracked long term high scores and achievements (stored via SQLite database) on our servers. The final round, level 21, was designed as a bonus round where admins would take control of multiple 'boss' enemies with a shared health pool as final challenge.
