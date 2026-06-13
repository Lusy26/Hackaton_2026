import random
class Cell():
    def __init__(self,pos):
        self.wall={"up":1,
                   "down":1,
                   "left":1,
                   "right":1}
        self.pos=pos
        self.visit=False
class CellBoard():
    def __init__(self,cellNumber):
        self.cellVector=[]
        self.cellNumber= cellNumber
        self.creadWhiteCellBoard()
    def creadWhiteCellBoard(self):
        for i in range(self.cellNumber):
                v=[]
                y=i*2+1
                for i in range(self.cellNumber):
                    x=i*2+1
                    v.append(Cell((x,y)))
                self.cellVector.append(v)
class Board():
    def __init__(self,cellBoard):
        self.vector=[]
        self.vectorLenght=cellBoard.cellNumber*2+1
    def boardUpdade(self,cellBoard):
        self.vector = []
        cellVector=cellBoard.cellVector
        for i in range(self.vectorLenght):
            v=[]
            for i in range(self.vectorLenght):
                v.append(-1)
            self.vector.append(v)
        for i in cellBoard.cellVector:
            for c in i:
                x,y=c.pos
                self.vector[y][x] = 0
                self.vector[y-1][x] = c.wall["up"]
                self.vector[y+1][x] = c.wall["down"]
                self.vector[y][x-1] = c.wall["left"]
                self.vector[y][x+1] = c.wall["right"]
class DFS():
    def __init__(self,cellBoard):
        self.v=[(0,0)]
        self.pos=(0,0)
        self.cellVector=cellBoard.cellVector
        self.cellNumber=cellBoard.cellNumber
        self.cellVector[0][0].visit=True
    def run(self):
        while self.v!=[]:
            vNeighbor=self.testNeighbor()
            if vNeighbor==[]:
                self.v.pop()
                if self.v!=[]:
                    self.pos=self.v[-1]
            else:
                x,y=self.pos
                dir=random.choice(vNeighbor)
                if dir == 'up':
                    self.cellVector[y][x].wall['up']=0
                    y-=1
                    self.cellVector[y][x].wall['down']=0
                elif dir =='down':
                    self.cellVector[y][x].wall['down']=0
                    y+=1
                    self.cellVector[y][x].wall['up']=0
                elif dir == "left":
                    self.cellVector[y][x].wall['left']=0
                    x-=1
                    self.cellVector[y][x].wall['right']=0
                elif dir == "right":
                    self.cellVector[y][x].wall['right']=0
                    x+=1
                    self.cellVector[y][x].wall['left']=0
                self.cellVector[y][x].visit=True
                self.pos=(x,y)
                self.v.append(self.pos)
        return self.cellVector
    def testNeighbor(self):
        v=[]
        x,y=self.pos
        if y!=0:
            if self.cellVector[y-1][x].visit==False:
                v.append("up")
        if y!=self.cellNumber-1:
            if self.cellVector[y+1][x].visit==False:
                v.append("down")
        if x!=0:
            if self.cellVector[y][x-1].visit==False:
                v.append("left")
        if x!=self.cellNumber-1:
            if self.cellVector[y][x+1].visit==False:
                v.append("right")
        return v
def generator(cellNumber):
    cellBoard= CellBoard(cellNumber)
    board=Board(cellBoard)
    cellBoard.cellVector[0][0].wall["up"]=0
    cellBoard.cellVector[-1][-1].wall["down"]=0
    board.boardUpdade(cellBoard)
    dfs=DFS(cellBoard)
    dfs.run()
    board.boardUpdade(cellBoard)
    #board.printBoard()
    return board.vector
def randomGap(maze,n,size):
    size=size*2-2
    for y in range(1,size):
        for x in range (1,size):
            if maze[y][x]==1:
                r=random.randint(1,100)
                if n>=r:
                    maze[y][x]=0
    return maze