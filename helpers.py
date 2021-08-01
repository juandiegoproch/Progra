def getroom(pos,rooms):
    for room in rooms:
        # if player is in correct
        if pos[1]>room[0] and pos[1] < room[0] + room[2]:
            if pos[0] > room[1] and pos[0] < room[1]+room[3]:
                return room[4]
    return -1

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

def isPath(paths,i,j):
    for path in paths:
        for block in path:
            if (i,j) == block:
                return True
    return False
