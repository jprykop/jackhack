#!/usr/bin/python

import os
import random
import re

class JackHack(object):
	def __init__(self):
		self.player = JackHack.Player(self)
		self.day = JackHack.Day(self)
		self.totalsteps = 100
		self.elements = [
			JackHack.Element('concrete','in a parking lot','slack','Bob','rhinestone','pavement','Slackers'),
			JackHack.Element('time','in another dimension','warp','Cthulu','quantum','theoretical','Shoggoths'),
			JackHack.Element('cheese','on the moon','cheddar','Ur','meteor','moon','Aliens'),
			JackHack.Element('clouds','in the sky','fog','Lucy','diamond','sky','Hippies'),
			JackHack.Element('fire','on a volcano','magma','Ifrit','ruby','volcano','Firemen'),
			JackHack.Element('waves','at sea','aguaga','Poseidon','water','sea','Pirates'),
			JackHack.Element('flowers','in a poppy field','sleep','Elphaba','emerald','fields','Lollipops'),
			JackHack.Element('sand','in the desert','sandstorm','Ra','amber','desert','Fremen'),
			JackHack.Element('ice','in the arctic','ice','Shiva','ice','arctic','Vikings'),
			JackHack.Element('rocks','in the mountains','quake','Buddha','stone','mountains','Masons'),
			JackHack.Element('mud','in a swamp','muck','Yoda','lucasite','swamp','Lizardmen'),
			JackHack.Element('darkness','underground','hole','Hades','black','caverns','Morlocks'),
			JackHack.Element('trees','in the forest','leaf','Treebush','wood','forest','Hoods'),
			JackHack.Element('grass','on the prairie','mow','Laura','glass','prairie','Barbarians')
		]
		self.monstertypes = [
			'yeti',
			'dinosaur',
			'dragon',
			'demon',
			'giant',
			'cockatrice',
			'gargoyle',
			'vampire',
			'werewolf',
			'zombie',
			'troll',
			'ogre',
			'goblin',
			'blob'
		]
# 'basilisk',
# 'beholder',
# 'cyclops',
# 'griffon',
# 'golem',
# 'mind flayer',
# 'lich',
# 'skeleton',
# 'wraith',
# 'ghost',
# 'ghoul',
# 'gelatinous cube',
# 'ooze',
# 'elemental',
# 'orc',
# 'banshee',
# 'hag',
# 'drow',
	def act(self,action,*args):
		self.day.results.append(JackHack.Action(self,action,args))
	def getcritter(self):
		return random.choice(['wolf','spider','rat','bat','snake'])
	def wrand(self,somelist,invert=False):
		c = random.randrange(sum(range(len(somelist))))
		s = 0
		for i in range(0,len(somelist)):
			s += i
			if c <= s:
				if invert:
					return somelist[-i]
				else:
					return somelist[i]
	def attackroll(self,attacker,target):
		if random.randrange(attacker.power(target)+target.power(attacker)) < attacker.power(target):
			return True
		else:
			return False
	def skillroll(self,job):
		if self.day.element in job.weak:
			return False
		if self.day.element in job.strong or random.randrange(self.day.level) < job.level:
			return True
		else:
			return False
	def addstrength(self,element,target):
		if not element in target.strong:
			if element in target.weak:
				target.weak.remove(element)
			else:
				target.strong.append(element)
	def addweakness(self,element,target):
		if not element in target.weak:
			if element in target.strong:
				target.strong.remove(element)
			else:
				target.weak.append(element)
	def addattack(self,element,target):
		if not element in target.attack:
			target.attack.append(element)
	def savegame(self):
		return (self.player.name,self.player.title(),self.player.gold,self.mom())
	def mom(self):
		if not self.day.totalgold:
			return 0
		else:
			return self.player.gold * 100 / self.day.totalgold
	class Error(Exception):
		errors = {
			0 : "Name must contain only word characters",
			1 : "Name must be 16 characters or less"
		}
		def __init__(self,num):
			self.num = num
		def __str__(self):
			return JackHack.Error.errors[self.num] or "Unknown Error"
	class Fatal(Exception):
		errors = {
			0 : "Day ended without being played",
			1 : "Action does not exist",
			2 : "No offer has been made"
		}
		def __init__(self,num):
			self.num = num
		def __str__(self):
			return JackHack.Fatal.errors[self.num] or "Unknown Fatal Error"
	class Player(object):
		def __init__(self,game):
			self.game = game
			self.name = 'Jack'
			self.health = 1
			self.gold = 0
			self.jobs = (
				JackHack.Warrior(game),
				JackHack.Healer(game),
				JackHack.Thief(game),
				JackHack.Wizard(game),
				JackHack.Ranger(game),
				JackHack.Scholar(game),
				JackHack.Druid(game),
				JackHack.Artist(game)
			)
			self.gems = self.jobs[0].attack
			self.healer = self.jobs[1]
			self.gods = self.jobs[1].strong
			self.thief = self.jobs[2]
			self.wanted = self.jobs[2].weak
			self.guilds = self.jobs[2].strong
			self.spells = self.jobs[3].attack
			self.maps = self.jobs[4].strong
			self.scholar = self.jobs[5]
			self.art = []
			self.scrolls = []
			self.dead = False
			self.sacrifice = 0
			self.monsterknowledge = []
			self.studentloan = 0
			self.pets = []
			self.__topjobs = []
			for job in self.jobs:
				self.__topjobs.append(job)
		def __str__(self):
			return self.name + ' ' + self.title()
		def title(self):
			topjobs = self.topjobs()
			daynum = self.game.day.level - 1
			title = ''
			if daynum:
				for den in range(2,len(topjobs)+1):
					if topjobs[0].experience / float(daynum) >= 1 / float(den):
						ratio = 1 / float(den + 1)
						break
				titlecount = 0
				for job in topjobs:
					if job.experience / float(daynum) >= ratio:
						titlecount += 1
						if title:
							title += '/'
						title += job.name
				if titlecount == len(topjobs):
					title = 'of All Trades'
				else:
					title = 'the ' + title
			else:
				title = 'the Unknown'
			return title
		def rename(self,newname):
			if newname:
				if re.search('\W',newname):
					raise JackHack.Error(0)
				if len(newname) > 16:
					raise JackHack.Error(1)
				self.name = newname
		def topjobs(self):
			self.__topjobs.sort(lambda x,y: y.experience - x.experience)
			return self.__topjobs
		def getpowerpet(self,target=None):
			if not self.pets:
				return None
			self.pets.sort(lambda x,y: y.power(target) - x.power(target))
			out = self.pets[0]
			self.sortpets()
			return out
		def getrichpet(self):
			if not self.pets:
				return None
			self.pets.sort(lambda x,y: y.gold - x.gold)
			out = self.pets[0]
			self.sortpets()
			return out
		def addpet(self,newpet):
			self.pets.append(newpet)
			self.sortpets();
		def killpet(self,doomedpet):
			self.pets.remove(doomedpet)
		def sortpets(self):
			self.pets.sort(lambda x,y: y.power() - x.power())
	class Element(object):
		def __init__(self,resist,terrain,spell,god,gem,somemap,guild):
			self.resist = resist
			self.terrain = terrain
			self.spell = spell
			self.god = god
			self.gem = gem
			self.map = somemap
			self.guild = guild
	class Town(object):
		def __init__(self,day):
			if not day.lastday:
				self.gold = random.randint(1,day.level)
			else:
				self.gold = day.level
	class Day(object):
		def __init__(self,game):
			self.totalgold = 0
			self.todaygold = 0
			self.game = game
			self.level = 0
			self.monster = None
			self.town = None
			self.results = True
		def __iter__(self):
			return self
		def __str__(self):
			return str(self.level)
		def next(self):
			self.totalgold += self.todaygold
			self.todaygold = 0
			if self.game.player.dead:
				raise StopIteration
			if self.level >= self.game.totalsteps:
				raise StopIteration
			if not self.results:
				raise JackHack.Fatal(0)
			self.level += 1
			self.results = []
			if self.level == self.game.totalsteps:
				self.lastday = True
			else:
				self.lastday = False
			self.monster = None
			if self.lastday or random.randrange(self.game.totalsteps) < self.level:
				self.monster = JackHack.Monster(self.game)
				self.todaygold += self.monster.gold
			self.town = None
			if self.lastday or random.randrange(self.game.totalsteps) >= self.level:
				self.town = JackHack.Town(self)
				self.todaygold += self.town.gold
			if self.lastday:
				self.element = self.game.elements[0]
			else:
				self.element = self.game.wrand(self.game.elements)
			return self
		def possible(self):
			player = self.game.player
			monster = self.monster
			town = self.town
			warriortext = ''
			healertext = ''
			thieftext = ''
			wizardtext = ''
			rangertext = ''
			scholartext = ''
			druidtext = ''
			artisttext = ''
			if monster:
				thieftext += 'Thief might steal from the monster!\n'
				possmon = self.level
				if monster.name in player.monsterknowledge:
					possmon = monster.level
				if player.health >= possmon:
					warriortext += 'Warrior will win a fight!\n'
				else:
					if not player.pets:
						thieftext += 'Thief might lose all gold!\n'
					warriortext += 'Warrior might win a fight!\n'
				if player.health > 1:
					wizardtext += 'Wizard might win a fight!\n'
				rangertext += 'Ranger might win a fight!\n'
				possmon = 1
				if monster.name in player.monsterknowledge:
					possmon = monster.level
				if player.health > possmon:
					druidtext += 'Druid might make a friend!\n'
					if player.pets:
						druidtext += 'Druid might lose all pets!\n'
				if monster.name not in player.art:
					artisttext += 'Artist will paint the monster!\n'
				if monster.name not in player.monsterknowledge:
					if player.health > 1 or player.pets:
						scholartext += 'Scholar will learn about the monster!\n'
					else:
						scholartext += 'Scholar might learn about the monster!\n'
				if player.pets:
					thieftext += 'Thief might lose a pet!\n'
					scholartext += 'Scholar might lose a pet!\n'
			if town:
				posstown = self.level
				if self.element in player.guilds:
					posstown = town.gold
				if self.element in player.wanted:
					if player.gold >= posstown:
						thieftext += 'Thief can shop!\n'
				else:
					if (self.element in player.guilds) or (player.thief.level >= posstown):
						thieftext += 'Thief will steal from the town!\n'
					else:
						thieftext += 'Thief might steal from the town!\n'
					if player.gold >= self.level*2:
						thieftext += 'Thief can shop!\n'
				warriortext += 'Warrior will heal!\n'
				if (not monster) and (player.gold >= len(player.gems) + 1):
					warriortext += 'Warrior can shop!\n'
				wizardtext += 'Wizard will heal!\n'
				if (not monster) and (player.gold >= len(player.spells) + 1):
					wizardtext += 'Wizard can shop!\n'
				rangertext += 'Ranger will heal!\n'
				if player.gold >= self.level * 2:
					rangertext += 'Ranger can shop!\n'
				if player.gold >= player.scholar.level * 2:
					if (not monster) or (player.health > self.level):
						scholartext += 'Scholar can shop!\n'
					else:
						scholartext += 'Scholar can maybe shop!\n'
				else:
					if (not monster) or (player.health > self.level):
						scholartext += 'Scholar can get paid!\n'
					else:
						scholartext += 'Scholar can maybe get paid a pittance!\n'
				if player.scrolls:
					if (not monster) or (player.health > self.level):
						scholartext += 'Scholar can identify scrolls!\n'
					else:
						scholartext += 'Scholar can maybe identify scrolls!\n'
				if player.pets:
					druidtext += 'Druid can shop!\n'
				elif player.gold >= self.level:
					druidtext += 'Druid can shop!\n'
			healertext += 'Healer will heal!\n'
			if (self.element in player.gods) or (town and player.gold) or (player.healer.level >= self.level):
				if player.pets and not player.gold:
					healertext += 'Healer will lose a pet!\n'
			else:
				if player.pets and not player.gold:
					healertext += 'Healer might lose a pet!\n'
			if not (town or monster):
				rangertext += 'Ranger will heal!\n'
				if self.element not in player.maps:
					rangertext += 'Ranger will learn the terrain!\n'
				elif player.pets:
					for pet in player.pets:
						if not pet.isknown():
							rangertext += 'Ranger will learn about a pet!\n'
							break
			if not town:
				if player.scholar.level >= self.level:
					scholartext += 'Scholar will find a scroll!\n'
				else:
					scholartext += 'Scholar might find a scroll!\n'
			if self.element.map not in player.art:
				artisttext += 'Artist will paint the landscape!\n'
			return warriortext + healertext + thieftext + wizardtext + rangertext + scholartext + druidtext + artisttext
	class Character(object):
		def __init__(self,game):
			self.game = game
			self.strong = []
			self.weak = []
			self.attack = []
		def __str__(self):
			return self.name
		def power(self,you=None):
			power = self.level
			if you:
				for att in self.attack:
					if att in you.weak:
						power = power * 2
			if self.game.day.element in self.strong:
				power = power * 2
			if self.game.day.element in self.weak:
				power = int(power / 2)
			if not power:
				power = 1
			return power
	class Monster(Character):
		def __init__(self,game):
			JackHack.Character.__init__(self,game)
			self.game = game
			if not game.day.lastday:
				self.level = random.randint(1,game.day.level)
				self.name = game.wrand(game.monstertypes)
				game.addstrength(game.wrand(game.elements),self)
				game.addweakness(game.wrand(game.elements),self)
			else:
				self.level = game.day.level
				self.name = 'final boss'
				game.addstrength(game.elements[0],self)
				game.addweakness(game.elements[1],self)
			self.health = self.level
			self.gold = self.level
		def isknown(self):
			if self.name in self.game.player.monsterknowledge:
				return True
			else:
				return False
		def whatknown(self):
			out = ''
			if self.name in self.game.player.monsterknowledge:
				out += str(self.health) + '/' + str(self.level)
				if self.weak:
					out += '/' + str(self.weak[0].resist).lower()
				if self.strong:
					out += '/' + str(self.strong[0].resist).upper()
			return out
	class Action(object):
		def __init__(self,game,action,args):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			if not action:
				self.text = 'You gain nothing but experience!  Lame!'
			elif action == 'artist-element':
				self.text = 'You paint a picture of the {0}!'.format(day.element.map)
				player.art.append(day.element.map)
			elif action == 'artist-monster':
				self.text = 'You paint a picture of the {0}!'.format(monster.name)
				player.art.append(monster.name)
			elif action == 'artist-town':
				self.text = 'You try to sell your paintings in town, but no one is buying!'
			elif action == 'bounty':
				self.text = 'For killing the {0}, the townspeople pay you {1} gold!'.format(monster.name,town.gold)
				player.gold += town.gold
			elif action == 'caught':
				self.text = 'You got caught!  The Guild of {0} will now be extra wary of you!'.format(day.element.guild)
			elif action == 'clearname':
				self.text = 'A corrupt official offers to clear your name for {0} gold!'.format(day.level)
			elif action == 'die':
				self.text = 'You die!  The {0} plunders your corpse!'.format(monster.name)
				player.dead = True
				player.gold = 0
			elif action == 'dodge':
				self.text = 'The {0} attempts to strike you, but misses!'.format(monster.name)
			elif action == 'dodgedistant':
				self.text = 'The {0} lashes out at you, forcing you to keep your distance!'.format(monster.name)
			elif action == 'eat':
				self.text = 'The succulent roast beast restores {0} health!'.format(monster.level)
				player.health += monster.level
			elif action == 'escape':
				self.text = 'You retreat to tend to your injuries!'
				player.health = 1
			elif action == 'escape-magic':
				self.text = 'Arcane magic whisks you from the brink of death!'
				player.health = 1
			elif action == 'fizzle':
				self.text = 'You try to cast a spell, but it fizzles!'
			elif action == 'flee':
				self.text = 'You flee in terror!'
			elif action == 'freeheal':
				self.text = 'A great voice from the heavens proclaims...'
				self.text += '\nTHIS ONE IS ON THE HOUSE!'
				player.health += 1
			elif action == 'glowgem':
				self.text = 'The {0} gem in your sword begins to glow!'.format(args[0])
			elif action == 'hadoken':
				self.text = 'You blast the {0} with a deadly {1} spell!'.format(monster.name,args[0])
				monster.health = 0
			elif action == 'heal':
				self.text = '{1} grants you {0[0]} health!'.format(args,day.element.god)
				player.health += args[0]
				self.text += '\nTo show your gratitude, you sacrifice {0[0]} gold!'.format(args)
				player.gold -= args[0]
				player.sacrifice += args[0]
			elif action == 'healtemple':
				self.text = 'You pay the priests at the temple of {0} to pray on your behalf!'.format(day.element.god)
				self.text += '\n{0[0]} gold for {0[0]} health is a fair price, but your soul feels empty!'.format(args)
				player.health += args[0]
				player.gold -= args[0]
				player.sacrifice += args[0]
			elif action == 'hunt':
				self.text = "Bullseye!  Looks like it's {0} for dinner tonight!".format(monster.name)
				monster.health = 0
			elif action == 'hunt-nature':
				self.text = 'You find a small fuzzy {0} to kill and eat.  +1 health!'.format(game.getcritter())
				player.health += 1
			elif action == 'inn':
				self.text = 'The inn here only costs {0} gold a night!'.format(day.level*2)
			elif action == 'joinguild':
				self.text = 'The Guild of {0} invites you to join for {1} gold!'.format(day.element.guild,day.level*2)
			elif action == 'learn':
				self.text = "You watch the {0[0]} closely and learn its ways!".format(args)
				game.player.monsterknowledge.append(args[0])
			elif action == 'loseallgold':
				self.text = 'The {0} knocks you out cold and plunders your corpse!  Lose all your gold!'.format(monster.name)
				player.health = 1
				player.gold = 0
			elif action == 'manatap':
				self.text = 'You tap yourself for mana! (-1 Health)'
				player.health -= 1
			elif action == 'map':
				self.text = "You make a map of the {0}!".format(day.element.map)
			elif action == 'monsterdies':
				self.text = 'The {0} dies!'.format(monster.name)
			elif action == 'monsterstrike':
				self.text = 'The {0} strikes you for {1[0]} damage!'.format(monster.name,args)
				player.health -= args[0]
			elif action == 'noheal':
				self.text = 'No one answers your prayers!'
			elif action == 'petattack':
				pet = args[0]
				self.text = 'Your {0.name} strikes the {1} for {0.level} damage!'.format(pet,monster.name)
				monster.health -= pet.level
			elif action == 'petbuyoffer':
				somepet = args[0][1]
				somepetname = somepet.name
				if somepet.isknown():
					somepetname += ' ({0})'.format(somepet.whatknown())
				somepetcost = args[0][2]
				self.text = "The local zookeeper offers to sell you a {0} for {1} gold!".format(somepetname,somepetcost)
			elif action == 'petcapture':
				self.text = "You've got a new pet {0.name}".format(monster)
				if monster.isknown():
					self.text += "({0})".format(monster.whatknown())
				self.text += '!'
				player.addpet(monster)
			elif action == 'petcapturefail':
				self.text = "You try to befriend the {0} but it only seems interested in eating you!".format(monster.name)
			elif action == 'petdeath':
				self.text = "Your {0} dies!".format(args[0].name)
				game.player.killpet(args[0])
			elif action == 'petdefend':
				self.text = "Your pet {0} jumps forward to defend you!".format(args[0].name)
			elif action == 'petdistract':
				self.text = "Your pet {0} distracts the {1}!".format(player.getpowerpet(monster).name,monster.name)
			elif action == 'petlearn':
				self.text = "You watch your pet {0} closely and learn its ways!".format(args[0].name)
				game.player.monsterknowledge.append(args[0].name)
			elif action == 'petnotpresent':
				self.text = "You don't feel healthy enough to make new friends!"
			elif action == 'petoffer':
				somepet = args[0][1]
				somepetname = somepet.name
				if somepet.isknown():
					somepetname += '({0})'.format(somepet.whatknown())
				somepetcost = args[0][2]
				self.text = "The local zookeeper offers to buy your {0} for {1} gold!".format(somepetname,somepetcost)
			elif action == 'petsacrifice':				
				somepet = player.getrichpet()
				somepetname = somepet.name
				if somepet.isknown():
					somepetname += ' ({0})'.format(somepet.whatknown())
				self.text = '{1} grants you {0} health!'.format(somepet.gold,day.element.god)
				player.health += somepet.gold
				self.text += '\nTo show your gratitude, you sacrifice your {0}!'.format(somepet.name)
				player.sacrifice += somepet.gold
				game.player.killpet(somepet)
			elif action == 'petstrike':
				self.text = 'The {0.name} strikes your {1[0].name} for {0.level} damage!'.format(monster,args)
				args[0].health -= monster.level
			elif action == 'plunder':
				self.text = 'You plunder {0} gold from the {1}!'.format(monster.gold,monster.name)
				player.gold += monster.gold
			elif action == 'pray':
				self.text = 'You pray to the gods!'
			elif action == 'rest':
				self.text = 'The townsfolk grant you respite, +1 health!'
				player.health += 1
			elif action == 'scrollfind':
				self.text = 'You find an unidentified scroll!'
				self.text += '\nTake it to a town to be identified!'
				player.scrolls.append(args[0])
			elif action == 'scrollfindfail':
				self.text = 'You search the wilderness and find nothing!'
			elif action == 'scrolltrain':
				self.text = 'You identify a scroll of {0[0][0].name} +{0[0][1]}!'.format(args)
				args[0][0].level += args[0][1]
				args[0][0].training += args[0][1]
				player.studentloan += args[0][1]
			elif action == 'scroungeheal':
				self.text = 'You manage to scrounge up a point of health'
				self.text += '\n  using only the limited techniques known to science!'
				player.health += 1
			elif action == 'spelloffer':
				self.text = 'The magic shop is selling the {0[0][0].spell} spell for {0[0][1]} gold!'.format(args)
			elif action == 'stealmonster':
				self.text = "You steal the {0}'s {1} gold!".format(monster.name,monster.gold)
				player.gold += monster.gold
			elif action == 'stealmonsterfail':
				self.text = 'The monster has no gold, only American dollars.  Worthless!'
			elif action == 'stealtown':
				self.text = 'You steal {0} gold from the town!'.format(town.gold)
				player.gold += town.gold
			elif action == 'stealtownfail':
				self.text = 'You are unable to steal from the town!'
			elif action == 'strike':
				self.text = 'You strike the {0} for {1[0]} damage!'.format(monster.name,args)
				monster.health -= args[0]
			elif action == 'swordoffer':
				self.text = 'Hiram the Blacksmith offers to put his {0[0][0].gem} gem on your sword for {0[0][1]} gold!'.format(args)
			elif action == 'trainfail':
				self.text = 'The townsfolk pay you a pittance to train them! (+1 gold)'
				player.gold += 1
			elif action == 'trainoffer':
				self.text = 'Local academics offer to train you as a {0[0][0].name} for {0[0][1]} gold!'.format(args)
			elif action == 'wiff':
				self.text = 'You aim, you shoot, you...totally miss!'
			elif action == 'finale-alltrades':
				reward = monster.gold + town.gold
				i = 0
				for art in player.art:
					i += 1
					reward += i
				for friend in player.pets:
					reward += friend.gold
				reward += player.sacrifice
				reward += player.health
				reward += player.studentloan
				self.text = '''You stand nervously in the {1}.

The {0} looks over your character sheet, nods and says,
"WE'VE BEEN LOOKING FOR A WELL-ROUNDED CANDIDATE LIKE YOU!
CONGRATULATIONS!  YOU'VE GOT THE JOB!"

The gods pay you {2} gold a year to start, plus full benefits!

You're happy, your mother is happy...
YOU WIN!!!!!
'''.format(monster.name,day.element.map,reward)
				player.gold += reward
			elif action == 'finale-artist':
				reward = monster.gold + town.gold
				i = 0
				for art in player.art:
					i += 1
					reward += i
				self.text = '''The {1} looks over your art.
"AIN'T TOO SHABBY," it booms.  "HOW MUCH DO YOU WANT FOR IT?"
Eager for the exposure, you ask for {0} gold, which it readily pays.

Later, you learn your artwork was resold for 100,000 gold.

Your mother is not pleased.
'''.format(reward,monster.name)
				player.gold += reward
			elif action == 'finale-bounty':
				self.text = 'They shower you with {0} gold!'.format(town.gold)
				player.gold += town.gold
			elif action == 'finale-druid':
				reward = town.gold
				for friend in player.pets:
					reward += friend.gold
				self.text = 'You set up a zoo and make {0} gold selling tickets!'.format(reward)
				player.gold += reward
			elif action == 'finale-hadoken':
				self.text = 'You cast HADOKEN!!!!!'
				monster.health = 0
			elif action == 'finale-healer-fail':
				self.text = """
You cower in fear, having known all along
you were doomed!  Then you hear laughing!

A great voice from the heavens proclaims...
GOTCHA!  WOW, BOB'S REALLY SCRAPING THE 
BOTTOM OF THE BARREL FOR FOLLOWERS THESE
DAYS, AIN'T HE?

The figure walks away into infinity, leaving
you small and alone!
"""
			elif action == 'finale-healer-reward':
				self.text = """
Just as suddenly, the figure does a double take!

A great voice from the heavens proclaims...
WAIT A SECOND, AREN'T YOU ONE OF BOB'S GUYS?
YEAH, I HANG OUT WITH YOUR GOD ALL THE TIME.
WHY DON'T YOU COME ON OVER TO MY PLACE AND
WE'LL HAVE A FEW DRINKS AND CHAT.

AND HERE, YOU CAN HAVE YOUR SACRIFICES BACK!
"""
				reward = player.sacrifice + monster.gold;
				self.text += '(+' + str(reward) + ' gold)'
				player.gold += reward
			elif action == 'finale-hunt':
				self.text = """
Throwing your crossbow aside, you leap on the {0}
and devour it whole!  Though it is the best thing you've
ever tasted, the next day you are sick to your stomach!""".format(monster.name)
				monster.health = 0
			elif action == 'finale-ranger-reward':
				self.text = 'Luckily, you vomit up {0[0]} gold!'.format(args)
				player.gold += args[0]
			elif action == 'finale-ranger-fail':
				self.text = 'You get the dry heaves!'
			elif action == 'finale-intro':
				self.text = """On the final day of your journey,
you are suddenly overcome by dizziness!

There is a great flash as all light and 
color in the world flows together to
form a single brilliant figure!

A great voice from the heavens proclaims...
DARE YOU CHALLENGE ME, {0}?

LET'S SEE WHAT YOU'RE MADE OF!!!!!
""".format(player.name)
			elif action == 'finale-petcapture':
				self.text = "You've made a new BEST friend!"
				self.text += "\n{0.name}({0.health}/{0.level})".format(monster)
				player.addpet(monster)
			elif action == 'finale-praise':
				self.text = """
You are a great hero!
People far and wide sing your praises!"""
			elif action == 'finale-scholar-intro':
				self.text = """You say, "I've dodged everything else in this
world.  Now it's time to dodge you!"
"""
			elif action == 'finale-scholar-dodge':
				self.text = """You slip past him. You didn't get this far by 
engaging incalculably powerful astral figures 
in hand-to-hand combat!"
"""
			elif action == 'finale-scholar-reward':
				reward = player.studentloan + monster.gold
				self.text = """A great voice from the heavens proclaims...
WHOA, YOU'RE A SLY ONE!  IF I PAY YOU
{0} GOLD, WOULD YOU BE MY TEACHER?

You accept, of course!  That should just about pay off your student loans!
""".format(reward)
				player.gold += reward
			elif action == 'finale-stealmonsterfail':
				self.text = "You steal the {0}'s heart.  You would have preferred gold!".format(monster.name)
			elif action == 'finale-stealtown':
				self.text = 'You steal {0} gold from them!'.format(town.gold)
				player.gold += town.gold
			elif action == 'finale-stealtownfail':
				self.text = 'You are unable to steal from them!'
			elif action == 'finale-warrior-monsterdies':
				self.text = 'The {0} explodes impressively!'.format(monster.name)
#			elif action == 'finale-warrior-reward':
#				self.text = """
#After you retire, you become a model,
#showing off your healthy body for {0} gold!
#""".format(player.health)
#				player.gold += player.health
			else:
				raise JackHack.Fatal(1)
	class Job(Character):
		def __init__(self,game):
			JackHack.Character.__init__(self,game)
			self.level = 1
			self.experience = 0
			self.training = 0
			self.name = self.__class__.__name__
			self.offer = None
		def __str__(self,game):
			return self.name + '(' + str(self.level) + '/' + str(self.experience) + ')'
		def play(self,game):
			self.offer = None
			if not game.day.lastday:
				self.__play(game)
				self.level += 1
				self.experience += 1
				if not game.day.results:
					game.act(0)
			else:
				game.act('finale-intro')
				if game.player.title() == 'of All Trades':
					game.act('finale-alltrades')
				else:
					self.__finish(game)
	class Warrior(Job):
		def _Job__play(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			self.offer = None
			if monster:
				glowgem = None
				for weakness in monster.weak:
					if weakness in self.attack:
						glowgem = weakness.gem
				if glowgem:
					game.act('glowgem',glowgem)
				pet = game.player.getpowerpet(monster)
				if pet:
					if game.attackroll(pet,monster):
						game.act('petattack',pet)
				mydamage = 0
				monsterdamage = 0				
				while monster.health > mydamage and player.health > monsterdamage:
					mydamage += 1
					if monster.health > 0:
						if game.attackroll(monster,self):
							monsterdamage += 1
				if monsterdamage:
					game.act('monsterstrike',monsterdamage)
				if player.health > 0:
					if mydamage:
						game.act('strike',mydamage)
					game.act('monsterdies')
					game.act('plunder')
					if town:
						game.act('bounty')
				else:
					game.act('escape')
			if town:
				game.act('rest')
				if not monster:
					if len(self.attack) < player.gold:
						if not (day.element in self.attack):
							self.offer = (day.element,len(self.attack)+1)
							self.offertext = 'Add a gem to your sword?'
							game.act('swordoffer',self.offer)
		def _Job__finish(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			self.offer = None
			glowgem = None
			for weakness in monster.weak:
				if weakness in self.attack:
					glowgem = weakness.gem
			if glowgem:
				game.act('glowgem',glowgem)
			mydamage = 0
			monsterdamage = 0				
			while monster.health > mydamage and player.health > monsterdamage:
				mydamage += 1
				if monster.health > 0:
					if game.attackroll(monster,self):
						monsterdamage += 1
			if monsterdamage:
				game.act('monsterstrike',monsterdamage)
			if player.health > 0:
				if mydamage:
					game.act('strike',mydamage)
				game.act('finale-warrior-monsterdies')
				game.act('plunder')
				monsterdies = True
			else:
				game.act('escape')
				monsterdies = False
			game.act('finale-praise')
			if monsterdies:
				game.act('finale-bounty')
#			game.act('finale-warrior-reward')
		def accept(self,game):
			if not self.offer:
				raise JackHack.Fatal(2)
			game.addattack(self.offer[0],self)
			game.player.gold -= self.offer[1]
	class Healer(Job):
		def _Job__play(self,game):
			player = game.player
			day = game.day
			game.act('pray')
			sacrifice = 0
			if player.gold < self.level:
				sacrifice = player.gold
			else:
				sacrifice = self.level
			if game.skillroll(self):
				if sacrifice:
					game.addstrength(day.element,self)
					game.act('heal',sacrifice)
				elif player.pets:
					game.addstrength(day.element,self)
					game.act('petsacrifice')
				else:
					game.act('freeheal')
			else:
				game.act('noheal')
				if sacrifice and day.town:
					game.act('healtemple',sacrifice)
				else:
					game.act('scroungeheal')
		def _Job__finish(self,game):
			player = game.player
			day = game.day
			monstersuccess = False
			if game.skillroll(self):
				game.act('finale-healer-reward')
				monstersuccess = True
			else:
				game.act('finale-healer-fail')
			game.act('finale-praise')
			if monstersuccess:
				game.act('finale-bounty')
	class Thief(Job):
		def _Job__play(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			outcold = 0
			if monster:
				pet = player.getpowerpet(monster)
				if pet:
					game.act('petdefend',pet)
					if game.attackroll(monster,pet):
						game.act('petstrike',pet,monster.level)
						if pet.health < 1:
							game.act('petdeath',pet)
				elif game.attackroll(monster,self):
					game.act('monsterstrike',monster.level)
				else:
					game.act('dodge')
				if player.health > 0:
					if game.attackroll(self,monster):
						game.act('stealmonster')
					else:
						game.act('stealmonsterfail')
				else:
					game.act('loseallgold')
					outcold = 1
			if town and not outcold:
				if (day.element in self.weak) and (player.gold >= day.level):
					self.offer = day.level
					self.offertext = "Pay to clear your name?"
					game.act('clearname')
				elif game.skillroll(self):
					game.act('stealtown')
					if (day.element not in self.strong) and (player.gold >= 2 * day.level):
						self.offer = 2 * day.level
						self.offertext = "Pay guild dues?"
						game.act('joinguild')
				else:
					game.act('stealtownfail')
					if day.element not in self.weak:
						game.addweakness(day.element,self)
						game.act('caught')
		def _Job__finish(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			if game.attackroll(monster,self):
				game.act('monsterstrike',monster.level)
			else:
				game.act('dodge')
			if player.health > 0:
				if game.attackroll(self,monster):
					game.act('stealmonster')
				else:
					game.act('finale-stealmonsterfail')
			else:
				game.act('die')
			if not player.dead:
				game.act('finale-praise')
				if game.skillroll(self):
					game.act('finale-stealtown')
				else:
					game.act('finale-stealtownfail')
		def accept(self,game):
			if not self.offer:
				raise JackHack.Fatal(2)
			game.addstrength(game.day.element,self)
			game.player.gold -= self.offer
	class Wizard(Job):
		def _Job__play(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			if monster:
				pet = game.player.getpowerpet(monster)
				firstattempt = 1
				while monster.health > 0 and player.health > 1:
					if firstattempt and pet and game.attackroll(pet,monster):
						game.act('petdistract')
					elif game.attackroll(monster,self):
						game.act('monsterstrike',monster.level)
					else:
						game.act('dodge')
					firstattempt = 0
					if player.health > 1:
						game.act('manatap')
						if game.attackroll(self,monster):
							castspell = 'magic missile'
							for weakness in monster.weak:
								if weakness in self.attack:
									castspell = weakness.spell
							game.act('hadoken',castspell)
						else:
							game.act('fizzle')
				if monster.health < 1:
					game.act('monsterdies')
					game.act('plunder')
					if town:
						game.act('bounty')
				elif player.health < 1:
					game.act('escape-magic')
				elif player.health == 1:
					game.act('flee')
			if town:
				game.act('rest')
				if not monster:
					if len(self.attack) < player.gold:
						if not (day.element in self.attack):
							self.offer = (day.element,len(self.attack)+1)
							self.offertext = 'Learn a spell?'
							game.act('spelloffer',self.offer)
		def _Job__finish(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			while monster.health > 0 and player.health > 1:
				if game.attackroll(monster,self):
					game.act('monsterstrike',monster.level)
				else:
					game.act('dodge')
				if player.health > 1:
					game.act('manatap')
					if game.attackroll(self,monster):
						game.act('finale-hadoken')
					else:
						game.act('fizzle')
			monsterdies = False
			if monster.health < 1:
				game.act('monsterdies')
				game.act('plunder')
				monsterdies = True
			elif player.health < 1:
				game.act('escape-magic')
			elif player.health == 1:
				game.act('flee')
			game.act('finale-praise')
			if monsterdies:
				game.act('finale-bounty')
		def accept(self,game):
			if not self.offer:
				raise JackHack.Fatal(2)
			game.addattack(self.offer[0],self)
			game.player.gold -= self.offer[1]
	class Ranger(Job):
		def _Job__play(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			if monster:
				pet = game.player.getpowerpet(monster)
				firstattempt = 1
				while monster.health > 0 and player.health > 0:
					if firstattempt and pet and game.attackroll(pet,monster):
						game.act('petdistract')
					elif game.attackroll(monster,self):
						game.act('monsterstrike',monster.level)
					else:
						game.act('dodge')
					firstattempt = 0
					if player.health > 0:
						if game.attackroll(self,monster):
							game.act('hunt')
						else:
							game.act('wiff')
				if monster.health < 1:
					game.act('eat')
					if town:
						game.act('bounty')
				else:
					game.act('escape')
			if town:
				game.act('rest')
				if player.gold >= day.level * 2:
					self.offer = True
					self.offertext = 'Stay at the inn?'
					game.act('inn')
			if not (town or monster):
				game.act('hunt-nature')
				if day.element not in self.strong:
					game.addstrength(day.element,self)
					game.act('map')
				else:
					for pet in player.pets:
						if not pet.isknown():
							game.act('petlearn',pet)
							break
		def _Job__finish(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			while monster.health > 0 and player.health > 0:
				if game.attackroll(monster,self):
					game.act('monsterstrike',monster.level)
				else:
					game.act('dodge')
				if player.health > 0:
					if game.attackroll(self,monster):
						game.act('finale-hunt')
					else:
						game.act('wiff')
			monsterdies = False
			if monster.health < 1:
				reward = monster.gold + player.health - player.gold
				if reward > 0:
					game.act('finale-ranger-reward',reward)
				else:
					game.act('finale-ranger-fail')
				monsterdies = True
			else:
				game.act('escape')
			game.act('finale-praise')
			if monsterdies:
				game.act('finale-bounty')
		def accept(self,game):
			self.offer = None
			game.player.gold -= game.day.level * 2
			game.player.health += game.day.level
	class Druid(Job):
		def _Job__play(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			if monster:
				petcaptured = False
				while (not petcaptured) and (player.health > monster.level):
					if game.attackroll(self,monster):
						game.act('petcapture')
						petcaptured = True
					else:
						game.act('petcapturefail')
						if player.pets:
							pet = player.getpowerpet(monster)
							game.act('petdefend',pet)
							if game.attackroll(monster,pet):
								game.act('petstrike',pet,monster.level)
								if pet.health < 1:
									game.act('petdeath',pet)
						else:
							if game.attackroll(monster,self):
								game.act('monsterstrike',monster.level)
							else:
								game.act('dodge')
				if not petcaptured:
					game.act('petnotpresent')
			if town:
				if player.pets:
					bestpet = player.getrichpet()
					self.offer = ('sell',bestpet,bestpet.gold + town.gold)
					self.offertext = 'Sell your pet?'
					game.act('petoffer',self.offer)
				elif player.gold >= game.day.level:
						newpet = JackHack.Monster(game)
						self.offer = ('buy',newpet,game.day.level)
						self.offertext = 'Buy a pet?'
						game.act('petbuyoffer',self.offer)
		def _Job__finish(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			petcaptured = False
			while (not petcaptured) and (player.health > monster.level):
				if game.attackroll(self,monster):
					game.act('finale-petcapture')
					petcaptured = True
				else:
					game.act('petcapturefail')
					if player.pets:
						pet = player.getpowerpet(monster)
						game.act('petdefend',pet)
						if game.attackroll(monster,pet):
							game.act('petstrike',pet,monster.level)
							if pet.health < 1:
								game.act('petdeath',pet)
					else:
						if game.attackroll(monster,self):
							game.act('monsterstrike',monster.level)
						else:
							game.act('dodge')
			if not petcaptured:
				game.act('petnotpresent')
			game.act('finale-praise')
			if player.pets:
				game.act('finale-druid')
		def accept(self,game):
			if not self.offer:
				raise JackHack.Fatal(2)
			if self.offer[0] == 'sell':
				game.player.killpet(self.offer[1])
				game.player.gold += self.offer[2]
			elif self.offer[0] == 'buy':
				game.player.addpet(self.offer[1])
				game.player.gold -= self.offer[2]
	class Scholar(Job):
		def _Job__play(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			distant = False
			if monster:
				pet = player.getpowerpet(monster)
				if pet:
					game.act('petdefend',pet)
					if game.attackroll(monster,pet):
						game.act('petstrike',pet,monster.level)
						if pet.health < 1:
							game.act('petdeath',pet)
				elif game.attackroll(monster,self):
					damage = monster.level
					if damage >= player.health:
						damage = player.health - 1
					if damage:
						game.act('monsterstrike',damage)
					else:
						distant = True
						game.act('dodgedistant')
				else:
					game.act('dodge')
				if not distant:
					if not monster.name in game.player.monsterknowledge:
						game.act('learn',monster.name)
			if not distant:
				if town:
					while player.scrolls:
						scroll = player.scrolls.pop(0)
						game.act('scrolltrain',scroll)
					someoffer = self.newtrain(game)
					if player.gold >= someoffer[1]:
						self.offer = someoffer
						self.offertext = 'Accept offer to train?'
						game.act('trainoffer',self.offer)
					else:
						game.act('trainfail')
				else:
					if game.skillroll(self):
						game.act('scrollfind',self.newtrain(game))
					else:
						game.act('scrollfindfail')
		def _Job__finish(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			game.act('finale-scholar-intro')
			if game.attackroll(monster,self):
				game.act('monsterstrike',monster.level)
			else:
				game.act('finale-scholar-dodge')
			if player.health < 0:
				game.act('die')
			if not player.dead:
				while player.scrolls:
					scroll = player.scrolls.pop(0)
					game.act('scrolltrain',scroll)
				game.act('finale-scholar-reward')
				game.act('finale-praise')
				game.act('finale-bounty')
		def newtrain(self,game):
			totrain = self
			while totrain == self:
				totrain = random.choice(game.player.jobs)
			return (totrain,self.level*2)
		def accept(self,game):
			if not self.offer:
				raise JackHack.Fatal(2)
			self.offer[0].level += self.offer[1]
			self.offer[0].training += self.offer[1]
			game.player.gold -= self.offer[1]
			game.player.studentloan += self.offer[1]
	class Artist(Job):
		def _Job__play(self,game):
			player = game.player
			day = game.day
			monster = day.monster
			town = day.town
			if day.element.map not in player.art:
				game.act('artist-element')
			if monster and monster.name not in player.art:
				game.act('artist-monster')
			if town:
				game.act('artist-town')
		def _Job__finish(self,game):
			game.act('finale-artist')


def JackHackCLI():
	def rename(game):
		while True:
			try:
				game.player.rename(raw_input("What is your name? "))
				break
			except JackHack.Error as error:
				print error
	def intro(game):
		print """
Once upon a time, there lived a player character named {0}!

Though {0} was of an age when responsible people no longer 
live with their mother, that's exactly where {0} lived!

One day she said, "{0}, you're restless!  And we're poor!
Why don't you go out into the world, figure out what you're 
meant to do with your life, and see how much gold you can 
make doing it!  I don't want to see you back here for at 
least {1} days!"

And so, {0} set out on a {1} day journey
to find his true purpose...and GOLD!

Welcome to the {1} day journey, {0}!
""".format(game.player.name,game.totalsteps)
	def daybanner(game):
		print '===== DAY',game.day.level,'====='
	def charsheet(game):
		print """{0}
Health: {0.health}
Gold: {0.gold}
""".format(game.player)
		needbreak = False
		if game.player.scrolls:
			print "You have {0} unidentified scrolls!".format(len(game.player.scrolls))
		if game.player.gems:
			gemtext = ''
			for element in game.player.gems:
				if not gemtext:
					gemtext += "Gems: {0}".format(element.gem)
				else:
					gemtext += ', {0}'.format(element.gem)
			print gemtext
		if game.player.gods:
			godtext = ''
			for element in game.player.gods:
				if not godtext:
					godtext += "Gods: {0}".format(element.god)
				else:
					godtext += ', {0}'.format(element.god)
			print godtext
		if game.player.wanted:
			wantedtext = ''
			for element in game.player.wanted:
				if not wantedtext:
					wantedtext += "Wanted: {0}".format(element.guild)
				else:
					wantedtext += ', {0}'.format(element.guild)
			print wantedtext
		if game.player.guilds:
			guildtext = ''
			for element in game.player.guilds:
				if not guildtext:
					guildtext += "Guilds: {0}".format(element.guild)
				else:
					guildtext += ', {0}'.format(element.guild)
			print guildtext
		if game.player.spells:
			spelltext = ''
			for element in game.player.spells:
				if not spelltext:
					spelltext += "Spells: {0}".format(element.spell)
				else:
					spelltext += ', {0}'.format(element.spell)
			print spelltext
		if game.player.maps:
			maptext = ''
			for element in game.player.maps:
				if not maptext:
					maptext += "Maps: {0}".format(element.map)
				else:
					maptext += ', {0}'.format(element.map)
			print maptext
		if game.player.monsterknowledge:
			knowtext = ''
			for name in game.player.monsterknowledge:
				if not knowtext:
					knowtext = 'Known: {0}'.format(name)
				else:
					knowtext += ', {0}'.format(name)
			print knowtext
		if game.player.pets:
			pettext = ''
			for friend in game.player.pets:
				if not pettext:
					pettext += "Pets: {0}".format(friend.name)
				else:
					pettext += ", {0}".format(friend.name)
				if friend.isknown():
					pettext += "({0})".format(friend.whatknown())
			print pettext
		if game.player.art:
			arttext = ''
			totalart = len(game.elements) + len(game.monstertypes)
			artcount = len(game.player.art)
			for work in game.player.art:
				if not arttext:
					arttext += "Art({1}/{2}): {0}".format(work,artcount,totalart)
				else:
					arttext += ", {0}".format(work)
			print arttext
		print "Mom: {0}%\n".format(game.mom())
		i = 0
		for job in game.player.jobs:
			i += 1
			print '{0})'.format(i),(job.name + ':').ljust(8),job.level,'({0})'.format(job.experience)
		print
	def place(game):
		towntext = ''
		if game.day.town:
			towntext = "in a town"
			if game.day.element in game.player.guilds:
				towntext += '(' + str(game.day.town.gold) + ')'
			towntext += ' '
		print "You are " + towntext + game.day.element.terrain + "!"
		if game.day.monster:
			if game.day.monster.isknown():
				leveltext = '(' + game.day.monster.whatknown() + ')'
			else:
				leveltext = ''
			print "There is a {0}{1} here!".format(game.day.monster.name,leveltext)
		print
	def pickjob(game):
		while True:
			try:
				line = raw_input("How will you approach this? (1-{0}) ".format(len(game.player.jobs)))
				while line in ['h','?']:
					print game.day.possible()
					line = raw_input("How will you approach this? (1-{0}) ".format(len(game.player.jobs)))
				return game.player.jobs[int(line) - 1]
			except JackHack.Error as error:
				print error
			except (ValueError,IndexError):
				pass
	def results(game):
		for result in game.day.results:
			print result.text
		print
	def makeoffer(job):
		while True:
			choice = raw_input(job.offertext + " (y/n) ")
			if choice.lower() == 'y':
				print
				return True
			elif choice.lower() == 'n':
				print
				return False
	def playagain():
		while True:
			choice = raw_input("Play again? (y/n) ")
			if choice.lower() == 'y':
				print
				return True
			elif choice.lower() == 'n':
				print
				return False
	def showgames(allgames,savegame = None):
		print 'Best games played:'
		bygold = {}
		bymom = {}
		for gameresult in allgames:
			if gameresult[2]:
				if gameresult[1] not in bygold:
					bygold[gameresult[1]] = gameresult
				elif bygold[gameresult[1]][2] < gameresult[2]:
					bygold[gameresult[1]] = gameresult
				elif bygold[gameresult[1]][3] < gameresult[3]:
					if gameresult[1] not in bymom:
						bymom[gameresult[1]] = gameresult
					elif bymom[gameresult[1]][3] < gameresult[3]:
						bymom[gameresult[1]] = gameresult
		alltitles = list(bygold.items() + bymom.items())
		alltitles.sort(lambda x,y: y[1][2] - x[1][2])
		for title in alltitles:
			gameresult = title[1]
			congratulations = ''
			if gameresult == savegame:
				congratulations = '\tCONGRATULATIONS!!!'
			print gameresult[2],'\t',gameresult[3],'\t',gameresult[0],gameresult[1],congratulations
		print
#		print 'All games played:'
#		for gameresult in allgames:
#			print gameresult[2],'\t',gameresult[0],gameresult[1]
#		print
	playme = True
	allgames = []
	try:
		savefile = open(os.path.expanduser('~/.jackhackpy'),'r')
		for line in savefile:
			line = line.strip()
			fields = line.split('\t')
			fields[2] = int(fields[2])
			fields[3] = int(fields[3])
			allgames.append(fields)
		savefile.close()
	except:
		allgames = []
	print "\nWelcome to JackHack!\n"
	if allgames:
		showgames(allgames)
	while playme:
		game = JackHack()
		rename(game)
		intro(game)
		for day in game.day:
			daybanner(game)
			charsheet(game)
			if not day.lastday:
				place(game)
				job = pickjob(game)
				print
			else:
				job = game.player.topjobs()[0]
			job.play(game)
			results(game)
			if not day.lastday:
				if job.offer and makeoffer(job):
					job.accept(game)
		print '===== FINAL STATS ====='
		charsheet(game)
		print
		thisgame = game.savegame()
		allgames.append(thisgame)
		allgames.sort(lambda x, y: y[2] - x[2])
		savefile = open(os.path.expanduser('~/.jackhackpy'),'w')
		for savegame in allgames:
			savefile.write(savegame[0]+'\t'+savegame[1]+'\t'+str(savegame[2])+'\t'+str(savegame[3])+'\n')
		savefile.close()
		showgames(allgames,thisgame)
		playme = playagain()

if __name__ == "__main__":
#try:
	JackHackCLI()
#except KeyboardInterrupt:
#	print
