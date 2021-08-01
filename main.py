import random
from helpers import *
from pathing import bfspathing


######### GLOBALS ################################################
# Game arena
scenario = [[0 for i in range(30)] for i in range(30)]
# variable to hold all rooms shape
rooms_g = []
# Player positions
players = [[-1,-1]]
# Player rooms
room_delays = []
player_rooms = []


########################### MAP GENERATION ##############################################
            
def init_places(areas,sizeof_areas=(17,35)):
    global scenario, rooms_g, room_delays, player_rooms
    scenario = [[0 for i in range(len(scenario[0]))] for i in range(len(scenario))] # clear scenario
    # usefull variables:
    mapw = len(scenario[0])
    mapl = len(scenario)

    #player room stuff
    player_rooms = []
    rooms_g = []
    room_delays = []
    
    rooms = []
    tempmap = [i.copy() for i in scenario]
    
    # Part 1: Generate the rooms:
    
    mapGeneratedSuccesfully = False
    while not mapGeneratedSuccesfully:
        
        # Make 100 attempts to generate more rooms
        tempmap = [i.copy() for i in scenario]
        rooms = []
        roomsgenerated = 0
        for i in range(100):
            # Generate candidate room
            x = random.randint(1,mapw)
            y = random.randint(1,mapl)
            w = random.randint(3,sizeof_areas[1]//2)
            l = random.randint(3,sizeof_areas[1]//2)
            
            # Check if viable:
            if room_fits(x,y,w,l,sizeof_areas,tempmap):
                roomsgenerated += 1
                # Log the rooms that are produced
                rooms.append((x,y,w,l,roomsgenerated))
                fill_room(x,y,w,l,tempmap)
            ##graph_map(tempmap)
            # Check if finished
            if roomsgenerated == areas:
                mapGeneratedSuccesfully = True
                break
    
    scenario = [i.copy() for i in tempmap] # For some reason this makes the two objects separate
    # Part 2: Generate the walls:
    for y in range(1,mapl - 1):
        for x in range(1,mapw - 1):
            # if all adjacent blocks are part of room:
            if tempmap[y-1][x] and tempmap[y+1][x] and tempmap[y][x+1] and tempmap[y][x-1]:
                scenario[y][x] = 0
    del(tempmap) #free allocated ram

    # Part 3: Generate doors
    for room in rooms:
        rooms_g.append(room)
        room_delays.append(random.randint(1,6))
        # 1 is top, 2 is left, 3 is bottom, 4 is right
        doorside = random.randint(1,4)
        pos = ()
        if doorside == 1:
            # Top
            shift = random.randint(1,room[2]-1)
            pos = (room[0] + shift, room[1])
            
        elif doorside == 2:
            # Left
            shift = random.randint(1,room[3]-1)
            pos = (room[0], room[1] + shift)
            
        elif doorside == 3:
            # Bottom
            shift = random.randint(1,room[2]-1)
            pos = (room[0]+room[2]-shift,room[1]+room[3])
            
        elif doorside == 4:
            # Right
            shift = random.randint(1,room[3]-1)
            pos = (room[0]+room[2],room[1]+room[3]-shift)
            
        scenario[pos[1]][pos[0]] = room[4]

def init_players(playernumber):
    global scenario,players
    players = []
    for i in range(playernumber):
        #generate a player location until it can be placed
        pos = [random.randint(0,len(scenario)-1),random.randint(0,len(scenario[0])-1)]
        while scenario[pos[0]][pos[1]] or pos in players:
            pos = [random.randint(0,len(scenario)-1),random.randint(0,len(scenario[0])-1)]
        players.append(pos)
        player_rooms.append(getroom(pos,rooms_g))

##################### PATHING #########################
def calculate_routes():
    global players,player_rooms,scenario

    impostor_pos = players[-1]

    routes = []

    for player in range(len(players)-1):
        if player_rooms[player] != -1:
            #if player is in a room:
            routes.append(bfspathing(scenario,impostor_pos,players[player]))
        else:
            routes.append([])
    return routes

def trgi_calc():
    trgis = []
    paths = calculate_routes()
    there_is_paths = False
    for i in range(len(players)-1):
        player_time = room_delays[player_rooms[i]-1]
        if len(paths[i]):
            there_is_paths = True
            trgis.append(player_time*10-(len(paths[i])))
    return max(trgis)/10 if there_is_paths else 255
#################### Visualization #############################
def draw_canvas(gamemap):
    screen = ""
    for i in range(len(gamemap)):
        for j in range(len(gamemap[0])):
            if gamemap[i][j] == 255:
                screen += "██"
            elif gamemap[i][j] == 0:
                screen += " ."
            elif str(gamemap[i][j]).isdigit() and 1<=gamemap[i][j]<=6:
                screen+= "{:>2}".format("E"+str(gamemap[i][j]))
            else :
                screen+= "{:>2}".format(gamemap[i][j])
        screen += "\n"
    print(screen)
    del(screen)

def draw_players():
    global players,scenario
    screen = ""
    for i in range(len(scenario)):
        for j in range(len(scenario[0])):
            if [i,j] in players:
                playernum = players.index([i,j])
                if playernum == len(players)-1: # player len(players-1) is allways impostor
                    screen+=" X"
                else:
                    screen+= "T"+str(playernum+1)
            else:
                if scenario[i][j] == 255:
                    screen += "██"
                elif scenario[i][j] == 0:
                    screen += " ."
                else :
                    screen+= "{:>2}".format("E"+str(scenario[i][j]))
        screen += "\n"
    print(screen)
    del(screen)

def draw_paths():
    global players,scenario
    paths = calculate_routes()
    screen = ""
    for i in range(len(scenario)):
        for j in range(len(scenario[0])):
            if [i,j] in players:
                playernum = players.index([i,j])
                if playernum == len(players)-1: # player len(players-1) is allways impostor
                    screen+=" X"
                else:
                    screen+= "T"+str(playernum+1)
            else:
                if scenario[i][j] == 255:
                    screen += "██"
                elif isPath(paths,i,j):
                    screen += "##"
                elif scenario[i][j] == 0:
                    screen += " ."
                else:
                    screen+= "{:>2}".format("E"+str(scenario[i][j]))
        screen += "\n"
    print(screen)
    del(screen)
def move_impostor(direction):
    intended_pos = players[-1].copy()
    if direction == 0:
        #top
        intended_pos[0]-=1
    elif direction == 1:
        #down
        intended_pos[0]+=1
    elif direction == 2:
        #right
        intended_pos[1]+=1
    elif direction == 3:
        #left
        intended_pos[1]-=1
    if isValid(intended_pos[0],intended_pos[1]):
        players[-1] = intended_pos

            

def main():
    command = "PLACEHOLDER"
    lastcommand = "PLACEHOLDER"
    while (command:=input()) != "quit":
        if command == "":
            command = lastcommand
        # User input processing
        if command == "init":
            init_places(6)
            init_players(5)
            draw_players()
        elif command == "top":
            move_impostor(0)
            draw_players()
        elif command == "down":
            move_impostor(1)
            draw_players()
        elif command == "right":
            move_impostor(2)
            draw_players()
        elif command == "left":
            move_impostor(3)
            draw_players()
        elif command == "route":
            draw_paths()
        elif command == "trgi":
            trgi = trgi_calc()
            print(trgi if trgi != 255 else "No hay ningun tripulante haciendo tareas")
        else:
            print("Comando ",command," Invalido")

        lastcommand = command


main()
