import sqlite3

attackDatabase = 'attackDatabase'

class CharacterSheet:

    def __init__(self, character = {}, attributes={}, modifiers={},
                 skills = {}, feats = {}, spells = {}):
        self.char = character
        self.attr = attributes
        self.skil = skills
        self.feat = feats
        self.spel = spells
        self.mods = modifiers

    def __str__(self):
        string = self.char['Player Name']+'\n'+self.char['Class']+' Level '+\
            self.char['Level']
        return(string)

    def returnChar(self, request):
        return self.char[request]

    def returnAtt(self, request):
        return self.attr[request]

    def returnSkill(self, request):
        return self.skil[request]

    def returnFeat(self, request):
        return self.feat[request]

    def returnSpell(self, request):
        return self.spel[request]

    def returnModifier(self, request):
        return self.mods[request]

    def updateChar(self, key, update):
        self.char[key] = update

    def updateAtt(self, key, update):
        self.attr[key] = update

    def updateSkill(self, key, update):
        self.skil[key] = update

    def updateFeat(self, key, update):
        self.feat[key] = update

    def updateSpell(self, key, update):
        self.spel[key] = update

    def attackBonus():
        charClass = self.char['Class']
        charLevel = self.char['Level']
        if len(charClass) == 1:
            pass
        else:
            for i in range(len(charClass)):
                pass

            
class CharacterClass():


    def __init__(self, name, database):
        self.name = name
        self.database = database

    def classLookup(self, name, level, lookup):

        conn = sqlite3.connect('classdatabase')
        c = conn.cursor()
        conn.row_factory = sqlite3.Row
        c.execute('select * from (?) where level (?)', (name,level))
        request = c.fetchone()[lookup]

        return request
        

#File manipulation functions

def charFromFile(file):
    f = open(file, "r")
    character = {}
    attributes = {}
    skills = {}
    feats = ()
    abilities = ()
    spells = ()
    modifiers = {}
    for line in f:
        line = line.strip("\n")
        if line.startswith('Attribute-'):
            line = line.strip('Attribute-')
            match = line.split(':')
            attributes[match[0]]=match[1]
            mod = attModifier(int(match[1]))
            modifiers[match[0]]=mod
        elif line.startswith('Skill-'):
            line = line.strip('Skill-')
            match = line.split(':')
            skills[match[0]]=match[1]
        elif line.startswith('Feat-'):
            line = line.strip('Feat-')
            feats.append(line)
        elif line.startswith('Spell-'):
            line = line.strip('Spell-')
            spells.append(line)
        elif line.startswith('Ability'):
            line = line.strip('Ability-')
            abilities.append(line)
        else:
            match = line.split(':')
            character[match[0]]=match[1]
    f.close()
    char = CharacterSheet(character, attributes, skills, feats, spells)
    return char

def attModifier(attribute):

    if attribute >= 10:
        modifier = int((attribute-10)/2)
    else:
        modifier = int((attribute-1)/2)

    return modifier


def wepFromFile(file):
    
    file = open(file, 'r')
    weapon = {}
    for line in file:
        line = line.strip('\n')
        match = line.split(':')
        key = match[0]
        value = match[1]
        if key == 'Critical':
            match = match[1].split('x')
            weapon['CritMult']=match[1]
            if match[0].find('-'):
                match = match[0].split('-')
                weapon['CritMin'] = match[0]
                weapon['CritMax'] = match[1]
            else:
                weapon['CritMin'] = 20
                weapon['CritMax'] = 20
        else:
            weapon[key]=value
    return weapon

def createWepTable():

    conn = sqlite3.connect(attackDatabase)
    c = conn.cursor()
    c.execute('''create table weapons
            (name text, range integer, damage integer, critmin integer,
            critmax integer, critmult integer, type text, ammo text)''')

def addToWepTable(file):

    conn = sqlite3.connect(attackDatabase)
    c = conn.cursor()
    w = wepFromFile(file)
    weapon = (w['Name'],w['Range'],w['Damage'],w['CritMin'],w['CritMax'],
              w['CritMult'],w['Type'],w['Ammo'])
    c.execute('insert into weapons values (?,?,?,?,?,?,?,?)',weapon)

def fromWepTable(weapon):
    
    if type(request) == str:
        request = [request]
        
    conn = sqlite3.connect(attackDatabase)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()    
    c.execute('select * from weapons where name (?)',weapon)
    wepStats = c.fetchone()
        
    return wepStats

def createSpellTable():

    conn = sqlite3.connect(spellDatabase)
    c = conn.cursor()
    c.execute('''create table spells (name text, castingtime integer,
            range integer, target string)''')

def addToSpellTable(file):

    conn = sqlite3.connect(attackDatabase)
    c = conn.cursor()
    s = spellFromDatabase(file)
    spell = (s['Name'],s['Casting Time'],s['Range'],s['Target'])
    spell = ('insert into spells values (?,?,?,?)', spell)

def fromSpellTable(spell):

    if type(request) == str:
        request = [request]
        
    conn = sqlite3.connect(attackDatabase)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()    
    c.execute('select * from spells where name (?)',spell)
    spellStats = c.fetchone()
        
    return spellStats

