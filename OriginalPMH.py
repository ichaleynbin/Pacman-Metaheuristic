row = 0
Memory.start = problem.getStartState()
start = problem.getStartState()
for x in foodGrid:
    col = 0
    for y in x:
        node = Memory.Node()
        Memory.Nodes[(row,col)] = Memory.Node()

        if y or (start[0]==(row,col)):
            Memory.Nodes[(row,col)].GoalState = 1
            Memory.GoalStatedict[(row,col)] = {}
        else:
            Memory.Nodes[(row,col)].GoalState = 0
        col +=1
    row += 1
for (x,y) in Memory.GoalStatedict:
    for (z,w) in Memory.GoalStatedict:
        Memory.GoalStatedict[(x,y)][(z,w)] = 0
for (x,y) in Memory.Nodes:
    if x != 0 and x != 29 and y != 0 and y != 13:
        if not problem.walls[x][y]:
            succlist = problem.getSuccessors(((x,y),start[1]))
            for item in succlist:
                Memory.Successors((x,y),item[0][0],(item[1],Memory.RD[item[1]]))
Fringe = util.Queue()
dictum = {}
counter = 0
bools = ()
Memory.GoalList = Memory.GoalStatedict.keys()
Memory.GoalList.pop(Memory.GoalList.index(start[0]))
for x in range(len(Memory.GoalList)):
    bools = bools + (1,)
for (x,y) in Memory.GoalStatedict:
    dictum[counter] = ((start+bools),(start[0]),(x,y),Directions.STOP,dist(start[0],(x,y)),counter,counter)
    Fringe.push(counter)
    counter +=1
    for (z,w) in Memory.GoalStatedict[(x,y)]:
        Fringe.push(counter)
        dictum[counter] = (((x,y),start[1])+bools,(x,y),(z,w),Directions.STOP,dist((x,y),(z,w)),counter,counter)
        counter += 1
Node = dictum[Fringe.pop()]
State = Node[0]
CS = {}
Cs2 = {}
breaker = 0
while not Fringe.isEmpty():
    while State[0]+Node[2]+Node[1] in CS or State[0]+Node[1]+Node[2] in CS:
        if State+Node[1]+Node[2] in CS:
            try: Node = dictum[Fringe.pop()]
            except IndexError:
                breaker = 1
                break;
            State = Node[0]
        else:
            if Memory.GoalStatedict[Node[1]][Node[2]]== 0 and State[0]+Node[2]+Node[1] in CS:
                Memory.GoalStatedict[Node[1]][Node[2]] = (Node[-2],CS[State[0]+Node[2]+Node[1]])
                try: Node = dictum[Fringe.pop()]
                except IndexError:
                    breaker = 1
                    break;
                State = Node[0]
            else:
                try: Node = dictum[Fringe.pop()]
                except IndexError:
                    breaker = 1
                    break;
            State = Node[0]
    if breaker == 1:
        break;
    for (x,y) in Memory.Nodes[State[0][:2]].Successors:
        if (x,y) in Memory.GoalList:
            inder = Memory.GoalList.index((x,y))
            bools = bools[:inder] + (0,) + bools[(inder+1):]
        item = (((x,y),State[1]),)+Memory.Nodes[State[0][:2]].Successors[(x,y)]
        newitem = (item[0]+State[2:], Node[1],Node[2],item[1],item[2],Node[-3] + item[2], counter, Node[-2])
        dictum[counter] = newitem
        Fringe.push(counter)
        counter += 1
    CS[State[0]+Node[1]+Node[2]] = Node[-2]
    Cs2[State] = Node[-2]
newdict = {}
for (x,y) in Memory.GoalStatedict:
    for (z,w) in Memory.GoalStatedict[(x,y)]:
        if (x,y) != (z,w):
            lister = []
            node1,node2 = dictum[Memory.GoalStatedict[(x,y)][(z,w)][0]], dictum[Memory.GoalStatedict[(x,y)][(z,w)][1]]
            leng = 0
            if node1[0][0] == node1[-5]:
                print "do something here"
            while node1[0][0] != node1[-6]:
                try: lister[-1]
                except IndexError:
                    lister.append(node1[0][0])
                    node1 = dictum[node1[-1]]
                    leng += 1
                    continue;
                if not node1[0][0] == lister[-1]:
                    lister.append(node1[0][0])
                    node1 = dictum[node1[-1]]
                    leng += 1
                    continue;
                else:
                    node1 = dictum[node1[-1]]
            lister.append(node1[0][0])
            lister.reverse()
            while node2[0][0] != node2[-6]:
                try: lister[-1]
                except IndexError:
                    lister.append(node2[0][0])
                    node2 = dictum[node2[-1]]
                    leng += 1
                    continue;
                if not node2[0][0] == lister[-1]:
                    lister.append(node2[0][0])
                    node2 = dictum[node2[-1]]
                    leng += 1
                    continue;
                else:
                    node2 = dictum[node2[-1]]
            lister.append(node2[0][0])
            if (x,y) in lister:
                lister.pop(lister.index((x,y)))
            cont = 0
            leng += 1
            Memory.Nodes[(x,y)].paths[(z,w)] = (lister,len(lister))
queue2 = util.PriorityQueue()
nstate = ()
goalstate = ()
while len(nstate) < (len(Memory.GoalList)):
    goalstate = goalstate + (0,)
    nstate = nstate + (1,)
count = 0
newstate = Memory.start[0]+nstate+(count,0,0)        
dm = {count:newstate}
count += 1
print "primed"
while newstate[2:-3] != goalstate:
    for x in range(len(Memory.GoalList)):
        if newstate[2+x] and newstate[:2]!=Memory.GoalList[x]:
            boools = newstate[2:-3]
            path, newcost= Memory.Nodes[newstate[:2]].paths[Memory.GoalList[x]]
            for item in path:
                if item in Memory.GoalStatedict and not item == Memory.start[0]:
                    place = Memory.GoalList.index(item)
                    if boools[place]:
                        boools = boools[:place] + (0,) + boools[(place+1):]
            newitem = Memory.GoalList[x]+boools + (count,newstate[-3],newstate[-1]+newcost)
            hcost = max(map(lambda z,y:z[1]*y,Memory.Nodes[newitem[:2]].paths[Memory.GoalList[x]][1], boools)) if newitem[:2]!=Memory.GoalList[x] else 0
            dm[count] = newitem
            queue2.push(count,(newitem[-1]+hcost))
            count += 1
    newstate = dm[queue2.pop()]
newstater = newstate
listy = []
nextstate = dm[newstater[-2]]
print newstater,newstate,nextstate
while newstater[:2] != start[0]:
    newlist = Memory.Nodes[nextstate[:2]].paths[newstater[:2]][0][::-1]
    for item in newlist:
        try: listy[-1]
        except IndexError:
            listy.append(item)                    
            continue;
        if dist(item,listy[-1]) == 1:
            listy.append(item)
        else:
            while dist(item,listy[-1]) != 1:
                listy.pop()
            listy.append(item)
    newstater = nextstate
    nextstate = dm[newstater[-2]]
listy.append(newstater[:2])
startcount = len(listy)
listy.reverse()
Memory.heurvals = {}
boools = ()
for x in range(len(Memory.GoalList)):
    boools = boools + (1,)
for x in range(len(listy)):
    if not listy[x] in Memory.heurvals:
        if listy[x] in Memory.GoalList:
            n = Memory.GoalList.index(listy[x])
            boools = boools[:n] + (0,) + boools[(n+1):]
        Memory.heurvals[listy[x]+(sum(boools),)] = (startcount-x-1,sum(boools))
        Memory.heurvals1[listy[x]] = (startcount-x-1,sum(boools))
Memory.init = 1
print "dun"
