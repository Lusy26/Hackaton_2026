def printBoard(maze):
    for i in maze:
        for o in i:
            if o == -1:
                #print("🟪", end=" ")
                print("⬛", end=" ")
            elif o==0:
                print("⬜", end=" ")
            elif o==1:
                print("⬛", end=" ")
            elif o==2:
                print("🟥", end=" ")
            elif o==3:
                print("🟩", end=" ")
            elif o==4:
                print("🟨", end=" ")
            else:
                assert False, "face not found"
        print("")
def updatePass(maze, v,n):
    for i in v:
        x,y=i
        maze[y][x]=n
    return maze