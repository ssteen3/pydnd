
import pygame
from pygame.locals import *

class gridarea:
	def __init__(self,root,w,h,sw,sh):
		self.pieces = {}
		self.images = {}
		self.butnames = []
		self.buttons = {}
		self.butfuncs = {}
		self.item = {}
		self.linesh = {}
		self.linesw = {}
		self.csa = 1
		self.root = root
		self.w = w
		self.h = h
		self.sw = sw
		self.sh = sh
		self.bg = 0
		#self.canvas.pack()
		#self.canvas.grid()
		self.sel = piece(0,0,0,0,0,0,0)
		self.setbg('.\\hi.gif')
		self.createpiece(250,350,'bob','.\\char.png',50,50)
		self.createpiece(30,350,'john','.\\char.png',50,50)
		self.createpiece(100,350,'jack','.\\char1.png',40,40)
		self.update()
		
	def selchar(self,name):
		self.sel = self.pieces[name]
		
	def selsquare(self, x, y, color, ref):
		if ref == 1:
			self.updatebg()
		sx, sy = self.getsquare(x,y)
		pygame.draw.line(self.images[self.bg],color,(sx*self.w/self.sw,sy*self.h/self.sh),((sx+1)*self.w/self.sw,sy*self.h/self.sh), 3)
		pygame.draw.line(self.images[self.bg],color,(sx*self.w/self.sw,sy*self.h/self.sh),(sx*self.w/self.sw,(sy+1)*self.h/self.sh), 3)
		pygame.draw.line(self.images[self.bg],color,(sx*self.w/self.sw,(sy+1)*self.h/self.sh),((sx+1)*self.w/self.sw,(sy+1)*self.h/self.sh), 3)
		pygame.draw.line(self.images[self.bg],color,((sx+1)*self.w/self.sw,sy*self.h/self.sh),((sx+1)*self.w/self.sw,(sy+1)*self.h/self.sh), 3)
		return sx, sy
		
		
	def getsquare(self, x, y):
		sx = int(x / (self.w/self.sw))
		sy = int(y / (self.h/self.sh))
		return sx,sy
		
	def tox(self, x):
		return x*self.w/self.sw
	
	def toy(self, y):
		return y*self.h/self.sh
		
	def makebutton(self, left, top, width, height, name, color, function):
		font = pygame.font.Font(None, 36)
		text = font.render(name, 0, (10, 10, 10))

		self.butnames.append(name)
		self.buttons[name] = Rect(left,top,width,height)
		self.butfuncs[name] = function
		pygame.draw.rect(self.root,color,self.buttons[name])
		self.root.blit(text, self.buttons[name])
		return self.buttons[name]

	def getsel(self):
		return self.sel
		
	def handlemouse(self, x,y):
		red = [255,0,0,255]
		for but in self.butnames:
			if (self.buttons[but].collidepoint(x, y)):
				self.butfuncs[but]()
		if x <= 600:
			sx,sy = self.getsquare(x,y)
			for sel in self.pieces.keys():
				if self.pieces[sel].inxy(sx,sy) == 1:
					self.selsquare(x,y,red,1)
					self.update()
					self.sel = self.pieces[sel]

	def createpiece(self,x,y,name,ifile,iw,ih):
		color = [0,255,0,255]
		self.pieces[name] = piece(self,x,y,ifile,name,iw,ih)
		self.pieces[name].sel(color)
		self.sel = self.pieces[name]

	def setbg(self,ifile):
		self.drawimage(ifile,x=0,y=0)
		self.bg = ifile
		self.drawgrid()
		#self.images[self.bg] = self.images[self.bg].convert()
		
	def updatebg(self):
		self.setbg(self.bg)
		
	def update(self):
		self.updateimage(ifile=self.bg,x=0,y=0)
		self.updatepieces()
		pygame.display.update()
		pygame.display.flip()
		
	def updatepieces(self):
		for sel in self.pieces.keys():
			self.pieces[sel].updateloc()
	
#redraws the grid
	def drawgrid(self):
		color = [0, 0, 0, 0]
		onetonumber = range(0,self.sh)		
		for count in onetonumber:
			self.linesh[count] = pygame.draw.line(self.images[self.bg],color,(0,count*self.h/self.sh),(self.w,count*self.h/self.sh), 1)
		onetonumbertwo = range(0,self.sw)
		for count in onetonumbertwo:
			self.linesw[count] = pygame.draw.line(self.images[self.bg],color,(count*self.w/self.sw,0),(count*self.w/self.sw,self.h), 1)

#adds image to canvas
	def drawimage(self,ifile,x,y):
		self.images[ifile] = pygame.image.load(ifile)
		screen.blit(self.images[ifile], (x,y))
		
	def updateimage(self,ifile,x,y):
		screen.blit(self.images[ifile], (x,y))

class piece:
	def __init__(self,root,x,y,image,name,iw,ih):
		self.grid = root
		self.midx = x + iw/2
		self.midy = y + ih/2
		self.locx = x
		self.locy = y
		self.ifile = image
		self.myname = name
		if iw > 0:
			self.createloc()
			
	def inxy(self,x,y):
		sx,sy = self.grid.getsquare(self.midx,self.midy)
		if x == sx:
			if sy == y:
				return 1
			else:
				return 0
			
	def selectmove(self, mod):
		print('Now Entering Select Move Mode')
		red = [255,0,0,255]
		green = [0,255,0,255]
		black = [0,0,0,0]
		white = [255,255,255,255]
		cancel = self.grid.makebutton(601, 53, 98, 25, 'Cancel', white, exit)
		go = self.grid.makebutton(701, 53, 98, 25, 'Go', white, exit)
		self.grid.update()
		print('Created Buttons')
		self.grid.makebutton
		mvsquares = []
		speed = 40*mod
		sqleft = speed
		self.sel(red)
		cur = self.grid.getsquare(self.midx,self.midy)
		self.grid.update()
		while 1:
			for event in pygame.event.get():
				if event.type == QUIT:
					print('Quiting')
					exit()
				elif event.type == MOUSEBUTTONDOWN:
					z = pygame.mouse.get_pos()
					next = self.grid.getsquare(z[0],z[1])
					x,y = next
					if (x > 14):
						if (cancel.collidepoint(z[0],z[1])):
							return
						if (go.collidepoint(z[0],z[1])):
							self.movelist(mvsquares)
							return
						self.grid.handlemouse(z[0],z[1])
					else:
						if sqleft > 5:
							if (cur[0] == x) and (cur[1] == y):
								mvsquares.remove(cur)
								if (len(mvsquares)>0):
									cur = mvsquares.pop()
									mvsquares.append(cur)
								else:
									cur = self.grid.getsquare(self.midx,self.midy)
								self.grid.selsquare(z[0],z[1],black,0)
								self.grid.update()
							elif (abs(cur[0]-x)<2) and (abs(cur[1]-y)<2):
								if not (next in mvsquares):
									if (abs(cur[0]-x)>0) and (abs(cur[1]-y)>0):
										sqleft -= 15
									elif (abs(cur[0]-x)>0) or (abs(cur[1]-y)>0):
										sqleft -= 10
									mvsquares.append(next)
									self.grid.selsquare(z[0],z[1],green,0)
									self.grid.update()
									cur = next
						else:
							print('out of movement')

	def movelist(self,mvsquares):
		for square in mvsquares:
			self.smovesq(square[0],square[1])
			
	def getname(self):
		return self.myname
		
	def goxy(self,x,y):
		self.locx = x
		self.locy = y
		
	def sel(self,color):
		self.grid.selsquare(self.midx,self.midy,color,1)
		
	def rmove(self,x,y):
		self.locx += x
		self.midx += x
		self.locy += y
		self.midy += y
	
	def smovesq(self,x,y):
		self.smove(self.grid.tox(x+.5),self.grid.toy(y+.5))
	
	def smove(self,desx,desy):
		incx = 0
		incy = 0
		red = [255,0,0,255]
		if (desx > self.midx):
			incx = 1
		if (desx < self.midx):
			incx = -1
		if (desy > self.midy):
			incy = 1
		if (desy < self.midy):
			incy = -1
		while ((desx-self.midx) or (desy-self.midy)):
			self.locx += incx
			self.locy += incy
			self.midx += incx
			self.midy += incy
			self.grid.update()
			pygame.time.delay(1)
			if ((desx-self.midx)==0):
				incx=0
			if ((desy-self.midy)==0):
				incy=0
			for event in pygame.event.get():
				pass
			self.sel(red)
		
	def getx(self):
		return self.locx
		
	def gety(self):
		return self.locy
		
	def createloc(self):
		self.grid.drawimage(ifile=self.ifile,x=self.locx,y=self.locy)
		
	def updateloc(self):
		self.grid.updateimage(ifile=self.ifile,x=self.locx,y=self.locy)
		
		
#start
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('DnD Engine')

#images and background
#background = pygame.image.load('testing.jpg').convert()


#Display text
#font = pygame.font.Font(None, 36)
#text = font.render("Hello There", 1, (10, 10, 10))
#textpos = text.get_rect()
#textpos.centerx = background.get_rect().centerx
#screen.blit(background, (0,0))
objects = []
grid = gridarea(screen,600,600,15,15)
RED = [255,255,255,255]
grid.makebutton(601,1,98,25,'Exit',RED,exit)
grid.update()
color= [255,0,0,255]
print(grid.getsel().getname())
#grid.onleft()
#grid.onright()
key = 0
while 1:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		elif event.type == MOUSEBUTTONDOWN:
			print('Mouse Input')
			z = pygame.mouse.get_pos()
			grid.handlemouse(z[0],z[1])
		elif event.type == KEYDOWN:
			key = event.key

			if key == 273:
				grid.selchar('bob')
			#	grid.getsel().rmove(0,-5)
			if key == 274:
				grid.selchar('john')
			#	grid.getsel().rmove(0,5)
			if key == 276:
				grid.selchar('jack')
			#	grid.getsel().rmove(-5,0)
			#if key == 275:
			#	grid.getsel().rmove(5,0)
			#grid.getsel().sel(color)
			grid.getsel().selectmove(1)
			grid.update()
		elif event.type == KEYUP:
			key = 0