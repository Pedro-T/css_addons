# Zombie Onslaught 3.1 by Pedro Teixeira

import es
import playerlib
import gamethread
import random
import repeat
import usermsg

info = es.AddonInfo()
info['name'] = "Zombie Onslaught" 
info['version'] = "3.1"
#info['url'] = "" 
info['description'] = "Night of the Dead's zombie vs humans gameplay mod" 

es.ServerVar("zo_version", info['version']).makepublic()

z_reserve = 0
z_display = 0
h_survivors = 0
currentLevel = 0
mdl = 0
h_team = 0
z_team = 0


estInstalled = bool(str(es.ServerVar('est_version')) != "0")

models = {
	1:"player/elis/uz1/uz1",
	2:"player/elis/uz5/uz5",
	3:"player/elis/uz7/uz7",
	4:"player/elis/uz1/uz1",
	5:"player/lextalionis/fatty/t_phoenix",
	6:"player/pil/fast_v5/pil_fast_v5",
	7:"player/slow/chainsaw/chainsaw",
	8:"player/slow/el_g_fix2/slow_gigante.mdl",
}

health = {
	1:120,
	2:130,
	3:140,
	4:150,
	5:300,
	6:70,
	7:220,
	8:15000,
	9:17000,
	10:20000,
	11:25000
}

speed = {
	1:1.1,
	2:1.2,
	3:1.1,
	4:1.15,
	5:0.9,
	6:1.5,
	7:1.3,
	8:1.3,
	9:1.4,
	10:1.5,
	11:1.6
}

levels = {
	1:"1: What's going on?",
	2:"2: ZOMBIES?!",
	3:"3: Zombies ate my neighbors!",
	4:"4: Zombies ARE my neighbors!!",
	5:"5: ",
	6:"6: ",
	7:"7: ",
	8:"8: ",
	9:"9: ",
	10:"10: ",
	11:"11: ",
	12:"12: ",
	13:"13: ",
	14:"14: ",
	15:"15: ",
	16:"16: ",
	17:"17: ",
	18:"18: ",
	19:"19: ",
	20:"20: Apocalypse",
	"Bonus":"Judgement Day"
}

humans = {
	"zo_metro":3,
	"zo_freeway":2,
	"de_dust":3,
	"de_dust2":2,
	"zh_jam":3,
	"cs_silenthill":3,
	"cs_northtower":3,
	"dotd_crookcounty":3,
	"de_deadblock":3,
	"de_nightmare":2,
	"de_livehouse":2,
	"de_residentevil2_v3":3,
	"cs_silenthill2":2
}

zombies = {
	"zo_metro":2,
	"zo_freeway":3,
	"de_dust":2,
	"de_dust2":3,
	"zh_jam":2,
	"cs_silenthill":2,
	"cs_northtower":2,
	"dotd_crookcounty":2,
	"de_deadblock":2,
	"de_nightmare":3,
	"de_livehouse":3,
	"de_residentevil2_v3":2,
	"cs_silenthill2":3
}

def load():
	global currentLevel
	currentLevel = 1
	if not estInstalled:
		es.ServerCommand("echo Error: ES_Tools not installed! (Error 1001)")
	es.ServerCommand("mp_limitteams 34")
	es.ServerCommand("bot_quota 34")
	es.ServerCommand("bot_join_after_player 0")
	es.ServerCommand("bot_add")
	es.ServerCommand("mp_autoteambalance 0")
	es.ServerCommand("bot_knives_only")
	es.ServerCommand("bot_quota_mode normal")
	es.ServerCommand("bot_prefix Infected")
	es.ServerCommand("bot_eco_limit 16001")
	es.ServerCommand("bot_allow_grenades 0")
	es.ServerCommand("bot_allow_pistols 0")
	es.ServerCommand("bot_allow_rifles 0")
	es.ServerCommand("bot_allow_sub_machine_guns 0")
	es.ServerCommand("bot_allow_shotguns 0")
	es.ServerCommand("bot_allow_snipers 0")
	es.ServerCommand("bot_allow_machine_guns 0")
	
	es.ServerCommand("exec downloads.cfg")
	es.ServerCommand("sv_alltalk 1")

def es_map_start(ev):
	global h_team, z_team
	es.ServerCommand("est_restrict =a flashbang")
	es.ServerCommand("est_restrict =a smokegrenade")
	if (humans.has_key(ev['mapname'])) and (zombies.has_key(ev['mapname'])):
		h_team = humans[ev['mapname']]
		z_team = zombies[ev['mapname']]
		if h_team == 2:
			es.ServerCommand("mp_humanteam 2")
			es.ServerCommand("bot_join_team 3")
			es.ServerCommand("est_restrict =ct hegrenade")
		elif h_team == 3:
			es.ServerCommand("mp_humanteam 3")
			es.ServerCommand("bot_join_team 2")
			es.ServerCommand("est_restrict =t hegrenade")
		else:
			es.msg("#green", "Error: undefined (Error 1102)")
	else:
		es.msg("#green", "Error: "+ev['mapname']+" is not supported by Zombie Onslaught (Error 1101)")

def round_start(ev):
	global h_survivors, z_reserve, bossLevel
	for userid in playerlib.getUseridList('#human,#alive'):
		h_survivors += 1
	z_reserve = generateArmy()
	startDisplayLoop()
	startEntityDelete()
	if currentLevel == 10:
		bossLevel(2)
	elif currentLevel == 20:
		bossLevel(4)
	if es.getUseridList():
		es.ServerCommand('es_xfire %s hostage_entity kill'%es.getUseridList()[0])

def player_spawn(ev):
	selectedPlayer = playerlib.getPlayer(ev['userid'])
	if selectedPlayer.attributes['steamid'] == "BOT":
		index = getIndex(currentLevel)
		selectedPlayer.set("model", models[index])
		selectedPlayer.set("health", health[index])
		selectedPlayer.set("speed", speed[index])
		es.ServerCommand("est_removeweapon %s 2"%ev['userid'])

def player_team(ev):
	if es.getplayersteamid(ev['userid']) == "BOT":
		if not es.getplayerteam(ev['userid']) == z_team:
			es.ServerCommand("est_team %s %s"%(ev['userid'], z_team))
	else:
		if not es.getplayerteam(ev['userid']) == 1:
			if not es.getplayerteam(ev['userid']) == h_team:
				es.ServerCommand("est_team %s %s"%(ev['userid'], h_team))

def player_death(ev):
	global z_reserve, h_survivors
	if ev['es_steamid'] == "BOT":
		if z_reserve > 0:
			es.ServerCommand("est_spawn "+ev['userid'])
			z_reserve -= 1
	#else:
		#user = playerlib.getPlayer(ev['userid'])
		#es.msg(user)
		#es.msg(user.attributes['name']+" has fallen in combat. He will be missed...")
	updateHud()

def round_end(ev):
	army = 0
	humans = 0
	for userid in playerlib.getUseridList('#bot,#alive'):
		army += 1
	for userid in playerlib.getUseridList('#human,#alive'):
		humans += 1
	army += z_reserve
	if army == 0:
		humansWin()
	elif humans == 0:
		zombiesWin()
	else:
		es.msg("#green", "Error: Zombie Onslaught cannot resolve the round! (Error 1301)")
	endDisplayLoop()
	endEntityDelete()

def item_pickup(ev):
	if ev['item'] == 'c4':
		es.ServerCommand('es_xfire %s weapon_c4 kill'%ev['userid'])

def bossLevel(lvl):
	global z_reserve
	z_reserve = 0
	available = playerlib.getUseridList('#bot')
	chosen = available.pop(random.randint(0,len(available)))
	boss = playerlib.getPlayer(chosen)
	boss.set("model",models[8])
	if lvl == 1:
		boss.set("health",health[8])
		boss.set("speed",speed[8])
	elif lvl == 2:
		boss.set("health",health[9])
		boss.set("speed",speed[9])
	elif lvl == 3:
		boss.set("health",health[10])
		boss.set("speed",speed[10])
	elif lvl == 4:
		boss.set("health",health[11])
		boss.set("speed",speed[11])
	for userid in playerlib.getUseridList('#bot'):
		if not userid == chosen:
			es.ServerCommand("est_slay %s"%userid)

def shakeScreen():
	usermsg.shake("#human", 1, 3)

def humansWin():
	global currentLevel
	usermsg.fade("#human", 10, 2, 10, 0, 255, 0)
	currentLevel += 1
	if (currentLevel == 21):
		currentLevel = 1
	# Option of bonus level, with admins on? TBD

def zombiesWin():
	global currentLevel
	usermsg.fade("#human", 10, 2, 10, 255, 0, 0)
	currentLevel -= 1
	if (currentLevel == 0):
		currentLevel = 1

	
def generateArmy():
	humans = es.getplayercount(h_team)
	army = currentLevel * 8
	temp = humans * 5
	army += temp
	return army

def getIndex(lvl):
	index = 1 # Default
	if (lvl == 1):
		index = 1
	elif (lvl == 2):
		index = 2
	elif (lvl == 3):
		index = random.randrange(1,3)
	elif (lvl == 4):
		index = 3
	elif (lvl == 5):
		index = random.randrange(3,4)
	elif (lvl == 6):
		index = random.randrange(2,4)
	elif (lvl == 7):
		index = 4
	elif (lvl == 8):
		index = random.randrange(3,5)
	elif (lvl == 9):
		index = random.randrange(1,5)
	# Skip 10, boss level
	elif (lvl == 11):
		index = 5
	elif (lvl == 12):
		index = random.randrange(1,6)
	elif (lvl == 13):
		index = 6
	elif (lvl == 14):
		index = random.randrange(5,7)
	elif (lvl == 15):
		index = random.randrange(3,7)
	elif (lvl == 16):
		index = random.randrange(1,7)
	elif (lvl == 17):
		index = 7
	elif (lvl == 18):
		index = random.randrange(6,8)
	elif (lvl == 19):
		index = random.randrange(1,8)
	# Skip 20, boss level
	return index
