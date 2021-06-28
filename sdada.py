#imports
import random

#defines
UP_I = 0
DOWN_I = 1
LEFT_I = 2
RIGHT_I = 3

# GLOBALS


def draw_canvas(gamemap):
    for i in range(len(gamemap)*4):
        for j in range(len(gamemap)*4):
            whichSquareAmIIn = (i//4,j//5)
            print(whichSquareAmIIn,end="")
            whereImInSquare = (i%4,j%4)
        print()

draw_canvas([[[random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1)]]*20]*20)
                

def init_places(gamemap,players):
    #create rooms

    roomap = [[0]*20]*20
    temp_roomap = [[0]*20]*20

    roomcount = 1
    while roomcount < 8:
        posx = random.randint(0,20)
        posy = random.randint(0,20) 
        


def init_players(gamemap,players):
    
    for i in range(5):
        x = random.randint(1,20)
        y = random.randint(1,20)
        players[i][0]=x
        players[i][1]=y
        while players[i] in players :
            x = random.randint(1,20)
            y = random.randint(1,20)
            coord = x,y
        players[i][0]=x
        players[i][1]=y
        
    return players

def move_impostor(gamemap,players,option=None):
    pass

def main():
    gamemap = [[[0,0,0,0]]*20]*20
    players = [[0,0]*5]

    impostor = random.randint(1,5)
    players = init_players(gamemap, players)
































































