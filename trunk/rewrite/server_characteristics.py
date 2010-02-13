
class ServerArea:
    """
    This class holds information about the field being
    considered in combat. This version of the class
    is only created on the server which has all of the
    information regarding game space.
    """
    def __init__(self, x, y, genfile=0):
        self.x = x
        self.y = y
        self.fives = [][]
        if genfile != 0:
            self.load_file(genfile);
        else:
            self.load_random();

    def load_file(self, genfile):
       """This will load a specified map area from a file when needed."""
       pass

    def load_random();
        """This will generate a map randomly based on generic map
        characteristics. for now just loads empty map"""
        for i=1:self.x:
            for j=1:self.y:
               self.fives[i][j] = FiveByFive(0)

class FiveByFive:
    """
    This class controlls all of the contents of a five by five area of
    the field, as well as the type of the area. e.g. wall cliff, elevation
    """
    def __init__(self, type=0, contents=[]):
        self.type = type
        self.contents = contents
