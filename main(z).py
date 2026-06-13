from maze_generator import generator, randomGap
from maze_printer import printBoard, updatePass
from algorithm_A import maze_resolve_A
n=18
maze=generator(n)
maze=randomGap(maze,10,n)
print(maze)
v=maze_resolve_A(maze,(1,0),(2*n-1,2*n))
fv,cv,ov=v
maze=updatePass(maze,ov,4)
maze=updatePass(maze,cv,3)
maze=updatePass(maze,fv,2)
printBoard(maze)




