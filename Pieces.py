import pygame
from pygame.locals import *
from Design import*

def Image(Piece,Color):
	Folder="Images"
	for index in [ "Pawn", "Knight", "Bishop", "Tower", "Queen", "King"]:
		for sub_index in ["W", "B"] :
			if(Piece == index and Color == sub_index):
				return Folder+f"/{index}_{sub_index}.png"

class Piece():
	Alive=True #Si la Ficha esta viva o en Juego
	Image=None #Image guardada de la Ficha
	Position=None #Position Actual
	Select=False #Si esta seleccionada
	Fortify=False
	Range=[] #Casillas a las que puede Moverse
	Capture=[] #Casillas en las que captura una Ficha enemiga
	Control=[] #Delimita el movimiento de una ficha para que no muera su Rey
	ColorPiece=None # Bando al que pertenece 1 Negros / -1 Blancos

	def Show(self):
		Window.blit(self.Image,(self.Position[0]-15,self.Position[1]-25))
		#Se le resta -15 a la coordenada en X y -25 en Y para que la Image encaje bien en su casilla

	def Paint(self):
		pygame.draw.rect(Window,(20,230,0),(self.Position[0]-20,self.Position[1]-20,40,40))         ### Verde Puro
		#Colorea en Verde la Casilla con la Ficha seleccionada

		def Drawing(List,Color):
			for Each in List:
				pygame.draw.rect(Window,Color,(Each[0]-20,Each[1]-20,40,40))
		Drawing(self.Range,(0,70,150)) #Colorea en azul su Range o casillas disponible para moverse ### Azul capri
		Drawing(self.Capture,(230,0,0)) #Colorea en rojo su comida o casillas disponible para matar ### Rojo Brillante

	def Hide(self):
		self.Range=[]
		self.Capture=[]
		#Elimina sus propiedades de movimiento o captura para calcular de nuevo los movimientos
		self.Position=None #Saca la ficha del mapa

class Pawn(Piece):
	Special=True #Mover 2 Pasos
	Promotion=0 #Peon llega a casilla final
	Passant=0 #Regla de Passant
	def __init__(self,Color,Coor):
		self.Image=pygame.image.load(Image("Pawn",Color))
		self.Position=Coor
		self.ColorPiece=-1 if(Color=='W') else 1
			
class Knight(Piece):
	def __init__(self,Color,Coor):
		self.Image=pygame.image.load(Image("Knight",Color))
		self.Position=Coor
		self.ColorPiece=-1 if(Color=='W') else 1

class Bishop(Piece):
	def __init__(self,Color,Coor):
		self.Image=pygame.image.load(Image("Bishop",Color))
		self.Position=Coor
		self.ColorPiece=-1 if(Color=='W') else 1

class Tower(Piece):
	Special=True #No se ha movido
	def __init__(self,Color,Coor):
		self.Image=pygame.image.load(Image("Tower",Color))
		self.Position=Coor
		self.ColorPiece=-1 if(Color=='W') else 1

class Queen(Piece):
	def __init__(self,Color,Coor):
		self.Image=pygame.image.load(Image("Queen",Color))
		self.Position=Coor
		self.ColorPiece=-1 if(Color=='W') else 1

class King(Piece):
	Special=True #No se ha movido
	Check=False #Jaque y Jaque-Mate
	def __init__(self,Color,Coor):
		self.Image=pygame.image.load(Image("King",Color))
		self.Position=Coor
		self.ColorPiece=-1 if(Color=='W') else 1
