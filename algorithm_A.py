#region const
order = [(0,1),(1,0),(0,-1),(-1,0)]
maze = None
endPos = None
startPos = None
openSet=None
closeSet=None
closePos=None
actualPos=None
endList=None
#endregion
class Cell():
    def __init__(self, pos,parent,g):
        self.pos=pos
        self.parent=parent
        self.g=g
        x1,y1=self.pos
        x2,y2=endPos
        self.h=abs(x2-x1)+abs(y2-y1)
        self.F=None
        self.updadeF()
    def updadeF(self):
        self.F=self.g+self.h
def add(a, b):
    return (a[0] + b[0], a[1] + b[1])
def cellInOpenSet(pos):
    for i in openSet:
        if i.pos==pos:
            return i
    return None
def cellInCloseSet(pos):
    for i in closeSet:
        if i.pos==pos:
            return i
    assert False, "Not foud parent"
def calculateG(parent):
    if parent=="Start":
        return 0 
    return parent.g+1
def cellUpdate(pos,parent):
    x,y = pos
    if x < 0:
        return
    if y < 0:
        return
    if x >= len(maze[0]):
        return
    if y >= len(maze):
        return
    if maze[pos[1]][pos[0]]!=0:
        return
    if pos in closePos:
        return
    cell=cellInOpenSet(pos)
    g=calculateG(parent)
    if cell != None:
        if g<cell.g:
            cell.parent=parent
            cell.g=g
            cell.updadeF()
    else:
        cell=Cell(pos,parent,g)
        openSet.append(cell)
    openSet.sort(key=lambda n: n.F)
def findParent(cell):
    global endList
    if cell.parent =="Start":
        endList.append(startPos)
        return
    findParent(cell.parent)
    endList.append(cell.pos)
    return
def maze_resolve_A (m,s,e):
    global maze, endPos, startPos, openSet, closeSet, actualPos, closePos,endList
    maze, endPos, startPos = m,e,s
    openSet=[]
    closeSet=[]
    closePos=[]
    endList=[]
    actualPos=startPos
    cellUpdate(actualPos,"Start")
    if len(openSet) == 0:
        raise RuntimeError("No path found")
    x=openSet.pop(0)
    closeSet.append(x)
    closePos.append(x.pos)
    actualPos=x.pos
    while actualPos!=endPos:
        for i in order:
            cellUpdate(add(actualPos,i),cellInCloseSet(actualPos))
        x=openSet.pop(0)
        closeSet.append(x)
        closePos.append(x.pos)
        actualPos=x.pos
    findParent(cellInCloseSet(actualPos))
    openPos=[]
    for i in openSet:
        openPos.append(i.pos)
    return([endList,closePos,openPos])
