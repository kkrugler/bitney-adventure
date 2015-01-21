#!/usr/bin/python
# -*- coding: utf-8 -*-
# adventureEngine.py
# Copyright 2005-2006, Paul McGuire
# 2009 Dusan Hokuv
# GPL
#


#TODO: zkracovani nazvu predmetu - napr. pro pap namisto pro papir
#TODO: moznost zadavat prikazy bez diakritiky - napr. pro kos
#TODO: dalsi prikazy
#TODO: v inventari muze byt jen sest predmetu, nebo dame treba osm, nektere predmety dokazou pocet zvysit(ruksak napr.)
#TODO: usnadnovaci funkce jako teleport a inventar co chce pro ladeni
#TODO: mereni herniho casu
#TODO: pygtk, pyqt front
#TODO: mereni casu - mas treba 15 sekund na prejiti do jine mistnosti
#TODO: predmet.inv - predmet obsahuje jine predmety, napr. uvnitr brasny vidis to to a to.
#TODO


# importy potrebnych modulu
from pyparsing import *
import sys
import os
import codecs
import cPickle
import random
from collections import deque #kvuli rotaci
import textwrap
import readline #doplnovani
import rlcompleter #historie - sipky, doplnovani
#import locale

alphas = u'aábcčdďeéěfghiíjklmnňoópqrřsštťuůúvwxyýzž'
alphas += alphas.upper()




def aOrAn( item ):
    if item.desc[0] in "aeiou":
        return "an"
    else:
        return "a"
    
# pocitani predmetu a vkladani carek mezi ne v seznamu a pred poslednim vlozeni a
def enumerateItems(l):
    if len(l) == 0: return u"nic"
    out = []
    for item in l:
        if len(l)>1 and item == l[-1]:
            out.append(u"a")
#        out.append( aOrAn( item ) )
        if item == l[-1]:
            out.append(item.desc)
        else:
            if len(l)>2 and item != l[-2]:
                out.append(item.desc+u",")
            else:
                out.append(item.desc)
    return u" ".join(out)

# pocitani smeru, oddeleni carkou a na pred poslednim a
def enumerateDoors(l):
    if len(l) == 0: return ""
    out = []
    for item in l:
        if len(l)>1 and item == l[-1]:
            out.append(u"a")
        if item == l[-1]:
            out.append(item)
        else:
            if len(l)>2 and item !=l[-2]:
                out.append(item+u",")
            else:
                out.append(item)
    return u" ".join(out)

# trida starajici se o doplnovani tabulatorem
class Completer:
    def __init__(self, words):
        self.words = words
        self.prefix = None
    def complete(self, prefix, index):
        if prefix != self.prefix:
            self.matching_words = [w for w in self.words if w.startswith(prefix)]
            self.prefix = prefix
        try:
            return self.matching_words[index]
        except IndexError:
            return None

# trida Svet
class World(object):
    def __init__(self, desc):
        self.desc = desc
        self.rooms = []
        self.room.inv
        self.room.doors
        self.room.desc


# trida mistnost
class Room(object):
    def __init__(self, desc):
        self.desc = desc
        self.inv = []
        self.gameOver = False
        self.doors = [None,None,None,None,None,None]
        self.compass = True
        self.canMove = True
        self.moveAction = None
        self.roomAction = None
    
    def __getattr__(self,attr):
        return \
            { 
            "s":self.doors[0],
            "j":self.doors[1],
            "v":self.doors[2],
            "z":self.doors[3],
            "n":self.doors[4],
            "d":self.doors[5],
            }[attr]
                
    def enter(self,player):
        if self.gameOver:
            player.gameOver = True
        
    def addItem(self, it):
        self.inv.append(it)
    
    def removeItem(self,it):
        self.inv.remove(it)
        
    def describe(self,player):
    # word wrap na sirku 80 znaku
        print (textwrap.fill(self.desc,80))
        # pokud je s mistnosti spojena nejaka akce
        if self.roomAction:
            self.roomAction(self,player)
        visibleItems = [ it for it in self.inv if it.isVisible ]
        if len(visibleItems) > 1:
            print u"Vidíš tu %s." % enumerateItems( visibleItems )
        elif len(visibleItems) == 1:
            print u"Vidíš tu %s." % enumerateItems( visibleItems )
        numDoors = sum([1 for r in self.doors if r is not None])
        if numDoors == 0:
            print u"Nemůžeš jít žádným směrem."
        else:         
            if numDoors == 1:
                reply = u"Můžeš jít jen "
            else:
                reply = u"Můžeš jít "
            doorNames = [ {0:u"na sever", 1:u"na jih", 2:u"na východ", 3:u"na západ", 4:u"nahoru", 5:u"dolů"}[i] 
                          for i,d in enumerate(self.doors) if d is not None ]
            #~ print doorNames
            reply += enumerateDoors( doorNames )
            reply += "."
            if self.compass:
                print reply
            else:
                print player.dirDescr(self)

class Exit(Room):
    def __init__(self):
        super(Exit,self).__init__("")
    
    def enter(self,player):
        player.gameOver = True


    
# trida predmet
class Item(object):
    items = {}
    def __init__(self, desc):
        # seznam atributu predmetu
        self.desc = desc
        self.isDeadly = False
        self.isFragile = False
        self.isBroken = False
        self.isTakeable = True
        self.isVisible = True
        self.isOpenable = False
        self.isCloseable = False
        self.useAction = None
        self.takeAction = None
        self.dropAction = None
        self.examineAction = None
        self.insertAction = None
        self.openAction = None
        self.closeAction = None
        self.usableConditionTest = None
        self.contents = None
        self.isOpened = False
        self.isClosed = False
        self.canInventory = False
        self.inv = []
        Item.items[desc] = self
        
    def __unicode__(self):
        return self.desc
        
    def breakItem(self):
        if not self.isBroken:
            print u"<Prásk!>"
            self.desc = u"rozbité " + self.desc
            self.isBroken = True

    def isUsable(self, player, target):
        if self.usableConditionTest:
            return True
        else:
            return False
        
    def useItem(self, player, target):
        if self.useAction:
            self.useAction(player, self, target)
            
    def takeItem(self, player, target):
        if self.takeAction:
            return self.takeAction(player, self, target)

    def dropItem(self, player, target):
        if self.dropAction:
            self.dropAction(player, self, target)

    def examineItem(self, player, target):
        if self.examineAction:
            self.examineAction(player, self, target)

    def insertItem(self, player, target):
        if self.insertAction:
            self.insertAction(player, self, target)

    def openItem(self, player, target):
        if not self.isOpened and self.isOpenable:
            self.isOpened = True
            self.isCloseable = True
            if self.openAction:
                self.openAction(player, self, target)
            if self.contents is not None:
                player.room.addItem( self.contents )
                self.contents = None
            self.desc = u"otevřený " + self.desc.lstrip(u"zavřený ")
            self.isOpenable = False
        elif self.openAction:
            self.openAction(player, self, target)

    def closeItem(self, player, target):
        if self.isOpened:
            self.isOpened = False
            self.isCloseable = False
            self.isOpenable = True
            if self.closeAction:
                self.closeAction(player, self, target)
            # je treba doresit to pridavani popisu zavreny otevreny - to resi ten lstrip
            self.desc = u"zavřený " + self.desc.lstrip(u"otevřený ")


# zakladni trida pro prikazy
class Command(object):
    "Base class for commands"
    def __init__(self, verb, verbProg):
        self.verb = verb
        self.verbProg = verbProg

    @staticmethod
    def helpDescription():
        return ""
        
    def _doCommand(self, player, world):
        pass
    
    def __call__(self, player, world):
        #print self.verbProg.capitalize()+"..."
        print
        self._doCommand(player, world)

# prikazy pohybu
class MoveCommand(Command):
    def __init__(self, quals):
        super(MoveCommand,self).__init__("JDI", u"jdu")
        self.direction = quals["direction"][0]

    @staticmethod
    def helpDescription():
        return u"""JDI nebo GO - jdi na SEVER, na JIH, na VÝCHOD, nebo na ZÁPAD 
          (může být zkráceno jako 'JDI S' a 'JDI Z', nebo dokonce jen 'V' a 'J')"""

    def _doCommand(self, player, world):
        rm = player.room
        if self.direction not in ["N","D"]:
            # zavolanim prepoctu smeru kam miri hrac
            self.direction = player.directions(self.direction)
            # ulozeni prepocteneho smeru kam miri hrac
            player.direction = self.direction

        nextRoom = rm.doors[ 
            {
            "S":0,
            "J":1,
            "V":2,
            "Z":3,
            "N":4,
            "D":5,
            }[self.direction]
            ]
    
        # pohyby bez kompasu osetrit tady - zavolat prepocet a pokud nelze
        # pouzit kompas, nabidnout jen pohyby rovne, doleva ...
        if nextRoom:
            if rm.moveAction:
                rm.moveAction(self,player,nextRoom,rm)
                if not player.gameOver and rm.canMove:
                    player.moveTo( nextRoom )
            elif not player.gameOver and rm.canMove:
                player.moveTo( nextRoom )
        else:
            print u"Tudy jít nemůžeš."


# prikaz sebrani predmetu
class TakeCommand(Command):
    def __init__(self, quals):
        super(TakeCommand,self).__init__("SEBER", u"beru")
        self.subject = quals["item"]

    @staticmethod
    def helpDescription():
        return u"SEBER nebo VEZMI nebo VEM - sebrat předmět (některé mohou ublížit)"
        
    def _doCommand(self, player, world):
        rm = player.room
        subj = Item.items[self.subject]
        if subj in rm.inv and subj.isVisible:
            if subj.isTakeable:
                if subj.takeAction:
                    if subj.takeItem( player, subj ) == True:
                        rm.removeItem(subj)
                        player.take(subj)
                else:
                    rm.removeItem(subj)
                    player.take(subj)
            else:
                if subj.takeAction:
                    subj.takeItem( player, subj )
                print u"To nemůžeš sebrat!"
        elif subj.isVisible == False:
            print u"Nejde to."
        elif subj in player.inv:
            print u"Vždyť máš %s v inventáři!" % subj
        else:
            print u"Nevidím tu %s." % subj

# prikaz polozeni predmetu
class DropCommand(Command):
    def __init__(self, quals):
        super(DropCommand,self).__init__("POLOŽ", u"pokládám")
        self.subject = quals["item"]

    @staticmethod
    def helpDescription():
        return u"POLOŽ - položí předmět (křehké předměty se mohou rozbít)"
        
    def _doCommand(self, player, world):
        rm = player.room
        subj = Item.items[self.subject]
        if subj in player.inv:
            if subj.dropAction:
                subj.dropItem( player, subj )
            rm.addItem(subj)
            player.drop(subj)
            
        else:
            print u"Nemáš %s." % (subj)

# prikaz inventar - co hrac ma u sebe
class InventoryCommand(Command):
    def __init__(self, quals):
        super(InventoryCommand,self).__init__("INV", u"prohlížím inventář")

    @staticmethod
    def helpDescription():
        return u"INVENTÁŘ nebo INV nebo I - vypíše předměty, které máš"
        
    def _doCommand(self, player, world):
        if player.inv:
            print u"Máš %s." % enumerateItems( player.inv )
        else:
            print u"Nemáš nic."

# prikaz situace - popis mistnosti kde se hrac nachazi
class LookCommand(Command):
    def __init__(self, quals):
        super(LookCommand,self).__init__("SIT", u"situace")

    @staticmethod
    def helpDescription():
        return u"SITUACE nebo SIT - popíše současnou lokaci společně s předměty a směry"
        
    def _doCommand(self, player, world):
        player.room.describe(player)

class DoorsCommand(Command):
    def __init__(self, quals):
        super(DoorsCommand,self).__init__("SMĚRY", u"rozhlížím se kolem")

    @staticmethod
    def helpDescription():
        return u"SMĚRY - zobrazí směry kudy můžeš jít"
        
    def _doCommand(self, player, world):
        rm = player.room
        numDoors = sum([1 for r in rm.doors if r is not None])
        if numDoors == 0:
            print u"Nemůžeš jít žádným směrem."
        else:
            if numDoors == 1:
                reply = u"Můžeš jít jen "
            else:
                reply = u"Můžeš jít "
            doorNames = [ {0:u"na sever", 1:u"na jih", 2:u"na východ", 3:u"na západ", 4:u"nahoru", 5:u"dolů"}[i] 
                          for i,d in enumerate(rm.doors) if d is not None ]
            #print doorNames
            reply += enumerateDoors( doorNames )
            reply += "."
            if rm.compass:
                print reply
            else:
                print player.dirDescr(rm)

# prikaz pouziti predmetu
class UseCommand(Command):
    def __init__(self, quals):
        super(UseCommand,self).__init__("POUŽIJ", u"používám")

        self.subject = Item.items[ quals["usedObj"] ]
        if "targetObj" in quals.keys():
            if quals["targetObj"] != None:
                self.target = Item.items[ quals["targetObj"] ]
            else:
                self.target = None

    @staticmethod
    def helpDescription():
        return u"POUŽIJ nebo POU - použít předmět, volitelně v nebo na jiném předmětu"
        
    def _doCommand(self, player, world):
        rm = player.room
        availItems = rm.inv+player.inv
        if self.subject in availItems:
            if self.subject.isUsable( player, self.target ):
                self.subject.useItem( player, self.target )
            else:
                print u"To zde použít nemůžeš."
        else:
            print u"Není zde %s pro použití." % self.subject

# prikaz otevreni predmetu
class OpenCommand(Command):
    def __init__(self, quals):
        super(OpenCommand,self).__init__("OTEVŘI", u"otvírám")
        self.subject = Item.items[ quals["item"] ]

    @staticmethod
    def helpDescription():
        return u"OTEVŘI nebo OTE nebo O - otevřít objekt"
        
    def _doCommand(self, player, world):
        rm = player.room
        availItems = rm.inv+player.inv
        if self.subject in availItems:
            if self.subject.isOpenable:
                if self.subject.isClosed:
                    self.subject.openItem( player, self.subject )
                elif self.subject.isOpened:
                    print u"Vždyť tu vidíš %s!" % self.subject
            else:
                self.subject.openItem( player, self.subject )
                print u"Nejde to otevřít."
        else:
            print u"Není zde %s pro použití." % self.subject

class CloseCommand(Command):
    def __init__(self, quals):
        super(CloseCommand,self).__init__("ZAVŘI", u"zavírám")
        self.subject = Item.items[ quals["item"] ]

    @staticmethod
    def helpDescription():
        return u"ZAVŘI nebo ZAV - zavřít objekt"
        
    def _doCommand(self, player, world):
        rm = player.room
        availItems = rm.inv+player.inv
        if self.subject in availItems:
            if self.subject.isOpened:
                self.subject.closeItem( player, self.subject )
            elif self.subject.isClosed:
                print u"Vždyť tu vidíš %s!" % self.subject
            else:
                print u"Nejde to zavřít."
        else:
            print u"Není zde %s pro použití." % self.subject

# prikaz prozkoumani predmetu
class ExamineCommand(Command):
    def __init__(self, quals):
        super(ExamineCommand,self).__init__("PROZKOUMEJ", u"zkoumám")
        self.subject = Item.items[ quals["item"] ]

    @staticmethod
    def helpDescription():
        return u"PROZKOUMEJ nebo PRO - prozkoumání objektu"
        
    def _doCommand(self, player, world):
        rm = player.room
        availItems = rm.inv+player.inv
        if self.subject in availItems:
            if self.subject.examineAction:
                self.subject.examineItem( player, self.subject )
            else:
                print self.subject.popis
            if self.subject.canInventory:
                if self.subject.inv:
                    print u"Uvnitř vidíš %s." % enumerateItems( self.subject.inv )
                else:
                    print u"Uvnitř nic není."
        else:
            print u"Nemohu prozkoumat %s." % self.subject


# prikaz vlozeni predmetu
class InsertCommand(Command):
    def __init__(self, quals):
        super(InsertCommand,self).__init__("VLOŽ", u"vkládám")
        self.subject = Item.items[ quals["item"] ]

    @staticmethod
    def helpDescription():
        return u"VLOŽ nebo VLO - vložení předmětu do jiného"
        
    def _doCommand(self, player, world):
        rm = player.room
        availItems = rm.inv+player.inv
        if self.subject in availItems:
            if self.subject.insertAction:
                self.subject.insertItem( player, self.subject )
            else:
                print "Nejde to."
        else:
            print u"Nemohu vložit %s." % self.subject

# prikaz score
class ScoreCommand(Command):
    def __init__(self, quals):
        super(ScoreCommand,self).__init__("SKÓRE", u"skóre")

    @staticmethod
    def helpDescription():
        return u"SKÓRE nebo SCORE - vypíše skóre hráče"
        
    def _doCommand(self, player, world):
        print u"Skóre:", player.score, " bodů"
        procent = float(player.score)/player.totalScore*100
        print u"Celkem dohráno: %.2f" % procent, "% příběhu"

# prikaz pro ukonceni hry
class QuitCommand(Command):
    def __init__(self, quals):
        super(QuitCommand,self).__init__("KONEC", u"ukončuji")

    @staticmethod
    def helpDescription():
        return u"KONEC nebo QUIT nebo Q - ukončí hru"
        
    def _doCommand(self, player, world):
        print u"Ok...."
        player.gameOver = True

# prikaz pro nahrani pozice - zatim pouze unixy
class LoadCommand(Command):
    def __init__(self, quals):
        super(LoadCommand,self).__init__("LOAD", u"načítám")

    @staticmethod
    def helpDescription():
        return u"LOAD - načte hru"
        
    def _doCommand(self, player, world):
        print u"LOAD...."
        # odkud nacitat - rozlisit unixy a win
        homedir = os.path.expanduser('~')
        try:
           from win32com.shell import shellcon, shell
           homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
        except ImportError:
           homedir = os.path.expanduser("~")
        try:
            f = open(homedir+'/.textovka/savegame', 'r')
        except IOError:
            print u"Soubor s uloženou hrou nelze přečíst, pravděpodobně neexistuje."
        # nacteni predmetu vcetne atributu a stavu
        Item.items = cPickle.load(f)
        
        # nacteni inventare hrace
        player.inv = cPickle.load(f)
        
        # vycisteni rozmisteni predmetu
        rozmisteni = {}
        
        # vymazani predmetu z mistnosti
        for mistnost in world:
            world[mistnost].inv = []
                
        # nacteni rozmisteni predmetu
        rozmisteni = cPickle.load(f)
        
        # vycisteni inventare
        player.inv =[]
        
        # umisteni predmetu do mistnosti a do inventare
        for predmet in Item.items.keys():
            if rozmisteni[predmet] == "v inventari":
                player.inv += [Item.items[predmet]]
            elif len(rozmisteni[predmet]) > 0:
                # smycka proleze pole zda neni predmet na vice mistech
                for mistnost in rozmisteni[predmet]:
                    world[mistnost].inv += [Item.items[predmet]]

        # ulozena pozice hrace na mape
        savedRoom = cPickle.load(f)
        
        # ulozene skore hrace
        player.score = cPickle.load(f)
        
        # ulozena sila hrace
        player.power = cPickle.load(f)
        
        #ulozeny smer a predchozi smer hrace
        player.direction = cPickle.load(f)
        player.prevDirection = cPickle.load(f)
        
        # nacteni informaci o mistnotech - popis, vychody, priznaky
        expMistnost = cPickle.load(f)
        # pri nastavovani vychodu z mistnosti je potreba vyhnout se None
        # proto jsou tam ty podminky > 0
        for mistnost in world:          
            world[mistnost].desc = expMistnost[locateRoom(world[mistnost], world)].get("desc")
            world[mistnost].gameOver = expMistnost[locateRoom(world[mistnost], world)].get("gameOver")
            if expMistnost[locateRoom(world[mistnost], world)].get("doors")[0] > 0:
                world[mistnost].doors[0] = world[expMistnost[locateRoom(world[mistnost], world)].get("doors")[0]]
            else:
                world[mistnost].doors[0] = None
            if expMistnost[locateRoom(world[mistnost], world)].get("doors")[1] > 0:
                world[mistnost].doors[1] = world[expMistnost[locateRoom(world[mistnost], world)].get("doors")[1]]
            else:
                world[mistnost].doors[1] = None
            if expMistnost[locateRoom(world[mistnost], world)].get("doors")[2] > 0:
                world[mistnost].doors[2] = world[expMistnost[locateRoom(world[mistnost], world)].get("doors")[2]]
            else:
                world[mistnost].doors[2] = None
            if expMistnost[locateRoom(world[mistnost], world)].get("doors")[3] > 0:
                world[mistnost].doors[3] = world[expMistnost[locateRoom(world[mistnost], world)].get("doors")[3]]
            else:
                world[mistnost].doors[3] = None
            if expMistnost[locateRoom(world[mistnost], world)].get("doors")[4] > 0:
                world[mistnost].doors[4] = world[expMistnost[locateRoom(world[mistnost], world)].get("doors")[4]]
            else:
                world[mistnost].doors[4] = None
            if expMistnost[locateRoom(world[mistnost], world)].get("doors")[5] > 0:
                world[mistnost].doors[5] = world[expMistnost[locateRoom(world[mistnost], world)].get("doors")[5]]
            else:
                world[mistnost].doors[5] = None
        
        f.close
        # presun do ulozene mistnosti
        player.moveTo( world[savedRoom] )    

# prikaz pro ulozeni pozice - zatim pouze unixy
class SaveCommand(Command):
    def __init__(self, quals):
        super(SaveCommand,self).__init__("SAVE", u"ukládám")

    @staticmethod
    def helpDescription():
        return u"SAVE - uloží hru"
        
    def _doCommand(self, player, world):
        print u"SAVE..."
        # kam ukladat - rozlisit unixy a win
        homedir = os.path.expanduser('~')
        try:
           from win32com.shell import shellcon, shell
           homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
        except ImportError:
           homedir = os.path.expanduser("~")
        try:
            try:
                os.mkdir(homedir+'/.textovka')
            except OSError:
                pass
            f = open(homedir+'/.textovka/savegame', 'w')
        except IOError:
            print u"Soubor neexistuje"
            return
        
        # ulozeni predmetu vcetne atributu a stavu
        cPickle.dump(Item.items,f)
        
        # ulozeni inventare hrace
        cPickle.dump(player.inv,f )
        
        # pomocna funkce pro ulozeni rozmisteni predmetu ve svete
        rozmisteni = {}
        for predmet in Item.items.keys():
                rozmisteni[predmet] = locateItem(player, world, predmet)
        
        # ulozeni rozmisteni predmetu
        cPickle.dump(rozmisteni,f)
        
        # zjisteni v jake mistnosti se nachazi hrac
        savedRoom = locateRoom(player.room,world)
        
        # ulozeni pozice hrace
        cPickle.dump (savedRoom,f)
        
        # ulozeni skore hrace
        cPickle.dump (player.score,f)

        # ulozeni sily hrace
        cPickle.dump (player.power,f)
        
        # ulozeni smeru a predchoziho smeru hrace
        cPickle.dump (player.direction,f)
        cPickle.dump (player.prevDirection,f)
        
        # ulozeni informaci o mistnotech - popis, vychody, priznaky
        expMistnost = {}
        for mistnost in world:
            expMistnost[mistnost] = {
                "desc": world[mistnost].desc,
                "gameOver": world[mistnost].gameOver,
                "doors": [locateRoom(world[mistnost].doors[0], world),
                    locateRoom(world[mistnost].doors[1], world),
                    locateRoom(world[mistnost].doors[2], world),
                    locateRoom(world[mistnost].doors[3], world),
                    locateRoom(world[mistnost].doors[4], world),
                    locateRoom(world[mistnost].doors[5], world)]
            }
        cPickle.dump (expMistnost,f)        
        f.close    

# prikaz napovedy
class HelpCommand(Command):
    def __init__(self, quals):
        super(HelpCommand,self).__init__("NÁPOVĚDA", u"napovídám")

    @staticmethod
    def helpDescription():
        return u"NÁPOVĚDA, HELP, POMOC nebo H nebo ? - zobrazí tuto nápovědu"
        
    def _doCommand(self, player, world):
        print u"Zadejte nějaký zásledujících příkazů (na velikosti písmen nezáleží):"
        for cmd in [
            InventoryCommand,
            DropCommand,
            TakeCommand,
            UseCommand,
            OpenCommand,
            ExamineCommand,
            InsertCommand,
            MoveCommand,
            LookCommand,
            DoorsCommand,
            ScoreCommand,
            QuitCommand,
            LoadCommand,
            SaveCommand,
            HelpCommand,
            ]:
            print "  - %s" % cmd.helpDescription()
        print

class AppParseException(ParseException):
    pass

# hlavni parser prikazu
# obsahuje seznam prikazu a volani funkci
class Parser(object):
    def __init__(self):
        self.bnf = self.makeBNF()
        
    def makeCommandParseAction( self, cls ):
        def cmdParseAction(s,l,tokens):
            
            return cls(tokens)
        return cmdParseAction
        
    def makeBNF(self):
        # potrebuji sem nejak dostat stav mistnosti ve ktere je hrac, pripadne atributy hrace (kompas ano/ne)
        
        invVerb = oneOf(u"INV INVENTÁŘ I", caseless=True) 
        dropVerb = oneOf(u"POLOŽ POL", caseless=True) 
        takeVerb = oneOf(u"SEBER VEZMI SEB VEZ VEM", caseless=True) | \
            (CaselessLiteral(u"PICK") + CaselessLiteral(u"UP") )
        moveVerb = CaselessLiteral(u"JDI") | empty | \
            (CaselessLiteral(u"JDI") + CaselessLiteral("NA") )
        useVerb = oneOf(u"POUŽIJ POU", caseless=True) 
        openVerb = oneOf(u"OTEVŘI OTE O", caseless=True)
        closeVerb = oneOf(u"ZAVŘI ZAV", caseless=True)
        examineVerb = oneOf(u"PROZKOUMEJ PRO", caseless=True)
        insertVerb = oneOf(u"VLOŽ VLO", caseless=True)
        scoreVerb = oneOf(u"SKÓRE SCORE", caseless=True)
        quitVerb = oneOf(u"KONEC QUIT Q", caseless=True) 
        loadVerb = oneOf(u"LOAD NAČTI", caseless=True) 
        saveVerb = oneOf(u"ULOŽ SAVE", caseless=True) 
        lookVerb = oneOf(u"SITUACE SIT", caseless=True) 
        doorsVerb = CaselessLiteral(u"SMĚRY")
        helpVerb = oneOf(u"NÁPOVĚDA POMOC HELP H ?",caseless=True)
          
        itemRef = OneOrMore(Word(alphas)).setParseAction( self.validateItemName )
                
        nDir = oneOf(u"S SEVER",caseless=True).setParseAction(replaceWith("S"))
        sDir = oneOf(u"J JIH",caseless=True).setParseAction(replaceWith("J"))
        eDir = oneOf(u"V VÝCHOD",caseless=True).setParseAction(replaceWith("V"))
        wDir = oneOf(u"Z ZÁPAD",caseless=True).setParseAction(replaceWith("Z"))
        uDir = oneOf(u"N NAHORU",caseless=True).setParseAction(replaceWith("N"))
        dDir = oneOf(u"D DOLŮ",caseless=True).setParseAction(replaceWith("D"))
        rovneDir = oneOf(u"R ROVNĚ",caseless=True).setParseAction(replaceWith("R"))
        vlevoDir = oneOf(u"L VLEVO",caseless=True).setParseAction(replaceWith("L"))
        vpravoDir = oneOf(u"P VPRAVO",caseless=True).setParseAction(replaceWith("P"))
        zpatkyDir = oneOf(u"O ZPĚT",caseless=True).setParseAction(replaceWith("O"))
        moveDirection = nDir | sDir | eDir | wDir | uDir | dDir | rovneDir | vlevoDir | vpravoDir | zpatkyDir
        
        invCommand = invVerb
        dropCommand = dropVerb + itemRef.setResultsName("item")
        takeCommand = takeVerb + itemRef.setResultsName("item")
        useCommand = useVerb + itemRef.setResultsName("usedObj") + \
            Optional(oneOf("V A NA S",caseless=True)) + \
            Optional(itemRef,default=None).setResultsName("targetObj")
        openCommand = openVerb + itemRef.setResultsName("item")
        closeCommand = closeVerb + itemRef.setResultsName("item")
        examineCommand = examineVerb + itemRef.setResultsName("item")
        insertCommand = insertVerb + itemRef.setResultsName("item")
        moveCommand = moveVerb + moveDirection.setResultsName("direction")
        quitCommand = quitVerb
        scoreCommand = scoreVerb
        loadCommand = loadVerb
        saveCommand = saveVerb
        lookCommand = lookVerb
        doorsCommand = doorsVerb
        helpCommand = helpVerb
        
        invCommand.setParseAction( 
            self.makeCommandParseAction( InventoryCommand ) )
        dropCommand.setParseAction( 
            self.makeCommandParseAction( DropCommand ) )
        takeCommand.setParseAction( 
            self.makeCommandParseAction( TakeCommand ) )
        useCommand.setParseAction( 
            self.makeCommandParseAction( UseCommand ) )
        openCommand.setParseAction( 
            self.makeCommandParseAction( OpenCommand ) )
        closeCommand.setParseAction( 
            self.makeCommandParseAction( CloseCommand ) )
        examineCommand.setParseAction( 
            self.makeCommandParseAction( ExamineCommand ) )
        insertCommand.setParseAction( 
            self.makeCommandParseAction( InsertCommand ) )
        moveCommand.setParseAction( 
            self.makeCommandParseAction( MoveCommand ) )
        scoreCommand.setParseAction( 
            self.makeCommandParseAction( ScoreCommand ) )
        quitCommand.setParseAction( 
            self.makeCommandParseAction( QuitCommand ) )
        loadCommand.setParseAction( 
            self.makeCommandParseAction( LoadCommand ) )
        saveCommand.setParseAction( 
            self.makeCommandParseAction( SaveCommand ) )
        lookCommand.setParseAction( 
            self.makeCommandParseAction( LookCommand ) )
        doorsCommand.setParseAction( 
            self.makeCommandParseAction( DoorsCommand ) )
        helpCommand.setParseAction( 
            self.makeCommandParseAction( HelpCommand ) )
        
        return ( invCommand | 
                  useCommand |
                  openCommand |
                  closeCommand |
                  examineCommand | 
                  dropCommand | 
                  takeCommand | 
                  insertCommand |           
                  lookCommand | 
                  doorsCommand |
                  loadCommand |
                  saveCommand | 
                  scoreCommand |                  
                  moveCommand |
                  helpCommand |
                  quitCommand ).setResultsName("command") + LineEnd()
    
    def validateItemName(self,s,l,t):
        iname = u" ".join(t)
        for i in t:
            if i in Item.items:
                return i
        raise AppParseException(s,l,u"Žádný předmět '%s'." % i )       

    def parseCmd(self, cmdstr):
        try:
            ret = self.bnf.parseString(cmdstr)
            return ret
        except AppParseException, pe:
            print pe.msg
        except ParseException, pe:
            print random.choice([ u"Lituji, tomu nerozumím.",
                                   u"Ehm?",
                                   u"Cože?",
                                   u"???",
                                   u"Co?" ] )
    
# trida hrac
class Player(object):
    def __init__(self, name, totalScore):
        self.name = name
        self.gameOver = False
        self.inv = []
        self.score = 0
        self.totalScore = totalScore
        self.power = 10
        self.direction = "S"
        self.prevDirection = "S"
        self.predirs = deque(['Z', 'S', 'V', 'J'])
    
    def moveTo(self, rm):
        self.room = rm
        rm.enter(self)
        if self.gameOver:
            if rm.desc:
                rm.describe(self)
            print u"Konec hry!"
        else:
            rm.describe(self)
    
    def take(self,it):
        if it.isDeadly:
            print u"Aaaagh!...., %s mě zabil!" % it
            self.gameOver = True
        else:
            self.inv.append(it)
    
    def drop(self,it):
        self.inv.remove(it)
        if it.isFragile:
            it.breakItem()
    def directions(self, smer):
        predirs = self.predirs

        # smer kterym hrac sel se prohlasi za rovne, ostatni se dopocitaji
        # dopocitane smery jsou [rovne,zpatky,doleva,doprava,nahoru,dolu]
        # nahoru a dolu se neprepocbitavaji
        # TODO: osetrit smery - udelat inverzni funkci na jakou svet. stranu jsem se vydal
        # pokud je predchozi smer nejaky a ted je rovne, tak je stejny atd
     
        # pohyb je jen rotace seznamu ctyr smeru [zapad,sever,vychod,jih] doleva je predchozi prvek
        # doprava nasledujici, otoceni je doprava(doleva) druhy nasledujici
        
        if smer == "R":
            smer = predirs[1]
            self.direction = smer
            self.prevDirection = smer
            self.predirs = predirs

        elif smer == "O":
            predirs.rotate(2)
            smer = predirs[1]
            self.predirs = predirs
            self.direction = smer
            self.prevDirection = smer

        elif smer == "L":
            predirs.rotate(1)
            smer = predirs[1]
            self.predirs = predirs
            self.direction = smer
            self.prevDirection = smer
        
        elif smer == "P":
            predirs.rotate(-1)
            smer = predirs[1]
            self.predirs = predirs
            self.direction = smer
            self.prevDirection = smer
            
        elif smer == "Z":          
            predirs = deque(['J', 'Z', 'S', 'V'])
            smer = predirs[1]
            self.predirs = predirs
            self.direction = smer
            self.prevDirection = smer

        elif smer == "V":          
            predirs = deque(['S', 'V', 'J', 'Z'])
            smer = predirs[1]
            self.predirs = predirs
            self.direction = smer
            self.prevDirection = smer
        
        elif smer == "S":          
            predirs = deque(['Z', 'S', 'V', 'J'])
            smer = predirs[1]
            self.predirs = predirs
            self.direction = smer
            self.prevDirection = smer

        elif smer == "J":          
            predirs = deque(['V', 'J', 'Z', 'S'])
            smer = predirs[1]
            self.predirs = predirs
            self.direction = smer
            self.prevDirection = smer

        return smer
        
    def dirDescr(self, rm):
        self.room = rm
        smer = self.direction
       
        directions =[]
        if smer == "S":
            directions = [rm.doors[0],rm.doors[1],rm.doors[3],rm.doors[2],rm.doors[4],rm.doors[5]]
            
        if smer == "J":
            directions = [rm.doors[1],rm.doors[0],rm.doors[2],rm.doors[3],rm.doors[4],rm.doors[5]]
            
        if smer == "V":
            directions = [rm.doors[2],rm.doors[3],rm.doors[0],rm.doors[1],rm.doors[4],rm.doors[5]]

        if smer == "Z":
            directions = [rm.doors[3],rm.doors[2],rm.doors[1],rm.doors[0],rm.doors[4],rm.doors[5]]
        
        numDoors = sum([1 for r in directions if r is not None])
        if numDoors == 0:
            print u"Nemůžeš jít žádným směrem."        
        else:
            reply = u"Můžeš jít "
            directionNames = [ {0:u"rovně", 1:u"zpátky", 2:u"doleva", 3:u"doprava", 4:u"nahoru", 5:u"dolů"}[i] 
                        for i,d in enumerate(directions) if d is not None ]
            #print doorNames
            reply += enumerateDoors( directionNames )
            reply += "."
            return reply



# pocatecni vytvoreni mapy mistnosti
def createRooms( rm ):
    """
    create rooms, using multiline string showing map layout
    """
    # start with empty dictionary of rooms
    # vymazani mapy
    ret = {}
    
    # nacteni mapy propojeni mistnosti
    
    rows = rm.split("\n")
    rows.pop()
    pocet = range(len(rows))
    pocet.remove(0)
    line = 1
    for line in pocet:
        smery = rows[line].split()
        ret[line] = Room(line)
        room = ret[line]
        s = None
        j = None
        v = None
        z = None
        n = None
        d = None
    
    for line in pocet:
        s = None
        j = None
        v = None
        z = None
        n = None
        d = None
        room = ret[line]
        smery = rows[line].split()
        
        
        if smery[0] !="0":
            s = ret[int(smery[0])]
        if smery[1] !="0":
            j = ret[int(smery[1])]
        if smery[2] !="0":
            v = ret[int(smery[2])]
        if smery[3] !="0":
            z = ret[int(smery[3])]
        if smery[4] !="0":
            n = ret[int(smery[4])]
        if smery[5] !="0":
            d = ret[int(smery[5])]
        
        # set connections to neighboring rooms
        # nastaveni propojeni s okolnimi mistnostmi
        room.doors=[s,j,v,z,n,d]
    
    return ret

# put items in rooms
# umisteni predmetu do mistnosti
def putItemInRoom(i,r):
    if isinstance(r,basestring):
        r = rooms[r]
    r.addItem( Item.items[i] )

# odebrani predmetu z mistnosti
def rmItemFromRoom(i,r):
    if isinstance(r,basestring):
        r = rooms[r]
    r.removeItem( Item.items[i] )

# kde se nachazi predmet
def locateItem(p,w,i):
    mistnosti = []
    if isinstance(i,basestring):
        i = Item.items[i]
    if i in p.inv:
        return "v inventari"
    for mistnost in w:
        # tady musi byt nejak osetreno kdyz je predmet ve vice mistnostech naraz
        if i in w[mistnost].inv:
            # pridat mistnost do pole potom v load save projet pole smyckou
            mistnosti.append(mistnost)
    return mistnosti

# preklad objektu mistnosti na cislo
def locateRoom(p,w):
    if p == None:
        return None
    for mistnost in w:
        if p == w[mistnost]:
            return mistnost

    
def playGame(p,world,startRoom):
    # create parser
    # hlavni smycka hry
    parser = Parser()
    p.moveTo( startRoom )
    while not p.gameOver:
        #doplnuje jen dostupne predmety z mistnosti, z inventare a slovesa
        availItems = p.room.inv + p.inv 
        slovesa = [u"otevři", u"zavři", u"situace", u"prozkoumej", u"použij",\
         u"seber", u"polož", u"inventář", u"směry", u"vlož", u"skóre", u"load", u"save",\
         u"quit", u"help", u"pomoc", u"sever", u"jih", u"západ", u"východ", u"nahoru", u"dolů"]
        if sys.platform == "win32":
            slovesaU = [unicode(s).encode("cp852") for s in slovesa]
            predmety = [unicode(s).encode("cp852") for s in availItems]
        else:
            slovesaU = [unicode(s).encode("utf-8") for s in slovesa]
            predmety = [unicode(s).encode("utf-8") for s in availItems]
        #doplnovani = slovesa + predmety
        doplnovani = slovesaU + predmety
        completer = Completer(doplnovani)
        
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer.complete)

        cmdstr = raw_input(u"> ")
        if sys.platform == "win32":
            # windows stale pouzivaji stare kodovani z dob ms-dosu
            cmdstr = unicode(cmdstr.decode("cp852"))
        else:
            # moderni operacni systemy uz pouzivaji unicode
            cmdstr = unicode(cmdstr.decode("utf-8"))     
        cmd = parser.parseCmd(cmdstr)
        if cmd is not None:
            cmd.command( p, world )
    print
    print u"Ukončil jsi hru."
    #print u"Náhodný kolemjdoucí našel:"
    #for i in p.inv:
    #    print u" - %s" % i


