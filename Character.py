import sqlite3

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

    
