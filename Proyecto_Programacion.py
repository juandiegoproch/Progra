import random

# helper functions

def room_fits(roomx,roomy,roomw,rooml,sizerange,gamemap):
    #Check for size
    if roomw * rooml < sizerange[0] or roomw * rooml > sizerange[1]:
        return False
    
    # corners of bounding box for room (room must leave 1 space between itself and nearest)
    p1 = (roomx - 1,roomy - 1)
    p2 = (roomx + roomw + 2, roomy + rooml + 2)

    # Check if room is inside map
    
    mapwidth = len(gamemap[0])
    maplen = len(gamemap)


    if p1[0] < 0 or p1[1] < 0 or p2[0] >= mapwidth or p2[1] >= maplen:
        return False


    # iterate in game map passed, if a tile overlaps return false
    for y in range(p1[1],p2[1]+1):
        for x in range(p1[0],p2[0]+1):
            if gamemap[y][x] == 255:
                return False
    # Return true if no tiles overlap
    return True

def fill_room(roomx,roomy,roomw,rooml,gamemap):
    # Get corners
    p1 = (roomx,roomy)
    p2 = (roomx + roomw, roomy + rooml)

    # Write room
    for y in range(p1[1],p2[1]+1):
        for x in range(p1[0],p2[0]+1):
            gamemap[y][x] = 255




def draw_canvas(gamemap):
    SIZEOF_MAP = 1
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
    return

def init_places(gamemap,areas,sizeof_areas=(15,25)):
    
    # usefull variables:
    mapw = len(gamemap[0])
    mapl = len(gamemap)
    
    
    rooms = []
    tempmap = gamemap.copy()
    
    # Part 1: Generate the rooms:
    
    mapGeneratedSuccesfully = False
    while not mapGeneratedSuccesfully:
        
        # Make 100 attempts to generate more rooms
        tempmap = [i.copy() for i in gamemap]
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

    gamemap = [i.copy() for i in tempmap]

    # Part 2: Generate the walls:
    for y in range(1,mapl - 1):
        for x in range(1,mapw - 1):
            # if all adjacent blocks are member of room:
            if tempmap[y-1][x] and tempmap[y+1][x] and tempmap[y][x+1] and tempmap[y][x-1]:
                gamemap[y][x] = 0

    # Part 3: Generate doors
    doors={}
    for room in rooms:
        
        # 1 is top, 2 is left, 3 is bottom, 4 is right
        doorside = random.randint(1,4)
        if doorside == 1:
            # Top
            shift = random.randint(1,room[2]-1)
            pos = (room[0] + shift, room[1])
            gamemap[pos[1]][pos[0]] = room[4]
            doors["E"+str(room[4])] = pos[1],pos[0]
        elif doorside == 2:
            # Left
            shift = random.randint(1,room[3]-1)
            pos = (room[0], room[1] + shift)
            gamemap[pos[1]][pos[0]] = room[4]
            doors["E"+str(room[4])] = pos[1],pos[0]
        elif doorside == 3:
            # Bottom
            shift = random.randint(1,room[2]-1)
            pos = (room[0]+room[2]-shift,room[1]+room[3])
            gamemap[pos[1]][pos[0]] = room[4]
            doors["E"+str(room[4])] = pos[1],pos[0]
        elif doorside == 4:
            # Right
            shift = random.randint(1,room[3]-1)
            pos = (room[0]+room[2],room[1]+room[3]-shift)
            gamemap[pos[1]][pos[0]] = room[4]
            doors["E"+str(room[4])] = pos[1],pos[0]

    return gamemap,doors


def init_player(mapa):
    dic = {}
    for i in range(5):
        cord_player_x = random.randint(0,29)
        cord_player_y = random.randint(0,29)
        while mapa[cord_player_x][cord_player_y]!=0 or (cord_player_x,cord_player_y) in dic.values():
            cord_player_x = random.randint(0,29)
            cord_player_y = random.randint(0,29)
        if i!=4:
            dic[f"T{i+1}"] =cord_player_x,cord_player_y
        else :
            dic["X"] = cord_player_x,cord_player_y
    return dic

def draw_player(mapa,d):
    for key,value in d.items():
        mapa[value[0]][value[1]] = key
    return mapa

def move_impostor(option,d,mapa,puertas):

    x,y= d["X"]
    if option=="down":
        if not(0<=x+1<=29) or not(0<=y<=29) or mapa[x+1][y]==255 or mapa[x+1][y] in d.keys():
            return draw_player(mapa,d)
        else :
            if (x,y) in puertas.values():
                for k,v in puertas.items():
                    if v==(x,y):
                        mapa[x][y]=k
            else:
                mapa[x][y]=0
            d["X"]=x+1,y
            return draw_player(mapa,d)
    
    elif option=="left":
        if  not(0<=x<=29) or not(0<=y-1<=29) or mapa[x][y-1]==255 or mapa[x][y-1] in d.keys():
            return draw_player(mapa,d)
        else :
            if (x,y) in puertas.values():
                for k,v in puertas.items():
                    if v==(x,y):
                        mapa[x][y]=k
            else:
                mapa[x][y]=0
            d["X"]=x,y-1
            return draw_player(mapa,d)

    elif option=="right":
        if not(0<=x<=29) or not(0<=y+1<=29) or mapa[x][y+1]==255 or mapa[x][y+1] in d.keys() :
            return draw_player(mapa,d)
        else :
            if (x,y) in puertas.values():
                for k,v in puertas.items():
                    if v==(x,y):
                        mapa[x][y]=k
            else:
                mapa[x][y]=0
            d["X"]=x,y+1
            return draw_player(mapa,d)
    
    elif option=="top":
        if  not(0<=x-1<=29) or not(0<=y<=29) or mapa[x-1][y]==255 or mapa[x-1][y] in d.keys():
            return draw_player(mapa,d)
        else :
            if (x,y) in puertas.values():
                for k,v in puertas.items():
                    if v==(x,y):
                        mapa[x][y]=k
            else:
                mapa[x][y]=0
            d["X"]=x-1,y
            return draw_player(mapa,d)
    else :
        return draw_player(mapa,d)

def main():
    scenario = [[0 for i in range(30)] for j in range(30)]
    mapa_base, mapa_puertas = init_places(scenario,6)
    place_player = init_player(mapa_base)
    mapa_base = draw_player(mapa_base,place_player)
    draw_canvas(mapa_base)
    dir = input()
    while dir !='' :
        draw_canvas(move_impostor(dir,place_player,mapa_base,mapa_puertas))
        dir = input()

main()