from blessed import Terminal
import random
import copy





## for see result in better style
# from pprint import pprint
# def p(t):
#   pprint(t,width=20, compact=True)



# config:
TABLE_SIZE = 4

# pls write items in order lowest to highest chance (sum of chances must be 100)
# ------------[ [item, chance of item], ...]
NEXT_ITEMS = [[4, 10], [2, 90]]
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

# blessed confs
# - cells:
CELL_PADDING_Y = 3 # padding (top and bottom) cells
CELL_PADDING_X = 1 # padding (left and right) cells
CELL_MAX_NUMBER_LENGTH = 7 # max numbers(length) in a cell
CELL_SIZE_Y = len(NUMBERS[0]) + (CELL_PADDING_Y * 2)
CELL_SIZE_x = (len(NUMBERS[0][0]) * CELL_MAX_NUMBER_LENGTH) + (CELL_PADDING_X * 2)
CELL_EMPTY_CHAR = " " # zeroes in NUMBERS
CELL_FILL_CHAR = "█" # ones in NUMBERS
CELL_GAP_CHAR = "█" # between cells
# - window:
WINDOW_PADDING_Y = 1
WINDOW_PADDING_X = 2
WINDOW_BORDER_Y = 1
WINDOW_BORDER_X = 2
WINDOW_WALL_CHAR = "█"
WINDOW_PADDING_CHAR = " "
WINDOW_SCORE_TEXT = "SCORE: "
WINDOW_SCORE_POS_Y = 1
WINDOW_SCORE_POS_X = 3
WINDOW_GOODBYE_TITLE = "Goodbye :D"
WINDOW_GOODBYE_TEXT = "Press any key to exit or w8 3s"

# funcs
# - cells funcs:
def new_empty_table(table_size):
  table = [[0]*table_size for _ in range(table_size)]
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
  random_index = random.randint(0,cells_count-1)
  random_cell = cells[random_index]
  return random_cell


def choose_random_item():
  random_number = random.randrange(0,100 + 1)
  minimum = 0
  for item in NEXT_ITEMS:
    maximum = item[1] + minimum
    if (minimum <= random_number <= maximum):
      return item[0]
    minimum = maximum
  return 0

# add an item to table after played a correct move
def add_next_number(table:list,item:int=choose_random_item()):
  empty_cells = get_empty_cells(table)
  random_cell = get_random_cell(empty_cells)
  y = random_cell["y"]
  x = random_cell["x"]

  table[y][x]=item
  return table


# moving cols(top and down) and rows(left and right) with an empty cells x,y only
def move_col_top(table:list,y,x):
  new_table = copy.deepcopy(table)
  for i in range(y, TABLE_SIZE-1):
    new_table[i][x] = table[i+1][x]
  new_table[TABLE_SIZE-1][x]=0;
  return new_table

def move_row_left(table:list,y,x):
  new_table = copy.deepcopy(table)
  for i in range(x, TABLE_SIZE-1):
    new_table[y][i] = table[y][i+1]
  new_table[y][TABLE_SIZE-1]=0;
  return new_table

def move_col_down(table:list,y,x):
  new_table = copy.deepcopy(table)
  for i in range(y, 0, -1): # "-1" -> reversed
    new_table[i][x] = table[i-1][x]
  new_table[0][x]=0;
  return new_table

def move_row_right(table:list,y,x):
  new_table = copy.deepcopy(table)
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
  new_table = copy.deepcopy(table)
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
  new_table = copy.deepcopy(table)
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
  new_table = copy.deepcopy(table)
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
  new_table = copy.deepcopy(table)
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
  new_table = copy.deepcopy(table)

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

  # if table has been changed then we add next number and increase score
  if (table != new_table):
    # TODO: increase score here
    new_table = add_next_number(table=new_table);
  return new_table;




# - widnow funcs:
def draw_border(term):
  # for y in range(int(max_y)):
  #   if y < (WINDOW_BORDER_Y) or y > (max_y-WINDOW_BORDER_Y):
  border_y = (WINDOW_WALL_CHAR * term.width)
  for y in range(WINDOW_BORDER_Y):
    print(term.move_xy(0,y)+f'{border_y}{term.normal}',end='')
    print(term.move_xy(0, term.height-1-y)+f'{border_y}{term.normal}',end='')

  border_x = (WINDOW_WALL_CHAR * WINDOW_BORDER_X)
  for y in range(term.height):
    print(term.move_xy(0, y)+f'{border_x}{term.normal}',end='')
    print(term.move_xy(term.width-WINDOW_BORDER_X, y)+f'{border_x}{term.normal}',end='')

  print(term.move_xy(0,0))




def main():
  game_table = new_empty_table(TABLE_SIZE)
  game_table = add_next_number(table=game_table)
  game_table = add_next_number(table=game_table)
  # p(game_table)

  term = Terminal()


  print(term.clear)
  draw_border(term)
  input()

  with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    key = ''
    while key.lower() != 'q':
      key = term.inkey(timeout=1)
      if key:
        print("key pressed: {0}".format(key))



    print(term.clear)

    print(term.move_xy(term.width//2 - (len(WINDOW_GOODBYE_TITLE)//2), term.height//2 - 1)+term.bold(f'{WINDOW_GOODBYE_TITLE}{term.normal}'))
    print(term.move_xy(term.width//2 - (len(WINDOW_GOODBYE_TEXT)//2), term.height//2 + 1)+term.bold(f'{WINDOW_GOODBYE_TEXT}{term.normal}'))
    term.inkey(timeout=3)
  # clear screen after end game
  print(term.clear)








# start app
if __name__ == "__main__":
    main()