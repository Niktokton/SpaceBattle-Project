import random


def get_table():
    return [['' for _ in range(100)] for _ in range(100)]


def mapgen(tplay1, tplay2):
    newmap = open('data/map.txt', 'w')
    mp = get_table()
    for x in range(100):
        for y in range(100):
            tmp = random.choices(['.', '#'], weights=[90, 10])
            mp[x][y] = tmp[0]
    if tplay2 == 1:
        for i in range(8):
            mp[random.randrange(10, 20)][random.randrange(45, 55)] = '-'
    elif tplay2 == 2:
        for i in range(3):
            mp[random.randrange(10, 20)][random.randrange(45, 55)] = '-'
    elif tplay2 == 3:
        mp[random.randrange(10, 20)][random.randrange(45, 55)] = '-'
    if tplay1 == 1:
        for i in range(8):
            mp[random.randrange(80, 90)][random.randrange(45, 55)] = '+'
    elif tplay1 == 2:
        for i in range(3):
            mp[random.randrange(80, 90)][random.randrange(45, 55)] = '+'
    elif tplay1 == 3:
        mp[random.randrange(80, 90)][random.randrange(45, 55)] = '+'
    mp[50][50] = '@'
    for x in range(100):
        tmp = ''
        for y in range(100):
            tmp += mp[x][y]
        newmap.write(tmp)
        newmap.write('\n')
