def neighbours(pos, maxx, maxy):
    nbs = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    ret = [(pos[0]+x, pos[1]+y) for x,y in nbs]
    return [(x,y) for x,y in ret if x>=0 and y>=0 and x<=maxx and y<=maxy]

def extended(lst):
    new = [x[:] for x in lst]
    for sub in new:
        sub.append(0)
        sub.insert(0, 0)
    new.append([0]*len(new[0]))
    new.insert(0,[0]*len(new[0]))
    return new

def croped(lst):
    maxx = max(x for x in range(len(lst)) if 1 in lst[x])
    minx = min(x for x in range(len(lst)) if 1 in lst[x])
    maxy = max(y for y in range(len(lst[0]))\
               for x in range(len(lst)) if lst[x][y])
    miny = min(y for y in range(len(lst[0]))\
               for x in range(len(lst)) if lst[x][y])
    return [x[miny:maxy+1] for x in lst[minx:maxx+1]]

def apply_rules(cells, newcells, pos):
    x, y = pos
    lx, ly = len(cells), len(cells[0])
    
    alive = len([cells[p[0]][p[1]] for p in neighbours(pos, lx-1, ly-1)\
             if cells[p[0]][p[1]]])

    if alive < 2 or alive > 3:
        newcells[x][y] = 0
    elif (alive == 3 or alive == 2) and cells[x][y]:
        newcells[x][y] = 1
    elif alive == 3:
        newcells[x][y] = 1   

def get_1generation(cells):
    cells = extended(cells)
    maxx, maxy = len(cells), len(cells[0])
    
    newcells = [[0]*len(cells[0]) for L in cells]
    for x in range(maxx):
        for y in range(maxy):
            apply_rules(cells, newcells, (x,y))
    return croped(newcells)

def get_generation(cells, n):
    for i in range(n):
        cells = get_1generation(cells)
    return cells