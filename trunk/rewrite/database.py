
class Database:
    """
    This class holds the playfield, the players and the initiative
    list, it parses the initiative list and informs client and server
    of what messages need to be passed in each direction.
    """
    def __init__(self, x, y, genfile=0, pgen=0, ngen=0, server):
        self.area = Area(x,y,genfile)
        self.playerset = Players(pgen)
        self.npcs = NPCs(ngen)
        self.initiative = []
        self.state = 0
        self.server = server

    def proc_init(self):
        """
        process one players initiative, if it is an npc then process
        completely and move to another, if player then return the 
        message that needs to be passed to client or server database
        """
        initiate = self.initiative.pop()
        self.initiative.append(initiate)
        if initiate.isnpc
            initiate.process(self)
            self.proc_init()
        else
            initiate.process(self)

class CLDatabase(Database):
    """
    This class is a duplicate of the server database class
    but contains some additional functions to handle the 
    recieving and parsing of messages
    """
    def __init__(self, x, y, genfile=0, pgen=0, ngen=0, client):
        Database.__init__(self,x,y,genfile,pgen,ngen,0)
        self.client = client

class Area:
    """
    This class holds information about the field being
    considered in combat. This version of the class
    is only created on the server which has all of the
    information regarding game space.
    """
    def __init__(self, x, y, genfile):
        self.x = x
        self.y = y
        self.fives = []
        if genfile != 0:
            self.load_file(genfile);
        else:
            self.load_random();

    def load_file(self, genfile):
       """This will load a specified map area from a file when needed."""
       pass

    def load_random():
        """This will generate a map randomly based on generic map
        characteristics. for now just loads empty map"""
        for i in range(0,(self.x-1)):
            for j in range(1,self.y):
               self.fives[(i)*self.y+j] = FiveByFive(0)

class FiveByFive:
    """
    This class controlls all of the contents of a five by five area of
    the field, as well as the type of the area. e.g. wall cliff, elevation
    """
    def __init__(self, type=0, contents=[]):
        self.type = type
        self.contents = contents
