from math import inf as infinity
import random
import platform
import time
from os import system


HUMAN = -1
COMP = +1 
board=[
    [0,0,0],
    [0,0,0],
    [0,0,0]
    ]

def valoriza(estado):
    #Metodo para valorização do minimax
    score=-2
    if ganha(estado,COMP):
        score += 1
    elif ganha(estado,HUMAN):
        score -= 1
    else:
        score=0
    return score

def ganha(estado,jogador):
    #Todas as jogadas possíveis para se ganhar
    win_estado = [
        [estado[0][0], estado[0][1], estado[0][2]],
        [estado[1][0], estado[1][1], estado[1][2]],
        [estado[2][0], estado[2][1], estado[2][2]],
        [estado[0][0], estado[1][0], estado[2][0]],
        [estado[0][1], estado[1][1], estado[2][1]],
        [estado[0][2], estado[1][2], estado[2][2]],
        [estado[0][0], estado[1][1], estado[2][2]],
        [estado[2][0], estado[1][1], estado[0][2]],
    ]
    #Se ele tiver nessa lista ele ganha
    if([jogador,jogador,jogador] in win_estado):
        return True
    else:
    #Caso contrario nao 
        return False
    

def game_over(estado):
    return ganha(estado,HUMAN) or ganha(estado,COMP)

def celulas_vazias(estado):
    #Verifica celulas vazias no tabuleiro
    celulas=[]
    for x,row in enumerate(estado):
        for y,cell in enumerate(row):
            if(cell==0):
                celulas.append([x,y])
    return celulas


def movimento_valido(x,y):
    #Vê se o movimento que se quer ser feito é valido
    if [x,y] in celulas_vazias(board):
        return True
    else:
        return False 
    
def set_move(x,y,jogador):
    if(movimento_valido(x,y)):
        board[x][y]=jogador
        return True
    else:
        return False

def minimax(estado,prof,jogador):
    if(jogador==COMP):
        best=[-1,-1,-infinity]
    else:
        best=[-1,-1,+infinity]
    
    if prof == 0 or game_over(estado):
        score=valoriza(estado)
        return [-1,-1,score]
    
    #Para cada celula que está vazia
    for cell in celulas_vazias(estado):
        #pega a posição da cedula vazia
        x,y= cell[0],cell[1] 
        estado[x][y]=jogador 
        score= minimax(estado,prof-1,-jogador)
        estado[x][y]=0
        score[0],score[1]=x,y

        if(jogador == COMP):
            if(score[2]>best[2]):
                best=score #valor maximo
        else:
            if(score[2]<best[2]):
                best=score #Valor minimo
    return best 

def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

def turno_da_IA(c_choice,h_choice,difficulty):
    #Profundidade se dá no numero de cedulas
    prof=len(celulas_vazias(board))

    if prof == 0 or game_over(board):
        return
    
    clean() 
    print(f"Turno do IA")
    print_bonito(c_choice,h_choice)
    if(difficulty=='E'):
        x=random.choice([0,1,2])
        y=random.choice([0,1,2])
        while(set_move(x,y,COMP) != True):
            x=random.choice([0,1,2])
            y=random.choice([0,1,2])
    elif(difficulty=='M'):
        random_change=random.randint(0,10) 
        if(random_change in [1,2,3]): 
            x=random.choice([0,1,2])
            y=random.choice([0,1,2])
            while(set_move(x,y,COMP) != True):
                x=random.choice([0,1,2])
                y=random.choice([0,1,2])
        else: 
            #Se começa primeiro seleciona qualquer lugar
            if(prof == 9):
                x=random.choice([0,1,2])
                y=random.choice([0,1,2])
            else:
                move= minimax(board,prof,COMP)
                x,y = move[0],move[1]
            set_move(x,y,COMP)
    elif(difficulty=='H'):
    #Se começa primeiro seleciona qualquer lugar
            if(prof == 9):
                x=random.choice([0,1,2])
                y=random.choice([0,1,2])
            else:
                move= minimax(board,prof,COMP)
                x,y = move[0],move[1]
            set_move(x,y,COMP)

def print_bonito(c_choice,h_choice):
    for i in board:
        for j in i:
            print("|",end="")
            if(j==0):
                print(" ",end="")
            elif(j==COMP):
                print(c_choice,end="")
            else:
                print(h_choice,end="")
        print("|")
    print("_")
def turno_do_player(c_choice,h_choice):
    prof=len(celulas_vazias(board))

    if prof == 0 or game_over(board):
        return
    
    # Dictionary of valid moves
    move = -1
    moves = {
        7: [0, 0], 8: [0, 1], 9: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        1: [2, 0], 2: [2, 1], 3: [2, 2],
    }

    clean()
    print(f"Turno do player")
    print_bonito(c_choice,h_choice)
    while move < 1 or move > 9:
        try: 
                move= int(input("Use numpad (1..9) "))
                coordenadas=moves[move]
                pode_ir = set_move(coordenadas[0],coordenadas[1],HUMAN)

                if(not pode_ir):
                    print("Movimentação ruim")
                    move=-1
        except (EOFError, KeyboardInterrupt):
            print("Bye")
            exit()
        except(KeyError,ValueError):
            print('Bad choice')

def main():
    clean()
    h_choice=''
    c_choice=''
    first=''
    difficulty=''

    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice= input("Choose your symbol X or O\n Chosen:").upper()
        except(EOFError,KeyboardInterrupt):
            exit()
        except(KeyError,ValueError):
            print("CHOOSE AGAIN!")
    
    if(h_choice=='X'):
        c_choice='O'
    else:
        c_choice='X' 
    
    while( first != 'Y' and first !='N'):
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')
        
    while difficulty != 'E' and difficulty != 'M' and difficulty!="H":
        try:
            print('')
            difficulty= input("Choose your symbol E , M or H\n Chosen:").upper()
        except(EOFError,KeyboardInterrupt):
            exit()
        except(KeyError,ValueError):
            print("CHOOSE AGAIN!")


    while(len(celulas_vazias(board)) > 0 and not game_over(board)):
        if(first == 'N'):
            turno_da_IA(c_choice,h_choice,difficulty)
            first=''
        turno_do_player(c_choice,h_choice)
        turno_da_IA(c_choice,h_choice,difficulty)
    
    if ganha(board,HUMAN):
        clean()
        print("Voce ganhou!") 
    elif ganha(board,COMP):
        clean()
        print("VOCE PERDEU!")
    else:
        clean()
        print("EMPATE!")

main()
