import random
import DnDFileManager as manager

attackDatabase = 'attackDatabase'


class Combat:


    def reqAttackType(attack, attackType):

        if attackType == 'Weapon':
            val = manager.fromWepTable(attack)
            value = val['Range']
        elif attackType == 'Spell':
            value = manager.fromSpellTable(attack)

        return value

    def makeWeaponAttack(weaponkey, attacker, target):
        
        weapon = manager.fromWepTable(weaponkey)
        
        

    def castSpell(spell, target='Self'):

        spell = manager.fromSpellTable(spell)

    def attackRoll(attacker, weapon, targetAC):

        attackClass = attacker['Class']
        attackLevel = attacker['Level']
        attackBonus = manager.CharacterClass.classLookup(attackClass,
                                             attackLevel,'Base Attack Bonus')
        newWep = manager.fromWepTable(weapon)
        critMin, critMax = newWep['CritMin'], newWep['CritMax']
        critMul = newWep['CritMult']
        wepDamage = newWep['Damage']
        damage = diceRoll(wepDamage)
        
        if critMin == critMax:
            attack = diceRoll.attackRoll([20],targetAC,attackBonus)
        else:
            critRange = range(critMin,critMax)
            attack = diceRoll.attackRoll(critRange,targetAC,attackBonus)

        if attack == 'Critical':
            return damage.standardRoll()*critMul
            
        elif attack == 'Hit':
            return damage.standardRoll()

        else:
            return 0

        

class diceRoll:

    def __init__(self, roll):
        roll = roll.strip('+')
        roll = roll.split('d')
        self.numDie = int(roll[0])
        self.die = int(roll[1])

    def standardRoll(self):
        sumRoll = 0
        for i in range(self.numDie):
            roll = random.randint(1,self.die)
            sumRoll+=roll
        return sumRoll

    def attackRoll(critrange,targetAC,bonus):
        roll = random.randint(1,20)
        if roll in critrange:
            roll = random.randint(1,20)
            if roll >= targetAC:
                return 'Critical'
            else:
                return 'Hit'
        elif roll == 1:
            return 'Miss'
        
        if roll+bonus >= targetAC:
            return 'Hit'    

        else:
            return 'Miss'
                
        
class Spell:
    
    def __init__(self, name, school, descriptor, level, components, castingtime,
                 spellrange, target, duration, saving_throw='None',
                 resistance='None', text=''):
        self.name = name
        self.school = school
        self.descriptor = descriptor
        self.level = level
        self.components = components
        self.castingtime = castingtime
        self.spellrange = spellrange
        self.target = target
        self.duration = duration
        self.saving_throw = saving_throw
        self.resistance = rsistance
        self.text = text

    def returnName(self):
        return self.name

    def returnSchool(self):
        return self.school

    def returnDescriptor(self):
        return self.descriptor

    def returnLevel(self):
        return self.level

    def returnComponents(self):
        return self.components

    def returnCastingTime(self):
        return self.castingtime

    def returnSpellRange(self):
        return self.spellrange

    def returnTarget(self):
        return self.target

    def returnDuration(self):
        return self.duration

    def returnSavingThrow(self):
        return self.saving_throw

    def returnResistance(self):
        return self.resistance

    def returnText(self):
        return self.text


class Feat:

    def __init__(self, name, prereq={}, benefit={}, normal={}, special={}):
        self.name = name
        self.prereq = prereq
        self.benefit = benefit
        self.normal = normal
        self.special = special

    def returnName(self):
        return self.name

    def returnPrereq(self):
        return self.prereq

    def returnBenefit(self):
        return self.benefit

    def returnNormal(self):
        return self.normal

    def returnSpecial(self):
        return self.special

