import pygame
from pygame.locals import *
Window = pygame.display.set_mode((800,800))
class Board:
	First_Pixel=None
	Last_Pixel=None
	def __init__(self,X,Y):
		self.First_Pixel=X
		self.Last_Pixel=Y

	def Create(self):
		Color_White=pygame.Color(255,255,255)
		Color_Black=pygame.Color(0,0,0)

		#Creando cuadrado Negro
		pygame.draw.rect(Window,Color_Black,(self.First_Pixel,self.First_Pixel,(self.Last_Pixel-self.First_Pixel),(self.Last_Pixel-self.First_Pixel)))
		#Creando Casillas Blancas				#200         #200         	#400                        #400
		def White_Boxes(X_Pos,Y_Pos):
			pygame.draw.rect(Window,Color_White,(X_Pos,Y_Pos,((self.Last_Pixel-self.First_Pixel)/8),((self.Last_Pixel-self.First_Pixel))/8))
																#####  50  #####           	#####  50 #####

		for Y in range (self.First_Pixel,self.Last_Pixel,int((self.Last_Pixel-self.First_Pixel)/8)): ###(200,600,50)###
			for X in range (self.First_Pixel,self.Last_Pixel,int((self.Last_Pixel-self.First_Pixel)/4)): ###(200,600,100)####
				White_Boxes(X,Y) if not(Y%100) else White_Boxes(X+50,Y)
	
	#Encerrar mini Tablero
		pygame.draw.rect(Window, Color_White, ((self.First_Pixel, self.First_Pixel), (self.First_Pixel*2, self.First_Pixel*2)), 1)
	#Coordinate
	def Render_Text(self):
		MyFont = pygame.font.SysFont("Comic Sans MS",30)
		list_text = [[[],"1"], [[],"2"], [[],"3"], [[],"4"], [[],"5"], [[],"6"], [[],"7"], [[],"8"]]
		aux = 555
		for i in range( 0, 8):
			list_text[i][0] = MyFont.render(list_text[i][1], 0 ,(255,255,255))
			Window.blit(list_text[i][0],(170,aux))
			Window.blit(list_text[i][0],(615,aux))
			aux-= 50 #aumenta de 50 en 50 iniciando desde 205 para posicionarse en el lugar de cada casilla
		MyText_Letters = MyFont.render("   A   B    C   D   E    F    G   H",0,(255,255,255))
		Window.blit(MyText_Letters,(190,155))
		Window.blit(MyText_Letters,(190,605))

class Note: #Notes de Coordinate para el ajedrez
	Range=0
	def Comun(Coordinate): # Note Comun
		Coor_X=Coordinate[0]-(Note.Range*4)
		Coor_Y=Coordinate[1]-(Note.Range*4)
		PosX=0
		PosY=0
		for number in range(1,9):
			if(Coor_X>0):
				Coor_X-=Note.Range
				PosX+=1
			if(Coor_Y>0):
				Coor_Y-=Note.Range
				PosY+=1
		Arab=[1,2,3,4,5,6,7,8]
		return chr((Arab[PosX-1]+64)),Arab[-PosY]

	def Pixel(Notecion): # Note en Pixeles
		if(ord(Notecion[0])<65 or ord(Notecion[0])>72 or Notecion[1]>8 or Notecion[1]<1):
			return None
		Coor_X=((ord(Notecion[0])-64)*Note.Range)+175
		Coor_Y=((9-Notecion[1])*Note.Range)+175
		return int(Coor_X),int(Coor_Y)
