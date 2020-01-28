class Movement():
	List_White=[]
	List_Black=[]
	Aggressor=-1 #Posicion en lista de ficha que intenta cazar al Rey
	Intermediate=[(0,0)] #Posiciones entre la ficha Agresor y el Rey
	Range=0
	Band=0

	def Reload(List_W,List_B,Agre):
		Movement.List_White=List_W
		Movement.List_Black=List_B
		Movement.Aggressor=Agre

	def BoxIsTaken(Boxes):# Saber si una Boxes esta llena
		#(x,y)
		BoxIsBusy=0
		if not(Boxes[0]<600 and Boxes[0]>200
			and Boxes[1]<600 and Boxes[1]>200):#Si se sale de los limites
			BoxIsBusy=3
		else:
			for Buscar in range(0,16):
				if(Movement.Band==1):# Si es Negra
					if(Movement.List_Black[Buscar].Position==Boxes): #SI hay una Boxes Aliada
						BoxIsBusy=1				
					if(Movement.List_White[Buscar].Position==Boxes): #SI hay una Boxes Enemiga
						BoxIsBusy=2
				else: #Si es Blanca
					if(Movement.List_White[Buscar].Position==Boxes): #SI hay una Boxes Aliada
						BoxIsBusy=1
					if(Movement.List_Black[Buscar].Position==Boxes): #SI hay una Boxes Negra
						BoxIsBusy=2				

			return BoxIsBusy

	def Pawn(Pos):
		Range=Movement.Range*Pos.ColorPiece # Para Que los ranges sean indefinidos
		Movement.Band=Pos.ColorPiece #Para el BoxIsTaken
		
		Two=((Pos.Special==True) and Movement.BoxIsTaken((Pos.Position[0],Pos.Position[1]+(Range*2)))==0)

			#Pasos
		if (Movement.BoxIsTaken((Pos.Position[0],Pos.Position[1]+Range))==0): #Si la casilla esta vacia

			if((Movement.List_White[15].Check==False and Pos.ColorPiece==-1) or (Movement.List_Black[15].Check==False and Pos.ColorPiece==1)): #Si no hay Jaque, muevete con normalidad
				if(Pos.Control==[]):
					Pos.Range.append((Pos.Position[0],Pos.Position[1]+Range))
					if(Two):
						Pos.Range.append((Pos.Position[0],Pos.Position[1]+(Range*2)))
				else: #Si el rey esta detras, no te apartes
					if((Pos.Position[0],Pos.Position[1]+Range) in Pos.Control):
						Pos.Range.append((Pos.Position[0],Pos.Position[1]+Range))
					if(Two and ((Pos.Position[0],Pos.Position[1]+(Range*2)) in Pos.Control)):
						Pos.Range.append((Pos.Position[0],Pos.Position[1]+(Range*2)))

			else:#Si hay jaque, solo puedes moverte en el intermedio

				if(Pos.ColorPiece==1): # Si es Negra
					if(((Pos.Position[0],Pos.Position[1]+Range) in Movement.Intermediate[-1])):
						if((Movement.Aggressor>=10 and Movement.Aggressor<15) or (Movement.Aggressor<8 and Movement.List_White[Movement.Aggressor].Promotion!=0)):
							Pos.Range.append((Pos.Position[0],Pos.Position[1]+Range))

					if(((Pos.Position[0],Pos.Position[1]+(Range*2)) in Movement.Intermediate[-1]) and Two):
						if((Movement.Aggressor>=10 and Movement.Aggressor<15) or (Movement.Aggressor<8 and Movement.List_White[Movement.Aggressor].Promotion!=0)):
							Pos.Range.append((Pos.Position[0],Pos.Position[1]+(Range*2)))

				else: # Si es Blanca
					if(((Pos.Position[0],Pos.Position[1]+Range) in Movement.Intermediate[-1])):
						if((Movement.Aggressor>=10 and Movement.Aggressor<15) or (Movement.Aggressor<8 and Movement.List_Black[Movement.Aggressor].Promotion!=0)):
							Pos.Range.append((Pos.Position[0],Pos.Position[1]+Range))

					if(((Pos.Position[0],Pos.Position[1]+(Range*2)) in Movement.Intermediate[-1]) and Two):
						if((Movement.Aggressor>=10 and Movement.Aggressor<15) or (Movement.Aggressor<8 and Movement.List_Black[Movement.Aggressor].Promotion!=0)):
							Pos.Range.append((Pos.Position[0],Pos.Position[1]+(Range*2)))

			#Capturas
		def Var (Alt):
			if(Movement.BoxIsTaken(Alt)==2):
				if((Movement.List_White[15].Check==False and Pos.ColorPiece==-1) or (Movement.List_Black[15].Check==False and Pos.ColorPiece==1)):#Si no hay jaque, captura con normalidad
					if(Pos.Control==[]):
						Pos.Capture.append(Alt)
					else: #Si el rey esta detras, no te apartes
						if(Alt in Pos.Control):
							Pos.Capture.append(Alt)
				else:#Si hay jaque, solo puedes capturar la ficha que hace jaque
					if(Pos.ColorPiece==1): #Si es Negra
						if(Alt == Movement.List_White[Movement.Aggressor].Position):
							Pos.Capture.append(Alt)
					else:	#Si es Blanca
						if(Alt == Movement.List_Black[Movement.Aggressor].Position):
							Pos.Capture.append(Alt)					

		Var((Pos.Position[0]+Range,Pos.Position[1]+Range))
		Var((Pos.Position[0]-Range,Pos.Position[1]+Range))

			#Fortificar
		for Ficha in range(0,16):
			if(Pos.ColorPiece==1): #Si es Negra
				if(Movement.List_Black[Ficha].Position==(Pos.Position[0]+Range,Pos.Position[1]+Range)):
					Movement.List_Black[Ficha].Fortify=True
				if(Movement.List_Black[Ficha].Position==(Pos.Position[0]-Range,Pos.Position[1]+Range)):
					Movement.List_Black[Ficha].Fortify=True						
			else: #Si es Blanca
				if(Movement.List_White[Ficha].Position==(Pos.Position[0]+Range,Pos.Position[1]+Range)):
					Movement.List_White[Ficha].Fortify=True
				if(Movement.List_White[Ficha].Position==(Pos.Position[0]-Range,Pos.Position[1]+Range)):
					Movement.List_White[Ficha].Fortify=True				

			#Passant
		if(Pos.Passant!=0):
			if(Pos.Control==[]):
				Pos.Capture.append((Pos.Passant[0],Pos.Passant[1]+Range))
			else:
				if((Pos.Passant[0],Pos.Passant[1]+Range) in Pos.Control):
					Pos.Capture.append((Pos.Passant[0],Pos.Passant[1]+Range))

		Pos.Control=[]
		return Movement.List_White,Movement.List_Black

	def Knight(Pos):
		Range=Movement.Range
		Movement.Band=Pos.ColorPiece #Para el BoxIsTaken
		
		def Var (Alt):
			if(Movement.BoxIsTaken(Alt)==0): #Range
				if((Movement.List_White[15].Check==False and Pos.ColorPiece==-1) or (Movement.List_Black[15].Check==False and Pos.ColorPiece==1)):#Si no hay Jaque, muevete con normalidad
					if(Pos.Control==[]):
						Pos.Range.append(Alt)
					else: #Si el rey esta detras, no te apartes
						if(Alt in Pos.Control):
							Pos.Range.append(Alt)
				else:#Si hay jaque, solo puedes moverte en el intermedio
					if((Alt in Movement.Intermediate[-1])):
						if(Pos.ColorPiece==1): # Si es Negra
							if((Movement.Aggressor>=10 and Movement.Aggressor<15) or (Movement.Aggressor<8 and Movement.List_White[Movement.Aggressor].Promotion!=0)):
								Pos.Range.append(Alt)
						else: # Si es Blanca
							if((Movement.Aggressor>=10 and Movement.Aggressor<15) or (Movement.Aggressor<8 and Movement.List_Black[Movement.Aggressor].Promotion!=0)):
								Pos.Range.append(Alt)

			if(Movement.BoxIsTaken(Alt)==1): #Fortificar
				for Ficha in range(0,16):
					if(Pos.ColorPiece==1): #Es Negra
						if(Alt==Movement.List_Black[Ficha].Position):
							Movement.List_Black[Ficha].Fortify=True
					else:
						if(Alt==Movement.List_White[Ficha].Position):
							Movement.List_White[Ficha].Fortify=True						

			if(Movement.BoxIsTaken(Alt)==2): #Capturas
				if((Movement.List_White[15].Check==False and Pos.ColorPiece==-1) or (Movement.List_Black[15].Check==False and Pos.ColorPiece==1)):#Si no hay jaque, captura con normalidad
					if(Pos.Control==[]):
						Pos.Capture.append(Alt)
					else: #Si el rey esta detras, no te apartes
						if(Alt in Pos.Control):
							Pos.Capture.append(Alt)
				else:#Si hay jaque, solo puedes capturar la ficha que hace jaque
					if(Pos.ColorPiece==1): #Si es Negra
						if(Alt == Movement.List_White[Movement.Aggressor].Position):
							Pos.Capture.append(Alt)
					else:			#Si es Blanca
						if(Alt == Movement.List_Black[Movement.Aggressor].Position):
							Pos.Capture.append(Alt)

		#Movimientos

		#Inferior Derecha
		Var((Pos.Position[0]+Range,Pos.Position[1]+(Range*2)))
		#Superior Izquierda
		Var((Pos.Position[0]-Range,Pos.Position[1]-(Range*2)))
		#Superior Derecha
		Var((Pos.Position[0]+Range,Pos.Position[1]-(Range*2)))
		#Inferior Izquierda
		Var((Pos.Position[0]-Range,Pos.Position[1]+(Range*2)))
		#Derecha Abajo
		Var((Pos.Position[0]+(Range*2),Pos.Position[1]+Range))
		#Izquierda Arriba
		Var((Pos.Position[0]-(Range*2),Pos.Position[1]-Range))
		#Derecha Arriba
		Var((Pos.Position[0]+(Range*2),Pos.Position[1]-Range))
		#Izquierda Abajo
		Var((Pos.Position[0]-(Range*2),Pos.Position[1]+Range))

		Pos.Control=[]
		return Movement.List_White,Movement.List_Black

	def MoveAs_Asterisk(Pos,Direction): #Pasos para el Alfil, Torre y Combinacion de Reina
		Range=Movement.Range
		Movement.Band=Pos.ColorPiece #Para el BoxIsTaken

		for Mov in Direction: # Recorre los movimientos posibles
			Void=[True,True]
			Look=None
			Deposito=[]
			for Boxes in range(1,8): #Nunca recorrera mas de 8 casillas y trabaja los movimientos
				Alt=(Pos.Position[0]+((Mov[0]*Boxes)*Range),Pos.Position[1]+((Mov[1]*Boxes)*Range))

					#Control
				if(Void[0]==False and Void[1]==True): #Luego de encontrar una ficha, si es el rey, que se quite de los posibles rangos, y si es una ficha
				# y detras esta el rey, que no se quite para dejar expuesto al rey

					if(Movement.BoxIsTaken(Alt)==0): # Si la casilla detras de la ficha a comer esta vacia
						Deposito.append(Alt)
					else: # Si encontro al rey, este no se podra mover en los posibles rangos de la ficha
						if( (Look==Movement.List_White[15].Position and Pos.ColorPiece==1) or (Look==Movement.List_Black[15].Position and Pos.ColorPiece==-1) ):
							if(Pos.ColorPiece==1):
								Movement.List_White[15].Control=Deposito
							else:
								Movement.List_Black[15].Control=Deposito

						if( (Alt==Movement.List_White[15].Position and Pos.ColorPiece==1) or (Alt==Movement.List_Black[15].Position and Pos.ColorPiece==-1) ):
							if(Pos.ColorPiece==1):
								for e in range(0,16):
									if(Movement.List_White[e].Position==Look):
										Deposito.append(Pos.Position) # Se reparo error de no poder comer la ficha que queria matar al rey
										Movement.List_White[e].Control=Deposito
							else:
								for e in range(0,16):
									if(Movement.List_Black[e].Position==Look):
										Deposito.append(Alt)
										Movement.List_Black[e].Control=Deposito
						Void[1]=False	

					#Range						
				if(Movement.BoxIsTaken(Alt)==0 and Void[0]==True): 
					if((Movement.List_White[15].Check==False and Pos.ColorPiece==-1) or (Movement.List_Black[15].Check==False and Pos.ColorPiece==1)): #Si no hay Jaque, muevete con normalidad
						if(Pos.Control==[]):
								Pos.Range.append(Alt)
						else:#Si el rey esta detras, no te apartes
							if(Alt in Pos.Control):
								Pos.Range.append(Alt)
						Deposito.append(Alt)
					else: #Si hay Jaque, solo muevete en espacios que puedan interrumpirlo
						if(Alt in Movement.Intermediate[-1]):
							if(Pos.ColorPiece==1):
								if((Movement.Aggressor>=10 and Movement.Aggressor<15) or (Aggressor<8 and Movement.List_Black[Movement.Aggressor].Promotion!=0)):
									Pos.Range.append(Alt)	
							else:
								if((Movement.Aggressor>=10 and Movement.Aggressor<15) or (Aggressor<8 and Movement.List_White[Movement.Aggressor].Promotion!=0)):
									Pos.Range.append(Alt)

				else:#Si ya no hay espacios para Moverse

						#Capture
					if(Movement.BoxIsTaken(Alt)==2 and Void[0]==True): 
						Look=Alt #Va a guardar la Position de la Ficha que puede Capture
						if((Movement.List_White[15].Check==False and Pos.ColorPiece==-1) or (Movement.List_Black[15].Check==False and Pos.ColorPiece==1)): #Si no hay Jaque,Capture con normalidad
							if((Alt==Movement.List_White[15].Position and Pos.ColorPiece==1) or (Alt==Movement.List_Black[15].Position and Pos.ColorPiece==-1)): #Si encontro al King,Guarda tu Range entre el y tu
								Movement.Intermediate.append(Deposito)
							if(Pos.Control==[]):
								Pos.Capture.append(Alt)
							else:
								if(Alt in Pos.Control):
									Pos.Capture.append(Alt)
						else: #Si hay Jaque, solo puedes Capture la ficha que pone en Jaque tu King
							if(Pos.ColorPiece==1): #Si es Negra
								if(Alt==Movement.List_White[Movement.Aggressor].Position):
									Pos.Capture.append(Alt)
							else:			#Si es Blanca
								if(Alt==Movement.List_Black[Movement.Aggressor].Position):
									Pos.Capture.append(Alt)

					if(Movement.BoxIsTaken(Alt)==1 and Void[0]==True): #Fortificar
						for Ficha in range(0,16):
							if(Pos.ColorPiece==1): #Es Negra
								if(Alt==Movement.List_Black[Ficha].Position):
									Movement.List_Black[Ficha].Fortify=True
							else:
								if(Alt==Movement.List_White[Ficha].Position):
									Movement.List_White[Ficha].Fortify=True
					Void[0]=False
		Pos.Control=[]			

	def Bishop(Pos):
		Direction=[(1,1),(-1,-1),(-1,1),(1,-1)] 
		#Inferior Derecha , Superior Izquierda , Inferior Izquierda , Superior Derecha
		Movement.MoveAs_Asterisk(Pos,Direction)
		return Movement.List_White,Movement.List_Black

	def Tower(Pos):
		Direction=[(1,0),(-1,0),(0,1),(0,-1)]
		#Derecha , Izquierda, Abajo , Arriba
		Movement.MoveAs_Asterisk(Pos,Direction)
		return Movement.List_White,Movement.List_Black

	def Queen(Pos):	
		Direction=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
		#Alfil y Torre
		Movement.MoveAs_Asterisk(Pos,Direction)
		return Movement.List_White,Movement.List_Black

	def King(Pos):
		Range=Movement.Range
		Movement.Band=Pos.ColorPiece #Para el BoxIsTaken

		def Verify(Alt):
			for e in range(0,16):
				if((Movement.List_Black[e].Alive==True and Pos.ColorPiece==-1) or (Movement.List_White[e].Alive and Pos.ColorPiece==1)):
					if(e<8): #Pawnes
						if((Movement.List_Black[e].Promotion==0 and Pos.ColorPiece==-1) or (Movement.List_White[e].Promotion==0 and Pos.ColorPiece==1)): #Si un Pawn puede Capturese al King , no mover a esa Boxes
							if(Pos.ColorPiece==1):#Si es negra
								if((Movement.List_White[e].Position[0]+Range,Movement.List_White[e].Position[1]+(Range*Movement.List_White[e].ColorPiece))==Alt or (Movement.List_White[e].Position[0]-Range,Movement.List_White[e].Position[1]+(Range*Movement.List_White[e].ColorPiece))==Alt):
									return True								
							else: #Si es blanca
								if((Movement.List_Black[e].Position[0]+Range,Movement.List_Black[e].Position[1]+(Range*Movement.List_Black[e].ColorPiece))==Alt or (Movement.List_Black[e].Position[0]-Range,Movement.List_Black[e].Position[1]+(Range*Movement.List_Black[e].ColorPiece))==Alt):
									return True

					if(Alt in Movement.List_Black[e].Range and Pos.ColorPiece==-1) or (Alt in Movement.List_White[e].Range and Pos.ColorPiece==1):#No Pawnes
						if(e>=8):
							return True
						else:
							if(Movement.List_Black[e].Promotion!=0 and Pos.ColorPiece==-1) or (Movement.List_White[e].Promotion!=0 and Pos.ColorPiece==1): #Pawnes Promotionados
								return True
					if(e==15):#No Acercarse a otro King
						if(Pos.ColorPiece==1): # Si es Negra
							if((Pos.Position[0]+Range-Movement.List_White[15].Position[0]<=Range and Pos.Position[0]+Range-Movement.List_White[15].Position[0]>=-Range) and (Pos.Position[1]+Range-Movement.List_White[15].Position[1]<=Range and Pos.Position[1]+Range-Movement.List_White[15].Position[1]>=-Range)):
								return True
						else: #Si es Blanca
							if((Pos.Position[0]+Range-Movement.List_Black[15].Position[0]<=Range and Pos.Position[0]+Range-Movement.List_Black[15].Position[0]>=-Range) and (Pos.Position[1]+Range-Movement.List_Black[15].Position[1]<=Range and Pos.Position[1]+Range-Movement.List_Black[15].Position[1]>=-Range)):
								return True
			
		def Var(Alt):
			Void=False
			if(Movement.BoxIsTaken(Alt)!=None):
				if(Movement.BoxIsTaken(Alt)==1): #Fortificar
					for Ficha in range(0,16):
						if(Pos.ColorPiece==1):#Si es negra
							if(Movement.List_Black[Ficha].Position==Alt):
								Movement.List_Black[Ficha].Fortify=True
						else: #Si es blanca
							if(Movement.List_White[Ficha].Position==Alt):
								Movement.List_White[Ficha].Fortify=True						
				else:
					Void=Verify(Alt)
					if not (Void):
						if(Movement.BoxIsTaken(Alt)==2): #Capture

							for y in range(0,16): #Nunca se acercara a otro King o Reina
								if(Pos.ColorPiece==1):#Si es negra
									if(Movement.List_White[y].Position==Alt and Movement.List_White[y].Fortify==False):
										Pos.Capture.append(Alt)
								else: #Si es blanca
									if(Movement.List_Black[y].Position==Alt and Movement.List_Black[y].Fortify==False):
										Pos.Capture.append(Alt)
						else: #Mover
							if(Pos.Control==[]):
								Pos.Range.append(Alt)
							else:
								if not(Alt in Pos.Control):
									Pos.Range.append(Alt)

		#Movimientos

		#Inferior Derecha
		Var((Pos.Position[0]+Range,Pos.Position[1]+Range))
		#Superior Izquierda
		Var((Pos.Position[0]-Range,Pos.Position[1]-Range))
		#Inferior Izquierda
		Var((Pos.Position[0]-Range,Pos.Position[1]+Range))
		#Superior Derecha
		Var((Pos.Position[0]+Range,Pos.Position[1]-Range))
		#Abajo
		Var((Pos.Position[0],Pos.Position[1]+Range))
		#Arriba
		Var((Pos.Position[0],Pos.Position[1]-Range))

		#Izquierda
		Var((Pos.Position[0]-Range,Pos.Position[1]))
		#Derecha
		Var((Pos.Position[0]+Range,Pos.Position[1]))

		#Enroque Izquierdo
		if((Pos.Position[0]-Range,Pos.Position[1]) in Pos.Range and Pos.Special==True and Pos.Check==False and Movement.BoxIsTaken((Pos.Position[0]-(Range*2),Pos.Position[1]))==0):
			if((Movement.List_Black[12].Special==True and Pos.ColorPiece==1) or (Movement.List_White[12].Special==True and Pos.ColorPiece==-1) and Movement.BoxIsTaken((Pos.Position[0]-(Range*3),Pos.Position[1]))==0):
				Pos.Range.append((Pos.Position[0]-(Range*2),Pos.Position[1]))

		#Enroque Derecho	
		if((Pos.Position[0]+Range,Pos.Position[1]) in Pos.Range and Pos.Special==True and Pos.Check==False and Movement.BoxIsTaken((Pos.Position[0]+(Range*2),Pos.Position[1]))==0):
			if((Movement.List_Black[13].Special==True and Pos.ColorPiece==1) or (Movement.List_White[13].Special==True and Pos.ColorPiece==-1)):
				Pos.Range.append((Pos.Position[0]+(Range*2),Pos.Position[1]))

		Pos.Control=[]
		return Movement.List_White,Movement.List_Black
		