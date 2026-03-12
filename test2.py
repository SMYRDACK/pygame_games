
#liczba kolumn i wierszy mapy (musi byc nieparzysta)
COLS=31
ROWS=51
tile_size = 128


def zmien_wymiary_plaszy(x,y):
    global COLS, ROWS
    if x % 2 == 0:
        COLS = x + 1
    else:
        COLS = x
    if y % 2 == 0:
        ROWS = y + 1
    else:
        ROWS = y
def pokaz():
    print(COLS," ",ROWS)