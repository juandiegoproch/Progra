import random

######### GLOBALS ################################################
scenario = [[0 for i in range(30)] for i in range(30)]
players = [[-1,-1]]

######### HELPERS ################################################
def isValid(x,y):
    if x > len(scenario)-1 or x<0 or y > len(scenario[0])-1 or y<0: # OutOfBounds
        return False
    if scenario[x][y] == 255: # is wall
        return False
    if [x,y] in players[:-1]: #is ocupied
        return False
    return True

def room_fits(roomx,roomy,roomw,rooml,sizerange,where):
    #Check for size
    if roomw * rooml < sizerange[0] or roomw * rooml > sizerange[1]:
        return False
    
    # corners of bounding box for room (room must leave 1 space between itself and nearest)
    p1 = (roomx - 1,roomy - 1)
    p2 = (roomx + roomw + 2, roomy + rooml + 2)

    # Check if room is inside map
    
    mapwidth = len(where[0])
    maplen = len(where)


    if p1[0] < 0 or p1[1] < 0 or p2[0] >= mapwidth or p2[1] >= maplen:
        return False


    # iterate in game map passed, if a tile overlaps return false
    for y in range(p1[1],p2[1]+1):
        for x in range(p1[0],p2[0]+1):
            if where[y][x] == 255:
                return False
    # Return true if no tiles overlap
    return True

def fill_room(roomx,roomy,roomw,rooml,where):
    # Get corners
    p1 = (roomx,roomy)
    p2 = (roomx + roomw, roomy + rooml)

    # Write room
    for y in range(p1[1],p2[1]+1):
        for x in range(p1[0],p2[0]+1):
            where[y][x] = 255

########################### MAP GENERATION ##############################################
            
def init_places(areas,sizeof_areas=(15,25)):
    global scenario
    scenario = [[0 for i in range(len(scenario[0]))] for i in range(len(scenario))] # clear scenario
    # usefull variables:
    mapw = len(scenario[0])
    mapl = len(scenario)
    
    
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
        else:
            print("Comando ",command," Invalido")

        lastcommand = command


main()
