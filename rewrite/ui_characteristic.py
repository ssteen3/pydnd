from server_characteristics import *
import pygame

class Game:
    """
    This handles pygame and the interactions between pygame
    and the server Area class
    """
    def __init__(self, host=localhost, port=6000, resx=640, resy=480, sqx=32, sqy=24):
        self.resx = resx
        self.resy = resy
        self.sqx = sqx
        self.sqy = sqy
        self.anchor = (0,0)
        self.database = 0
        self.client = Client(host,port)
        pygame.init()
        self.screen = pygame.display.set_mode((self.resx, self.resy))

    def draw_grid(self):
        """This adds grid to screen based on number of visible squares"""
        color = [0, 0, 0, 0]
        rge = range(0,self.sqy)
        for count in rge:
            self.linesh[count] = pygame.draw.line(self.images[self.bg],color,(0,count*self.resy/self.sqy),(self.resx,count*self.resy/self.sqy),1)

        rge = range(0,self.sqx)
        for count in rge:
            self.linesw[count] = pygame.draw.line(self.images[self.bg],color,(count*self.resx/self.sqx,0),(count*self.resx/self.sqx,self.resy),1)

    def main_loop(self):
        while 1:
            self.update_game()
            self.update_screen()

    def 
