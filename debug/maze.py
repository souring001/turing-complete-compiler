arrows = ['→', '↓', '←', '↑']

def maze(dir, rot, n):
    if n == 0:
        return

    dir = dir + rot
    maze(dir, -rot, n-1)
    print(arrows[dir], dir, n)

    dir = dir - rot
    maze(dir, rot, n-1)
    print(arrows[dir], dir, n)
    maze(dir, rot, n-1)

    dir = dir - rot
    print(arrows[dir], dir, n)
    maze(dir, -rot, n-1)

maze(0, -1, 3)