import pygame
import random
from pygame.locals import *

class screenhandler:
	def __init__(self,root,w,h,sw,sh,bg='.\\hi.gif',easybutton='y',bw=2,bh=0,bspace=1):
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
		self.sel = piece(0,0,0,0,0,0,0) #null piece
		self.setbg(bg)
		self.makedummychars()
		if easybutton == 'y':
			self.buttonstart(bw,bh,bspace)
		self.update()
		
	def makedummychars(self):
		self.createpiece(250,350,'bob','.\\char.png',50,50)
		self.createpiece(30,350,'john','.\\char.png',50,50)
		self.createpiece(100,350,'jack','.\\char1.png',40,40)
		
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
		
	def buttonstart(self, width, height=0,spacing=1):
		self.buttonspace = spacing
		self.buttonmode = 'standard'
		x,y = self.root.get_size()
		buttonspacer = x - self.w
		buttonspaceb = y - self.h
		if buttonspacer == 0:
			self.buttonmode = 'bottom'
			#note need to add other button mode compatibilities
			print('Warning: button mode not yet supported, may be caused due to screen resolution')
		else:
			if height == 0:
				self.bthigh = int(self.h/(25+self.buttonspace))
				self.buttonheight = 25
			else:
				self.bthigh = height
				self.buttonheight = int(self.h/self.bthigh) - self.buttonspace

			self.btwide = width			
			self.buttonwidth = int(buttonspacer/self.btwide) - self.buttonspace
			self.numbuttonst = -1
			self.numbuttonsb = -1
		
	def easybutton(self, name, color, function, align='top'):
		#note need to add other button mode compatibilities
		if self.buttonmode == 'standard':
			if align == 'top':
				print('Making Button')
				self.numbuttonst += 1
				return self.makebutton( self.w + self.buttonspace + (self.numbuttonst%self.btwide)*(self.buttonwidth+self.buttonspace),self.buttonspace + int(self.numbuttonst/self.btwide)*(self.buttonheight+self.buttonspace),self.buttonwidth, self.buttonheight, name, color, function)
			elif align == 'bottom':
				self.numbuttonsb += 1
				return self.makebutton( self.w + self.buttonspace + (self.numbuttonsb%self.btwide)*(self.buttonwidth+self.buttonspace),self.buttonspace + (self.bthigh-1-int(self.numbuttonsb/self.btwide))*(self.buttonheight+self.buttonspace),self.buttonwidth, self.buttonheight, name, color, function)

		else:
			print('Warning: button mode not yet supported')
	
	def easyrmbutton(self, num, align='top'):
		if align == 'top':
			for i in range(num):
				last = self.butnames.pop()
				self.butnames.append(last)
				self.removebutton(last)
				self.numbuttonst -= 1
		else:
				last = self.butnames.pop()
				self.butnames.append(last)
				self.removebutton(last)
				self.numbuttonsb -= 1
		
	def makebutton(self, left, top, width, height, name, color, function):
		font = pygame.font.Font(None, 36)
		text = font.render(name, 0, (10, 10, 10))

		self.butnames.append(name)
		self.buttons[name] = Rect(left,top,width,height)
		self.butfuncs[name] = function
		pygame.draw.rect(self.root,color,self.buttons[name])
		self.root.blit(text, self.buttons[name])
		return self.buttons[name]

	def removebutton(self, name):
		if name in self.butnames:
			black = [0,0,0,0]
			pygame.draw.rect(self.root,black,self.buttons[name])
			self.butnames.remove(name)
			del self.buttons[name]
			del self.butfuncs[name]
		else:
			print('Error: Button ',name,' does not exist')
		
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

	def updatepieces(self):
		for sel in self.pieces.keys():
			self.pieces[sel].updateloc()

	def setbg(self,ifile):
		self.drawimage(ifile,x=0,y=0)
		self.bg = ifile
		self.drawgrid()
		#self.images[self.bg] = self.images[self.bg].convert()
		
	def update(self):
		self.updateimage(ifile=self.bg,x=0,y=0)
		self.updatepieces()
		pygame.display.update()
		pygame.display.flip()
		

	def drawgrid(self):
		color = [0, 0, 0, 0]
		onetonumber = range(0,self.sh)		
		for count in onetonumber:
			self.linesh[count] = pygame.draw.line(self.images[self.bg],color,(0,count*self.h/self.sh),(self.w,count*self.h/self.sh), 1)
		onetonumbertwo = range(0,self.sw)
		for count in onetonumbertwo:
			self.linesw[count] = pygame.draw.line(self.images[self.bg],color,(count*self.w/self.sw,0),(count*self.w/self.sw,self.h), 1)
	def drawimage(self,ifile,x,y):
		self.images[ifile] = pygame.image.load(ifile)
		screen.blit(self.images[ifile], (x,y))
		
	def updateimage(self,ifile,x,y):
		screen.blit(self.images[ifile], (x,y))
	def updatebg(self):
		self.setbg(self.bg)

class piece:
	def __init__(self,root,x,y,image,name,iw,ih):
		self.grid = root
		self.midx = x + iw/2
		self.midy = y + ih/2
		self.locx = x
		self.locy = y
		self.ifile = image
		self.myname = name
		self.initiative = random.randrange(1,40,1)
		print(self.initiative)
		if iw > 0:
			self.createloc()
			self.sq = self.grid.getsquare(self.midx,self.midy)
			
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
		cancel = self.grid.easybutton('Cancel', white, exit)
		go = self.grid.easybutton('Go', white, exit)
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
							self.grid.easyrmbutton(2)
							self.sel(red)
							self.grid.update()
							return
						if (go.collidepoint(z[0],z[1])):
							self.grid.easyrmbutton(2)
							self.movelist(mvsquares)
							return
						self.grid.handlemouse(z[0],z[1])
					else:
						if (cur[0] == x) and (cur[1] == y):
							mvsquares.remove(cur)
							if (len(mvsquares)>1):
								last = mvsquares.pop()
								if (abs(cur[0]-last[0])>0) and (abs(cur[1]-last[1])>0):
									sqleft += 15
								elif (abs(cur[0]-last[0])>0) or (abs(cur[1]-last[1])>0):
									sqleft += 10								
								mvsquares.append(last)
								cur = last

							elif (len(mvsquares)>0):
								if (abs(cur[0]-self.sq[0])>0) and (abs(cur[1]-self.sq[1])>0):
									sqleft += 15
								elif (abs(cur[0]-self.sq[0])>0) or (abs(cur[1]-self.sq[1])>0):
									sqleft += 10
								cur = mvsquares.pop()
								mvsquares.append(cur)

							else:
								if (abs(cur[0]-self.sq[0])>0) and (abs(cur[1]-self.sq[1])>0):
									sqleft += 15
								elif (abs(cur[0]-self.sq[0])>0) or (abs(cur[1]-self.sq[1])>0):
									sqleft += 10							
								cur = self.grid.getsquare(self.midx,self.midy)
							self.grid.selsquare(z[0],z[1],black,0)
							self.grid.update()
						elif (abs(cur[0]-x)<2) and (abs(cur[1]-y)<2):
							if (abs(cur[0]-x)>0) and (abs(cur[1]-y)>0):
								var = 15
							elif (abs(cur[0]-x)>0) or (abs(cur[1]-y)>0):
								var = 10
							if sqleft >= var:
								if not (next in mvsquares):
									sqleft -= var
									mvsquares.append(next)
									self.grid.selsquare(z[0],z[1],green,0)
									self.grid.update()
									cur = next
							else:
								print('out of movement')

	def movelist(self,mvsquares):
		for square in mvsquares:
			self.smovesq(square[0],square[1])
			
		
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
		self.sq = self.grid.getsquare(self.midx,self.midy)
		
	def getx(self):
		return self.locx
		
	def gety(self):
		return self.locy

	def getname(self):
		return self.myname
		
	def createloc(self):
		self.grid.drawimage(ifile=self.ifile,x=self.locx,y=self.locy)
		
	def updateloc(self):
		self.grid.updateimage(ifile=self.ifile,x=self.locx,y=self.locy)
		
	

#start
random.seed()
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('DnD Engine')


#Display text
#font = pygame.font.Font(None, 36)
#text = font.render("Hello There", 1, (10, 10, 10))
#textpos = text.get_rect()
#textpos.centerx = background.get_rect().centerx
#screen.blit(background, (0,0))

objects = []
grid = screenhandler(screen,600,600,15,15)
white = [255,255,255,255]
grid.easybutton('Exit',white,exit,align='bottom')
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
				