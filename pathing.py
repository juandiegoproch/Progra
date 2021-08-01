scene =[[0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]]
scene = [[255 if i else 0 for i in r] for r in scene]

def isValid(x,y,sce):
    max_x = len(sce)
    max_y = len(sce[0])

    if (x >= 0 and x < max_x) and (y >= 0 and y <max_y):
        # it is in bounds
        if sce[x][y] == 1:
            # it doesnt interfere with walls
            return True
    return False
def graphqueue(grid,tovisit,dest,origin):
    buffer = ""
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i,j) == dest or (i,j) == origin:
                buffer+="&&"
            elif (i,j) in tovisit:
                buffer+= "##"
            else:
                buffer += "██" if grid[i][j] == 255 else " ."
        buffer+="\n"
    print(buffer)
    print()

    
def bfspathing(scenario,pos,target):
    
    pos = tuple(pos)
    target = tuple(target)
    
    gamemap = [[ 0 if i == 255 else 1 for i in r] for r in scenario]
    prev_mat = [[ (-1,-1) for i in r] for r in scenario]
    queue = [pos]
    hasfound = False
    
    while len(queue) != 0 and not hasfound:
        tempqueue = []
        #expand all queue elems
        for node in queue:
            x,y = node
            if node == target:
                hasfound = True
                break
            
            # append all new elems
            if isValid(x+1,y,gamemap):
                tempqueue.append((x+1,y))
                prev_mat[x+1][y] = node
                
            if isValid(x-1,y,gamemap):
                tempqueue.append((x-1,y))
                prev_mat[x-1][y] = node
                
            if isValid(x,y+1,gamemap):
                tempqueue.append((x,y+1))
                prev_mat[x][y+1] = node
                
            if isValid(x,y-1,gamemap):
                tempqueue.append((x,y-1))
                prev_mat[x][y-1] = node
                
            gamemap[node[0]][node[1]] = 0
        # copy to the queue
        queue = []
        # adress bug about duplicates

        for i in tempqueue:
            if i not in queue:
                queue.append(i)
                if i == target:
                    hasfound = True

        #queue = tempqueue
    
    steps = []
    current_backtrack = target
    while current_backtrack != pos:
        steps.append(current_backtrack)
        current_backtrack = prev_mat[current_backtrack[0]][current_backtrack[1]]
    return steps + [pos]

bfspathing(scene,(0,0),(4,4))
