# from blessed import Terminal
import random

# config:
TABLE_SIZE = 4
NEXT_ITEM = 2 # after every correct move will add one "2" in table
# ------------[ [item, chance of item], ...]
# NEXT_ITEMS = [[2, 90], [4, 10]]
KEYS_MOVES = {
  # WASD mode:
  "W":"top",
  "A":"left",
  "S":"down",
  "D":"right",
  # HJKL vim mode:
  "K":"top",
  "H":"left",
  "J":"down",
  "L":"right",
}

# numbers (y,x):(7,3)
NUMBERS = (
  [[1,1,1],
  [1,0,1],
  [1,0,1],
  [1,0,1],
  [1,0,1],
  [1,0,1],
  [1,1,1]],

  [[0,1,0],
  [0,1,0],
  [0,1,0],
  [0,1,0],
  [0,1,0],
  [0,1,0],
  [0,1,0]],

  [[1,1,1],
  [1,0,1],
  [0,0,1],
  [1,1,1],
  [1,0,0],
  [1,0,0],
  [1,1,1]],

  [[1,1,1],
  [0,0,1],
  [0,0,1],
  [1,1,1],
  [0,0,1],
  [0,0,1],
  [1,1,1]],

  [[1,0,1],
  [1,0,1],
  [1,0,1],
  [1,1,1],
  [0,0,1],
  [0,0,1],
  [0,0,1]],

  [[1,1,1],
  [1,0,0],
  [1,0,0],
  [1,1,1],
  [0,0,1],
  [1,0,1],
  [1,1,1]],

  [[1,1,1],
  [1,0,0],
  [1,0,0],
  [1,1,1],
  [1,0,1],
  [1,0,1],
  [1,1,1]],

  [[1,1,1],
  [0,0,1],
  [0,0,1],
  [0,0,1],
  [0,0,1],
  [0,0,1],
  [0,0,1]],

  [[1,1,1],
  [1,0,1],
  [1,0,1],
  [1,1,1],
  [1,0,1],
  [1,0,1],
  [1,1,1]],

  [[1,1,1],
  [1,0,1],
  [1,0,1],
  [1,1,1],
  [0,0,1],
  [0,0,1],
  [1,1,1]]
)


# 31 * 13


# funcs
def new_empty_table(table_size):
  table = [[0]*table_size]*table_size
  return table

# returns list [ {"y":y1,"x":x1} , {"y":y2,"x":x2} , ... ] of empty cells
def get_empty_cells(table:list):
  empty_cells=[]

  rows = len(table)
  cols = len(table[0])

  # find empty cells and put them in empty_cells var
  for y in range(rows):
    for x in range(cols):
      if table[y][x]==0:
        empty_cells.append({"y":y,"x":x})

  return empty_cells

def get_random_cell(cells:list):
  cells_count = len(cells)
  random_index = random.randint(0,cells_count)
  random_cell = cells[random_index]
  return random_cell



# add an item to table after played a correct move
def add_next_number(table:list,item:int):
  empty_cells = get_empty_cells(table)
  random_cell = get_random_cell(empty_cells)
  table[random_cell[0]][random_cell[1]] = item
  return table


# moving cols(top and down) and rows(left and right) with an empty cells x,y only
def move_col_top(table:list,y,x):
  new_table = table[:]
  for i in range(y, TABLE_SIZE-1):
    new_table[i][x] = table[i+1][x]
  new_table[TABLE_SIZE-1][x]=0;
  return new_table

def move_row_left(table:list,y,x):
  new_table = table[:]
  for i in range(x, TABLE_SIZE-1):
    new_table[y][i] = table[y][i+1]
  new_table[y][TABLE_SIZE-1]=0;
  return new_table

def move_col_down(table:list,y,x):
  new_table = table[:]
  for i in range(y, 0, -1): # "-1" -> reversed
    new_table[i][x] = table[i-1][x]
  new_table[0][x]=0;
  return new_table

def move_row_right(table:list,y,x):
  new_table = table[:]
  for i in range(x, 0, -1): # "-1" -> reversed
    new_table[y][i] = table[y][i-1]
  new_table[y][0]=0;
  return new_table


# moving table in 4 directions (top, left, down, right)
def move_table_top(table:list):
  empty_cells = get_empty_cells(table)
  empty_cells.reverse()
  for empty_cell in empty_cells:
    table = move_col_top(table, empty_cell["y"], empty_cell["x"])
  return table

def move_table_left(table:list):
  empty_cells = get_empty_cells(table)
  empty_cells.reverse()
  for empty_cell in empty_cells:
    table = move_row_left(table, empty_cell["y"], empty_cell["x"])
  return table

def move_table_down(table:list):
  empty_cells = get_empty_cells(table)
  for empty_cell in empty_cells:
    table = move_col_down(table, empty_cell["y"], empty_cell["x"])
  return table

def move_table_right(table:list):
  empty_cells = get_empty_cells(table)
  for empty_cell in empty_cells:
    table = move_row_right(table, empty_cell["y"], empty_cell["x"])
  return table

# sum cells in 4 directions
def sum_to_top(table:list):
  new_table = table[:]
  x = 0
  while(x < TABLE_SIZE):
    y = 0
    while(y < TABLE_SIZE - 1): # "-1": NO LAST CELL
      if new_table[y][x] != 0:# not empty
        if new_table[y][x] == new_table[y+1][x]:
          new_table[y][x] *= 2
          new_table = move_col_top(new_table, y+1, x)
          y -= 1
      y += 1
    x += 1
  return new_table

def sum_to_left(table:list):
  new_table = table[:]
  y = 0
  while(y < TABLE_SIZE):
    x = 0
    while(x < TABLE_SIZE - 1): # "-1": NO LAST CELL
      if new_table[y][x] != 0: # not empty
        if new_table[y][x] == new_table[y][x+1]:
          new_table[y][x] *= 2
          new_table = move_row_left(new_table, y, x+1)
          x -= 1
      x += 1
    y += 1
  return new_table

def sum_to_down(table:list):
  new_table = table[:]
  x = 0
  while(x < TABLE_SIZE):
    y = TABLE_SIZE - 1
    while(y > 0): # "> 0": NO FIRST CELL
      if new_table[y][x] != 0:# not empty
        if new_table[y][x] == new_table[y-1][x]:
          new_table[y][x] *= 2
          new_table = move_col_down(new_table, y-1, x)
          y += 1
      y -= 1
    x += 1
  return new_table

def sum_to_right(table:list):
  new_table = table[:]
  y = 0
  while(y < TABLE_SIZE):
    x = TABLE_SIZE - 1
    while(x > 0): # "> 0": NO FIRST CELL
      if new_table[y][x] != 0: # not empty
        if new_table[y][x] == new_table[y][x-1]:
          new_table[y][x] *= 2
          new_table = move_row_right(new_table, y, x-1)
          x += 1
      x -= 1
    y += 1
  return new_table





def move_table(table:list, move:str):
  new_table = table[:]
  # move = top, left, down, right
  match move:
    case "top":
      new_table = sum_to_top(move_table_top(new_table))
    case "left":
      new_table = sum_to_left(move_table_left(new_table))
    case "down":
      new_table = sum_to_down(move_table_down(new_table))
    case "right":
      new_table = sum_to_right(move_table_right(new_table))
    case _:
      print("incorrect move")
  # print(table==new_table)

  return new_table;


# for see result in better style
from pprint import pprint
def p(t):
  pprint(t,width=20, compact=True)

def main():
  # game_table = new_empty_table(TABLE_SIZE)
  # print(game_table)
  # print(get_empty_cells(game_table))
  # print(get_random_cell(get_empty_cells(game_table)))

  test_table = [[2, 2, 2, 2],
                [2, 0, 1, 0],
                [0, 2, 3, 0],
                [5, 1, 4, 1]]
  p(test_table)
  p("---")

  p("t")
  p(move_table([[2, 2, 2, 2],
                [2, 0, 1, 0],
                [0, 2, 3, 0],
                [5, 1, 4, 1]],"top"))
  p("l")
  p(move_table([[2, 2, 2, 2],
                [2, 0, 1, 0],
                [0, 2, 3, 0],
                [5, 1, 4, 1]],"left"))
  p("d")
  p(move_table([[2, 2, 2, 2],
                [2, 0, 1, 0],
                [0, 2, 3, 0],
                [5, 1, 4, 1]],"down"))
  p("")
  p(move_table([[2, 2, 2, 2],
                [2, 0, 1, 0],
                [0, 2, 3, 0],
                [5, 1, 4, 1]],"right"))
  print(test_table==move_table(test_table,"top"))
  # print(move_row_right(test_table,0,2))
  # print(move_row_left(test_table,0,0))
  # print(move_col_top(test_table,2,1))
  # print(move_col_down(test_table,2,1))






# start app
if __name__ == "__main__":
    main()