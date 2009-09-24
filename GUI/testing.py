from tkinter import *
from tkinter.ttk import *
from time import *
#from pyx import *

#class to handle grid, constructor takes root, width, height, squares wide, and squares high
class gridarea:
	def __init__(self,root,w,h,sw,sh):
		self.canvas = Canvas(root,width=w,height=h, bg='white')
		self.pieces = {}
		self.tkim = {}
		self.item = {}
		self.linesh = {}
		self.linesw = {}
		self.root = root
		self.w = w
		self.h = h
		self.sw = sw
		self.sh = sh
		self.bg = 0
		#self.canvas.pack()
		#self.canvas.grid()
		self.createpiece(250,350,'bob','C:\\Users\\jmonk\\char.gif')
		self.createpiece(30,350,'john','C:\\Users\\jmonk\\char.gif')
		self.setbg('C:\\Users\\jmonk\\hi.gif')
		self.canvas.grid()
		self.update()

		
	def createpiece(self,x,y,name,ifile):
		self.pieces[name] = piece(self,x,y,ifile,name)
		
	def onleft(self):
		self.pieces['bob'].smove(self,50,50)
		self.update()
		self.pieces['john'].smove(self,100,50)
		self.update()
	
	def onright(self):
		self.pieces['bob'].smove(self,500,500)
		self.pieces['john'].smove(self,450,500)
		self.update()

	def setbg(self,ifile):
		self.drawimage(ifile,x=self.w/2,y=self.h/2)
		self.bg = ifile
		
	def update(self):
		self.canvas.delete('all')
		self.updateimage(ifile=self.bg,x=self.w/2,y=self.h/2)
		self.updatepieces()
		self.drawgrid()
		
	def updatepieces(self):
		for sel in self.pieces.keys():
			self.pieces[sel].updateloc()
	
#redraws the grid
	def drawgrid(self):
		onetonumber = range(0,self.sh)
		for count in onetonumber:
			self.linesh[count] = self.canvas.create_line(0,count*self.h/self.sh,self.w,count*self.h/self.sh, tags="arb")
			self.canvas.itemconfig(self.linesh[count],tags=("grid"))
		onetonumbertwo = range(0,self.sw)
		for count in onetonumbertwo:
			self.linesw[count] = self.canvas.create_line(count*self.w/self.sw,0,count*self.w/self.sw,self.h, tags="arb")
			self.canvas.itemconfig(self.linesw[count],tags=("grid"))
		self.canvas.addtag_withtag("three","grid")

#adds image to canvas
	def drawimage(self,ifile,x,y):
		self.tkim[ifile] = PhotoImage(file=ifile)
		self.item[ifile] = self.canvas.create_image(x,y,image=self.tkim[ifile])
		
	def updateimage(self,ifile,x,y):
		self.item[ifile] = self.canvas.create_image(x,y,image=self.tkim[ifile])

		

class piece:
	def __init__(self,root,x,y,image,name):
		self.grid = root
		self.locx = x
		self.locy = y
		self.ifile = image
		self.myname = name
		self.createloc()
		
	def goxy(self,x,y):
		self.locx = x
		self.locy = y
		
		#will error out when running
	def smove(self,root,desx,desy):
		incx = 0
		incy = 0
		if (desx > self.locx):
			incx = 1
		if (desx < self.locx):
			incx = -1
		if (desy > self.locy):
			incy = 1
		if (desy < self.locy):
			incy = -1
		while ((desx-self.locx) or (desy-self.locy)):
			self.locx = self.locx+incx
			self.locy = self.locy+incy
			print("loc x ")
			print(self.locx)
			print("loc y ")
			print(self.locy)
			root.update()
			if ((desx-self.locx)==0):
				incx=0
			if ((desy-self.locy)==0):
				incy=0
		
	def getx(self):
		return self.locx
		
	def gety(self):
		return self.locy
		
	def createloc(self):
		self.grid.drawimage(ifile=self.ifile,x=self.locx,y=self.locy)
		
	def updateloc(self):
		self.grid.updateimage(ifile=self.ifile,x=self.locx,y=self.locy)
		
	
root = Tk()
root.title("Blah!!")
ga = gridarea(root,600,600,20,20)
b1 = Button(root,text="cheese",command=root.quit)
b1.grid()
b2 = Button(root,text="left",command=ga.onleft)
b2.grid()
b3 = Button(root,text="right",command=ga.onright)
b3.grid()
root.mainloop()
