import pygame
import sys
from pygame.locals import *
from Design import* #Iniciando la pantalla del Tablero a mostar
from Pieces import*
from Movements import*

pygame.init()
pygame.display.set_caption("Ajedrez")
Dimensions=[200,600] #Dimensiones del Tablero
Boxes=Board(Dimensions[0],Dimensions[1]) #Tamaño del Tablero
Boxes.Create() #Crear el mismo Tablero
Boxes.Render_Text() #Muestra las coordenadas del tablero
Range=int((Dimensions[1]-Dimensions[0])/8) #El Range es el area de cada Casilla
Last_Pixel=0 # Ultima coordenada, para que solo tome una nueva cada vez que salga del Range de una, asi no se ralentiza el programa
Case=True # Cuando Da click para levantar una Pieza
Note.Range=Range # Para hacer los procesos de Notaciones con la clase Note
Turn=True #True Juegan las Blancas / False Las Negras
Times=True #Para que no se quede infinitamente sacando Rangos y consuma muchos procesos
Stop=False #Detiene el Juego mientras Sucede un Evento
Movement.Range=Range

Aggressor=-1 #Posicion en lista de Pieza que intenta cazar al Rey
Reset=1 ###
EndGame=[0,0,0] #Cuando Finaliza el Juego

#Declaracion de Piezas 
for  num in range ( 1, 9):
	exec(f'Pawn{num}W = Pawn( "W" ,( Note.Pixel( ( chr( ord ( "A" ) + {num} -1 ), 2 ) ) ) ) ')
	exec(f'Pawn{num}B = Pawn( "B" ,( Note.Pixel( ( chr( ord ( "A" ) + {num} -1 ), 7 ) ) ) ) ')
	if ( num == 1):
		for pieces in [ ["Tower", "A", num ],["Knight", "B", num ], ["Bishop", "C", num],["Tower", "H", num+1],["Knight", "G", num+1], ["Bishop", "F", num+1] ]:
				exec(f'{pieces[0]}{pieces[2]}W = {pieces[0]}( "W" ,( Note.Pixel ( ( "{pieces[1]}", num ) ) ) ) ')
	if ( num == 8 ):
		for pieces in [ ["Tower", "A", num - 7 ],["Knight", "B", num -7 ], ["Bishop", "C", num - 7 ],["Tower", "H", num - 6],["Knight", "G", num - 6], ["Bishop", "F", num - 6] ]:
			exec(f'{pieces[0]}{pieces[2]}B = {pieces[0]}( "B" ,( Note.Pixel ( ( "{pieces[1]}", num ) ) ) ) ')

King_W =King("W",(Note.Pixel(("E",1))))
King_B =King("B",(Note.Pixel(("E",8))))
Queen_W =Queen("W",(Note.Pixel(("D",1))))
Queen_B =Queen("B",(Note.Pixel(("D",8))))

#Listas para trabajar con las Piezas de manera mas ordenada y rapida
List_White=[Pawn1W,Pawn2W,Pawn3W,Pawn4W,Pawn5W,Pawn6W,Pawn7W,Pawn8W,Knight1W,Knight2W,Bishop1W,Bishop2W,Tower1W,Tower2W,Queen_W,King_W]
List_Black=[Pawn1B,Pawn2B,Pawn3B,Pawn4B,Pawn5B,Pawn6B,Pawn7B,Pawn8B,Knight1B,Knight2B,Bishop1B,Bishop2B,Tower1B,Tower2B,Queen_B,King_B]

#Sonidos y Textos
Selection=pygame.mixer.Sound("Images/Select.wav")
Move=pygame.mixer.Sound("Images/Move.wav")
Eat=pygame.mixer.Sound("Images/Eat.wav")
Initial=pygame.mixer.Sound("Images/Victory.wav")
#Initial.play()

def Calculate_Moves(List):
	global List_White,List_Black
	for Piece in List:
		Piece.Fortify=False #Reseteo el Fortificado de las Piezas
	for num in range(0,16):
		if(List[num].Alive==True):
			#Range, Capture, Promotion
			List[num].Range=[] #Vaciado de Ranges
			List[num].Capture=[] #Vaciado de Capture
			if(num<8 and List[num].Promotion==0):#Pawnes
				Movement.Reload(List_White,List_Black,Aggressor)
				List_White,List_Black=Movement.Pawn(List[num])

			if((num>=8 and num<10) or (num<8 and List[num].Promotion==1)): #Knights
				if(num<8):
					if(List[num].ColorPiece==-1):
						List[num].Image=pygame.image.load(Image("Knight","W"))
					elif(List[num].ColorPiece==1):
						List[num].Image=pygame.image.load(Image("Knight","B"))
				Movement.Reload(List_White,List_Black,Aggressor)
				List_White,List_Black=Movement.Knight(List[num])

			if((num>=10 and num<12) or (num<8 and List[num].Promotion==2)): #Bishops
				if(num<8 and List_White[num].Promotion==2):
					if(List[num].ColorPiece==-1):
						List_White[num].Image=pygame.image.load(Image("Bishop","W"))
					elif(List[num].ColorPiece==1):
						List_White[num].Image=pygame.image.load(Image("Bishop","B"))
				Movement.Reload(List_White,List_Black,Aggressor)
				List_White,List_Black=Movement.Bishop(List[num])
	
			if((num>=12 and num<14) or (num<8 and List[num].Promotion==3)): #Towers
				if(num<8 and List[num].Promotion==3):
					if(List[num].ColorPiece==-1):
						List[num].Image=pygame.image.load(Image("Tower","W"))
					elif(List[num].ColorPiece==1):
						List[num].Image=pygame.image.load(Image("Tower","B"))
				Movement.Reload(List_White,List_Black,Aggressor)
				List_White,List_Black=Movement.Tower(List[num])

			if((num==14) or (num<8 and List[num].Promotion==4)): #Queen
				if(num<8 and List[num].Promotion==4):
					if(List[num].ColorPiece==-1):
						List[num].Image=pygame.image.load(Image("Queen","W"))
					elif(List[num].ColorPiece==1):
						List[num].Image=pygame.image.load(Image("Queen","B"))
				Movement.Reload(List_White,List_Black,Aggressor)
				List_White,List_Black=Movement.Queen(List[num])

			if(num==15): #King
				Movement.Reload(List_White,List_Black,Aggressor)
				List_White,List_Black=Movement.King(List[num])

def Print_winner(color1, color2, team_win):
	MyFont = pygame.font.SysFont("Comic Sans MS",30)
	MyText_EndGame = MyFont.render("End Game",0,color1)
	MyText_Play = MyFont.render("Jugar de Nuevo",0,color1)
	MyText_Exit = MyFont.render("Salir",0,color1)
	MyText_Win = MyFont.render("Ganaron las " + team_win ,0,color2)
	for Text in [[MyText_EndGame,(300,300)], [MyText_Play,(120,450)], [MyText_Exit,(520,450)], [MyText_Win,(235,375)]]:
		Window.blit(Text[0],Text[1])

Clock = pygame.time.Clock()
while True:
	def Show_Alive(List):
		for Piece in List:
			Piece.Show() if(Piece.Alive) else Piece.Hide()	

	Show_Alive(List_White)
	Show_Alive(List_Black)

	if(Times==True): #Recarga de Movimientos
		Calculate_Moves(List_White)
		Calculate_Moves(List_Black)
		Calculate_Moves(List_White)

		Alternatives=0 #Si no puedes hacer ninguna jugada entonces estas jaque-mate
		King_IsCheck=[False,False]

		for num in range(0,16): #Verificar Jaques
			if(King_W.Position in List_Black[num].Capture):
				Aggressor=num
				King_IsCheck[0]=True
				King_W.Check=True
				Calculate_Moves(List_Black)
				Calculate_Moves(List_White)
			if(King_B.Position in List_White[num].Capture):
				Aggressor=num
				King_IsCheck[1]=True
				King_B.Check=True
				Calculate_Moves(List_White)
				Calculate_Moves(List_Black)

		if not (King_IsCheck[0]):
			King_W.Check=False

		if not (King_IsCheck[1]):
			King_B.Check=False

		for num in range(0,16):
			if(Turn):
				if(List_White[num].Range!=[] or List_White[num].Capture!=[]):
					Alternatives=1
			else:
				if(List_Black[num].Range!=[] or List_Black[num].Capture!=[]):
					Alternatives=1

		if not (Alternatives):
			if(Turn):
				EndGame[0]=1
				if not(King_W.Check):
					EndGame[2]=1
			else:
				EndGame[1]=1
				if not(King_B.Check):
					EndGame[2]=1
		Times=False

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if(EndGame[0]!=0 or EndGame[1]!=0):
			#Final del juego
			pygame.draw.rect(Window,(0,100,140),(100,300,600,200))
			Case=True # Cuando Da click para levantar una Pieza
			Turn=True #True Juegan las Blancas / False Las Negras
			Aggressor=-1 #Position en lista de Pieza que intenta cazar al King
			Stop=True
			Movement.Intermediate=[(0,0)]

			for num in range(0,16): #Reacomodar Piezas a posiciones originales
				List_White[num].Alive=True
				List_Black[num].Alive=True
				if(num<8 or num==15 or num==12 or num==13):
					List_White[num].Special=True
					List_Black[num].Special=True
					if(num<8):
						List_White[num].Position=(Note.Pixel((chr(ord("A")+num),2)))
						List_Black[num].Position=(Note.Pixel((chr(ord("A")+num),7)))

				#Reseteo de las posiciones iniciales
				list_pieces = [[Tower1W, "A", 1], [Tower2W, "H", 1], [Tower1B, "A", 8], [Tower2B, "H", 8], [King_W, "E", 1], [King_B, "E", 8], [Queen_W, "D", 1], [Queen_B, "D", 8], [Knight1W, "B", 1], [Knight2W, "G", 1], [Knight1B, "B", 8], [Knight2B, "G", 8], [Bishop1W, "C", 1], [Bishop2W, "F", 1], [Bishop1B, "C", 8], [Bishop2B, "F", 8]]
				for Piece in list_pieces:
					Piece[0].Position=(Note.Pixel( ( Piece[1], Piece[2] ) ) )

				if(Reset):
					Boxes.Create()
					Reset=0

			if(EndGame[2]!=0):
				#Tablas
				Print_winner ( (130,130,130) , (76,47,39), "Tablas" )

			elif(EndGame[1]==1):#Ganaron las Blancas
				Print_winner ( (0,0,0), (240,240,240), "Blancas" )

			elif(EndGame[0]==1):#Ganaron las Negras
				Print_winner ( (240,240,240), (0,0,0), "Negras" )
			
		if(Stop!=False and EndGame!=[0,0,0]):

			if event.type == pygame.MOUSEBUTTONUP: #Eleccion de Final del Juego
				if(pygame.mouse.get_pos()[0]<365 and pygame.mouse.get_pos()[0]>110 and pygame.mouse.get_pos()[1]<485 and pygame.mouse.get_pos()[1]>445):
					#Nuevo Juego
					King_W.Check=False
					King_B.Check=False
					Window.fill((0,0,0))
					Boxes.Create()
					Initial.play()
					EndGame=[0,0,0]
					Stop=False
					Calculate_Moves(List_White)
					Calculate_Moves(List_Black)
					Boxes.Render_Text()
					Reset=1

				if(pygame.mouse.get_pos()[0]<600 and pygame.mouse.get_pos()[0]>505 and pygame.mouse.get_pos()[1]<485 and pygame.mouse.get_pos()[1]>445):
					#Salida del Programa
					pygame.quit()
					sys.exit()

		for Piece in range(0,8): #Promocion de Peones
			if(List_Black[Piece].Promotion==5 or List_White[Piece].Promotion==5): #Si el Peon esta esperando Ascenso
				Stop=True #Para evitar que las Piezas sigan jugando hasta que se decida la Promocion
				Elections=[("Knight","W"),("Bishop","W"),("Tower","W"),("Queen","W"),("Knight","B"),("Bishop","B"),("Tower","B"),("Queen","B")]

				if(List_White[Piece].Promotion!=0):

					def Promotion_W():
						global Stop
						global Aggressor
						Stop=False
						Calculate_Moves(List_White)
						Boxes.Create()
						for num in range(0,16):
							if(King_B.Position in List_White[num].Capture): #Si el peon promocionado causa Jaque
								Aggressor=num
								King_B.Check=True
								Calculate_Moves(List_Black)
						pygame.draw.rect(Window,(0,0,0),(Dimensions[0]-(Range*2),Dimensions[0],Range,Range*4)) #Parche para tapar hueco
					
					#Dibujo de Tabla para Promocion
					pygame.draw.rect(Window,(143,143,143),(100,200,50,200))
					for Pieces in Elections[:4]:
						Window.blit(pygame.image.load(Image(Pieces[0],Pieces[1])),(110,200+(Range*Elections.index(Pieces))))

					if event.type == pygame.MOUSEBUTTONUP: #Eleccion de Ascenso
						if(pygame.mouse.get_pos()[0]<Dimensions[0]-Range and pygame.mouse.get_pos()[0]>Dimensions[0]-(Range*2)
							and pygame.mouse.get_pos()[1]<Dimensions[0]+Range and pygame.mouse.get_pos()[1]>Dimensions[0]):
							#Knight Promocion
							List_White[Piece].Promotion=1
							Promotion_W()
						elif(pygame.mouse.get_pos()[0]<Dimensions[0]-Range and pygame.mouse.get_pos()[0]>Dimensions[0]-(Range*2)
							and pygame.mouse.get_pos()[1]<Dimensions[0]+(Range*2) and pygame.mouse.get_pos()[1]>Dimensions[0]+Range):
							#Bishop Promocion
							List_White[Piece].Promotion=2
							Promotion_W()
						elif(pygame.mouse.get_pos()[0]<Dimensions[0]-Range and pygame.mouse.get_pos()[0]>Dimensions[0]-(Range*2)
							and pygame.mouse.get_pos()[1]<Dimensions[0]+(Range*3) and pygame.mouse.get_pos()[1]>Dimensions[0]+(Range*2)):
							#Tower Promocion
							List_White[Piece].Promotion=3
							Promotion_W()
						elif(pygame.mouse.get_pos()[0]<Dimensions[0]-Range and pygame.mouse.get_pos()[0]>Dimensions[0]-(Range*2)
							and pygame.mouse.get_pos()[1]<Dimensions[0]+(Range*4) and pygame.mouse.get_pos()[1]>Dimensions[0]+(Range*3)):
							#Queen Promocion
							List_White[Piece].Promotion=4
							Promotion_W()

				if(List_Black[Piece].Promotion!=0):

					def Promotion_B():
						global Stop
						global Aggressor
						Stop=False
						Calculate_Moves(List_Black)
						Boxes.Create()
						for num in range(0,16):
							if(King_W.Position in List_Black[num].Capture): #Si el peon promocionado causa Jaque
								Aggressor=num
								King_W.Check=True
								Calculate_Moves(List_White)
						pygame.draw.rect(Window,(0,0,0),(Dimensions[1]+Range,Dimensions[1]-Dimensions[0],Range,Range*4)) #Parche para tapar hueco

					#Dibujo de Tabla para Promocion
					pygame.draw.rect(Window,(215,215,215),(650,400,50,200))
					for Pieces in Elections[4:]:
						Window.blit(pygame.image.load(Image(Pieces[0],Pieces[1])),(660,550-(Range*(Elections.index(Pieces)-4))))	

					if event.type == pygame.MOUSEBUTTONUP: #Eleccion de Ascenso
						if(pygame.mouse.get_pos()[0]<Dimensions[1]+(Range*2) and pygame.mouse.get_pos()[0]>Dimensions[1]+Range
							and pygame.mouse.get_pos()[1]<Dimensions[1]-Dimensions[0]+(Range*4) and pygame.mouse.get_pos()[1]>Dimensions[1]-Dimensions[0]+(Range*3)):
							#Knight Promocion
							List_Black[Piece].Promotion=1
							Promotion_B()
						elif(pygame.mouse.get_pos()[0]<Dimensions[1]+(Range*2) and pygame.mouse.get_pos()[0]>Dimensions[1]+Range
							and pygame.mouse.get_pos()[1]<Dimensions[1]-Dimensions[0]+(Range*3) and pygame.mouse.get_pos()[1]>Dimensions[1]-Dimensions[0]+(Range*2)):
							#Bishop Promocion
							List_Black[Piece].Promotion=2
							Promotion_B()
						elif(pygame.mouse.get_pos()[0]<Dimensions[1]+(Range*2) and pygame.mouse.get_pos()[0]>Dimensions[1]+Range
							and pygame.mouse.get_pos()[1]<Dimensions[1]-Dimensions[0]+(Range*2) and pygame.mouse.get_pos()[1]>Dimensions[1]-Dimensions[0]+Range):
							#Tower Promocion
							List_Black[Piece].Promotion=3
							Promotion_B()
						elif(pygame.mouse.get_pos()[0]<Dimensions[1]+(Range*2) and pygame.mouse.get_pos()[0]>Dimensions[1]+Range
							and pygame.mouse.get_pos()[1]<Dimensions[1]-Dimensions[0]+Range and pygame.mouse.get_pos()[1]>Dimensions[1]-Dimensions[0]):
							#Queen Promocion
							List_Black[Piece].Promotion=4
							Promotion_B()							

		if(pygame.mouse.get_pos()[0]<600 and pygame.mouse.get_pos()[0]>200
		and pygame.mouse.get_pos()[1]<600 and pygame.mouse.get_pos()[1]>200 and Stop==False): #Si esta dentro de los limites del tablero y el juego no esta detenido

			if(Note.Comun(pygame.mouse.get_pos())!=Last_Pixel): #Si es la primera vez que se posa en esa Casilla
				#print(Note.Comun(pygame.mouse.get_pos()))
				Last_Pixel=Note.Comun(pygame.mouse.get_pos())
				Last_Coor=Note.Pixel(Last_Pixel)
				#print(Last_Coor)
			if event.type == pygame.MOUSEBUTTONUP: #Clicks en el juego
				if(Case==True): #Funcion A
					for Piece in range(0,16):

						if(Last_Coor==List_White[Piece].Position and Turn==True): #####
							Selection.play()
							List_White[Piece].Select=True ##### Selecciona la Pieza que se puede mover
							List_White[Piece].Paint() ##### Colores para indicar donde dar click el usuario
							Case=False

						if(Last_Coor==List_Black[Piece].Position and Turn==False):
							Selection.play()
							List_Black[Piece].Select=True ###Selecciona la Pieza que se puede mover
							List_Black[Piece].Paint() ### Colores para indicar donde dar click el usuario
							Case=False

				else: #Funcion B
					def Finish(Pos):
						global Turn
						global Times
						global Case

						if(Pos.ColorPiece==-1):	
							Turn=False
						else:
							Turn=True

						Times=True		
						Pos.Special=False
						Pos.Select=False
						Boxes.Create()
						Case=True						

					def Action(Pos):
						global Case
						Movement.Band=Pos.ColorPiece

						if(Last_Coor==Pos.Position): #Si dio click a la misma Pieza que habia seleccionado
								Pos.Select=False
								Boxes.Create()
								Case=True

						if(Last_Coor in Pos.Range): #Si la Coordenada esta en un Movimiento de Rango
							Move.play()
							if(len(Pos.Range)==2 and ((Pos in List_White[0:8]) or (Pos in List_Black[0:8]))): #Si es un Peon no promocionado y en el Rango de movimiento tiene 2 casillas para moverse
								if(Pos.Promotion==0):
									if(Last_Coor==Pos.Range[1]): #Si dio 2 Pasos

											#Alguien esta a tu derecha o a tu izquierda?
										if(Movement.BoxIsTaken((Last_Coor[0]+Range,Last_Coor[1]))==2 or
											Movement.BoxIsTaken((Last_Coor[0]-Range,Last_Coor[1]))==2):
											for Pawn in range(0,8):
												if(Pos.ColorPiece==-1):
													if(List_Black[Pawn].Position==(Last_Coor[0]+Range,Last_Coor[1])):
														#Si hay un Peon enemigo a la derecha, dale Passant
														List_Black[Pawn].Passant=Last_Coor

													if(List_Black[Pawn].Position==(Last_Coor[0]-Range,Last_Coor[1])):
														#Si hay un Peon enemigo a la izquierda, dale Passant
														List_Black[Pawn].Passant=Last_Coor
												else:
													if(List_White[Pawn].Position==(Last_Coor[0]+Range,Last_Coor[1])):
														#Si hay un Peon enemigo a la derecha, dale Passant
														List_White[Pawn].Passant=Last_Coor

													if(List_White[Pawn].Position==(Last_Coor[0]-Range,Last_Coor[1])):
														#Si hay un Peon enemigo a la izquierda, dale Passant
														List_White[Pawn].Passant=Last_Coor												

							if(Piece==15):
								if(Pos.ColorPiece==-1):
									if(Last_Coor[0]==King_W.Position[0]+(Range*2)): #Enroque Derecho
										Tower2W.Position=(King_W.Position[0]+(Range),Last_Coor[1])
									if(Last_Coor[0]==King_W.Position[0]-(Range*2)): #Enroque Izquierdo
										Tower1W.Position=(King_W.Position[0]-(Range),Last_Coor[1])
								else:
									if(Last_Coor[0]==King_B.Position[0]+(Range*2)): #Enroque Derecho
										Tower2B.Position=(King_B.Position[0]+(Range),Last_Coor[1])
									if(Last_Coor[0]==King_B.Position[0]-(Range*2)): #Enroque Izquierdo
										Tower1B.Position=(King_B.Position[0]-(Range),Last_Coor[1])								

							Pos.Position=Last_Coor #Desplaza la Pieza a esa coordenada
							Pos.Passant=0 #Si pasa el turno ya no puede hacer la jugada de Paso

							if(Pos.ColorPiece==-1 and Note.Comun(Last_Coor)[1]==8 and Pos in List_White[0:8]) or (Pos.ColorPiece==1 and Note.Comun(Last_Coor)[1]==1 and Pos in List_Black[0:8]): 
							#Si esta en la Ultima Casilla y es un Peon, Promocionalo
								if(Pos.Promotion==0):
									Pos.Promotion=5
							Finish(Pos)												

						if(Last_Coor in Pos.Capture):  #Si la Coordenada esta en un Movimiento de Captura
							Eat.play()
							for num in range(0,16):

								if(List_Black[num].Position==Last_Coor): #Busca la Pieza que tiene su posicion en esa coordenada
									List_Black[num].Alive=False #La Pieza muere
								if(List_White[num].Position==Last_Coor):
									List_White[num].Alive=False

								if not(Movement.BoxIsTaken(Last_Coor)): #Si no hay ninguna Pieza en la Coordenada es porque es una Jugada de Paso
									if(List_Black[num].Position==(Last_Coor[0],Last_Coor[1]+Range) and Pos.ColorPiece==-1):
										List_Black[num].Alive=False
									if(List_White[num].Position==(Last_Coor[0],Last_Coor[1]-Range) and Pos.ColorPiece==1):
										List_White[num].Alive=False

							Pos.Passant=0 #Si pasa el turno ya no puede hacer la jugada de Paso
							Pos.Position=Last_Coor #Desplaza la Pieza a esa coordenada
								
							if(Pos.ColorPiece==-1 and Note.Comun(Last_Coor)[1]==8 and Pos in List_White[0:8]) or (Pos.ColorPiece==1 and Note.Comun(Last_Coor)[1]==1 and Pos in List_Black[0:8]): 
							#Si esta en la Ultima Casilla y es un Peon, Promocionalo
								if(Pos.Promotion==0):
									Pos.Promotion=5
							Finish(Pos)

					for Piece in range(0,16):
						if(List_White[Piece].Select==True):
							Action(List_White[Piece])
						if(List_Black[Piece].Select==True):
							Action(List_Black[Piece])		

	Clock.tick(200) #FPS
	pygame.display.update()
	