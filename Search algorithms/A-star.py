import copy
import time
import math
class state:
    def __init__(self, snakepos, frt, path):
        self.snakepos = snakepos
        self.fruit = frt
        self.path = path
        h1 = 0
        h2 = 0
        for i in self.fruit:
            h2 += i[2]
            h1 += (math.sqrt((self.snakepos[0][0]-i[0])**2) + math.sqrt((self.snakepos[0][1]-i[1])**2)) * i[2]
        self.heuristic = h1*5
    def pos(self):
        return self.snakepos
    def isGoal(self):
        s = 0
        for i in self.fruit:
            s += i[2]
        return s
    def fr(self):
        return self.fruit
    def show(self):
        print("New State Created")
        print("Snake Position = ", self.snakepos)
        print("Fruit = ", self.fruit)
        print("Path until this state = ", self.path)
        printboard([5,5], self.snakepos, self.fruit)
    def sett(self):
        a = ''
        for i in self.snakepos:
            a += str(i[0])
            a += str(i[1])
        a += '+'
        for i in self.fruit:
            a += str(i[0])
            a += str(i[1])
            a += str(i[2])
        return a
    def addpath(self, a):
        self.path.append(a)
    def p(self):
        return self.path
    def getHeu(self):
        return self.heuristic

def printboard(size, pos, fruit):
    for i in range(size[0]):
        for j in range(size[1]):
            flag = 0
            flag2 = 0
            for k in pos:
                if k[0]==i and k[1]==j:
                    flag = 1
            for k in fruit:
                if k[0]==i and k[1]==j and k[2]>0:
                    flag2 = 1
            if flag==1:
                print('1', end=' ')
            elif flag2==1:
                print('$', end=' ')
            else:
                print('0', end=' ')
        print()
def overflow(l, size):
    if l[0] >= size[0]:
        l[0] = 0
    if l[0] < 0:
        l[0] = size[0] - 1
    if l[1] >= size[1]:
        l[1] = 0
    if l[1] < 0:
        l[1] = size[1]-1
    return l
def hit(head, fruit):
    for i in range(len(fruit)):
        if fruit[i][0]==head[0] and fruit[i][1]==head[1] and fruit[i][2]>0:
            return i
    return -1
def newpos(head):
    return [ head[0]-1 , head[1] ], [head[0]+1, head[1]], [head[0], head[1]-1], [head[0], head[1]+1]
def firstval(line):
    line = line.split()
    line[0] = line[0].split(',')
    val = line[0][0]
    return int(val)
def secondval(line):
    line = line.split()
    line[0] = line[0].split(',')
    val = line[0][1]
    return int(val)
def thirdval(line):
    line = line.split()
    line[0] = line[0].split(',')
    val = line[0][2]
    return int(val)

## input from file
f = open("test3.txt")
size = []
snakepos = []
n = 0
fruit = []
initPos = []
line = f.readline()
size.append(firstval(line))
size.append(secondval(line))
line = f.readline()
initPos.append(firstval(line))
initPos.append(secondval(line))
n = int(f.readline())
for i in range(n):
    line = f.readline()
    ea = []
    ea.append(firstval(line))
    ea.append(secondval(line))
    ea.append(thirdval(line))
    fruit.append(ea)

## Making initial state
snakepos.append(initPos)
mainQueue = []
initialState = state(snakepos, fruit, [])
mainQueue.append(initialState)
seen = set()
k = initialState
numberOfState = 0
## Main Loop
t1 = time.time()
while ( True ):
    numberOfState += 1
    ## Queue Head details
    f = []
    k = mainQueue.pop(0)
    pos = k.pos()
    fruts = k.fr()
    p = k.p()
    head = pos[0]
    f = copy.deepcopy(fruts)
    point = hit(head, f)
    if point != -1:
        f[point][2] -= 1
        s = 0
        for i in range(len(f)):
            s += f[i][2]
        if s==0:
            break
    else:
        last = pos.pop()

    ## new head
    up, down, left, right = newpos(head)

    ## overflow correction
    up = overflow(up, size)
    down = overflow(down, size)
    left = overflow(left, size)
    right = overflow(right, size)
    ## Possible Moves
    ch = []
    ## Left
    flag = 0
    for i in pos:
        if (i[0] == left[0] and i[1] == left[1]):
            flag = 1
    if len(pos)==1:
        if (left[0] == last[0] and left[1] == last[1]):
            flag=1
    if flag == 0:
        ch = []
        ch.append(left)
        if len(pos) > 0:
            for i in pos:
                ch.append(i)
        p2 = p.copy()
        p2 += 'L'
        newState = state(ch.copy(), f, p2)

        if newState.sett() not in seen:
            if newState.isGoal() == 0:
                break
            seen.add(newState.sett())
            i = 0
            if len(mainQueue) > 0:
                while mainQueue[i].getHeu() + len(mainQueue[i].p()) < newState.getHeu() + len(newState.p()) and i < len(mainQueue)-1:
                    i += 1
            mainQueue.insert(i, newState)
    ## Right
    flag = 0

    for i in pos:
        if (i[0] == right[0] and i[1] == right[1]):
            flag = 1
    if len(pos)==1:
        if (right[0] == last[0] and right[1] == last[1]):
            flag=1
    if flag == 0:
        ch = []
        ch.append(right)
        if len(pos) > 0:
            for i in pos:
                ch.append(i)
        p2 = p.copy()
        p2 += 'R'
        newState = state(ch.copy(), f, p2)
        if newState.sett() not in seen:
            if newState.isGoal() == 0:
                break
            seen.add(newState.sett())
            i = 0
            if len(mainQueue) > 0:
                while mainQueue[i].getHeu() + len(mainQueue[i].p()) < newState.getHeu() + len(newState.p()) and i < len(mainQueue)-1:
                    i += 1
            mainQueue.insert(i, newState)
    ## Down
    flag = 0
    for i in pos:
        if (i[0] == down[0] and i[1] == down[1]):
            flag = 1
    if len(pos)==1:
        if (down[0] == last[0] and down[1] == last[1]):
            flag=1
    if flag == 0:
        ch = []
        ch.append(down)
        if len(pos) > 0:
            for i in pos:
                ch.append(i)
        p2 = p.copy()
        p2 += 'D'
        newState = state(ch.copy(), f, p2)
        if newState.sett() not in seen:
            if newState.isGoal() == 0:
                break
            seen.add(newState.sett())
            i = 0
            if len(mainQueue) > 0:
                while mainQueue[i].getHeu() + len(mainQueue[i].p()) < newState.getHeu() + len(newState.p()) and i < len(mainQueue)-1:
                    i += 1
            mainQueue.insert(i, newState)
    ## Up
    flag=0
    for i in pos:
        if (i[0]==up[0] and i[1]==up[1]):
            flag=1
    if len(pos)==1:
        if (up[0] == last[0] and up[1] == last[1]):
            flag=1
    if flag==0:
        ch = []
        ch.append(up)
        if len(pos)>0:
            for i in pos:
                ch.append(i)
        p2 = p.copy()
        p2 += 'U'
        newState = state(ch.copy(), f, p2)
        if newState.sett() not in seen:
            if newState.isGoal()==0:
                break
            seen.add(newState.sett())
            i = 0
            if len(mainQueue) > 0:
                while mainQueue[i].getHeu() + len(mainQueue[i].p()) < newState.getHeu() + len(newState.p()) and i < len(mainQueue)-1:
                    i += 1
            mainQueue.insert(i, newState)

t2 = time.time()
print("Result of Weighted A* algorithm for TEST3, alpha = 5")
print("Time duration:", ((t2-t1)//0.01) / 100, 's')
print("Number of visited States =", len(seen))
print("Totall number of different States =", numberOfState)
print("Succesfull path distance =", len(k.p()))
print("Succesfull path is =", end=' [ ')
for i in range(len(k.p())):
    if i==20:
        print()
    if i < len(k.p())-1:
        print(k.p()[i], ',', end='')
    else:
        print(k.p()[i], end=' ')
print(']')