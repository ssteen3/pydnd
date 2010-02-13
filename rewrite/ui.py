from server_characteristics import *

class Game:
    """
    This handles pygame and the interactions between pygame
    and the server Area class
    """
    def __init__(self, resx=640, resy=480, sqx=32, sqy=24):
        self.resx = resx
        self.resy = resy
        self.sqx = sqx
        self.sqy = sqy
        pygame.init()
        self.screen = pygame.display.set_mode((self.resx, self.resy))

    def draw_grid(self):
        color = [0, 0, 0, 0]
        rge = range(0,self.sqy)
        for count in rge:
            self.linesh[count] = pygame.draw.line(self.images[self.bg],color,(0,count*self.resy/self.sqy),(self.resx,count*self.resy/self.sqy),1)

        rge = range(0,self.sqx)
        for count in rge:
            self.linesw[count] = pygame.draw.line(self.images[self.bg],color,(count*self.resx/self.sqx,0),(count*self.resx/self.sqx,self.resy),1)
