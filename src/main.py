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

# numbers (y,x):(5,3)
NUMBERS = (
  [[1,1,1],
  [1,0,1],
  [1,0,1],
  [1,0,1],
  [1,1,1]],

  [[0,1,0],
  [0,1,0],
  [0,1,0],
  [0,1,0],
  [0,1,0]],

  [[1,1,1],
  [0,0,1],
  [1,1,1],
  [1,0,0],
  [1,1,1]],

  [[1,1,1],
  [0,0,1],
  [1,1,1],
  [0,0,1],
  [1,1,1]],

  [[1,0,1],
  [1,0,1],
  [1,1,1],
  [0,0,1],
  [0,0,1]],

  [[1,1,1],
  [1,0,0],
  [1,1,1],
  [0,0,1],
  [1,1,1]],

  [[1,1,1],
  [1,0,0],
  [1,1,1],
  [1,0,1],
  [1,1,1]],

  [[1,1,1],
  [0,0,1],
  [0,0,1],
  [0,0,1],
  [0,0,1]],

  [[1,1,1],
  [1,0,1],
  [1,1,1],
  [1,0,1],
  [1,1,1]],

  [[1,1,1],
  [1,0,1],
  [1,1,1],
  [0,0,1],
  [1,1,1]]
)

COLOR_EMPTY = (204, 192, 179);
COLOR_2 = (238, 228, 218);
COLOR_4 = (237, 224, 200);
COLOR_8 = (242, 177, 121);
COLOR_16 = (245, 149, 99);
COLOR_32 = (246, 124, 95);
COLOR_64 = (246, 94, 59);
COLOR_128 = (237, 207, 114);
COLOR_256 = (237, 204, 97);
COLOR_512 = (237, 200, 80);
COLOR_1024 = (237, 197, 63);
COLOR_2048 = (237, 194, 46);
COLOR_OTHER = (80, 80, 80);
COLORS = {"0":COLOR_EMPTY,
          "2":COLOR_2,
          "4":COLOR_4,
          "8":COLOR_8,
          "16":COLOR_16,
          "32":COLOR_32,
          "64":COLOR_64,
          "128":COLOR_128,
          "256":COLOR_256,
          "512":COLOR_512,
          "1024":COLOR_1024,
          "2048":COLOR_2048,
          "999999":COLOR_OTHER
          }
COLORS_FILL = {
  "2048":(0,0,0),
  "999999":(255,255,255),
}


# blessed confs
# - cells:
CELL_PADDING_Y = 1 # padding (top and bottom) cells
CELL_PADDING_X = 1 # padding (left and right) cells
CELL_GAP_Y = 1
CELL_GAP_X = 2
CELL_MAX_NUMBER_LENGTH = 6 # max numbers(length) in a cell
CELL_SIZE_Y = len(NUMBERS[0]) + (CELL_PADDING_Y * 2)
CELL_SIZE_x = (len(NUMBERS[0][0]) * CELL_MAX_NUMBER_LENGTH) + (CELL_PADDING_X * 2) + CELL_MAX_NUMBER_LENGTH
CELL_EMPTY_CHAR = "█" # zeroes in NUMBERS
CELL_FILL_CHAR = "█" # ones in NUMBERS
CELL_GAP_CHAR = "█" # between cells
# - window:
WINDOW_PADDING_Y = 1
WINDOW_PADDING_X = 2
WINDOW_BORDER_Y = 1
WINDOW_BORDER_X = 2
WINDOW_WALL_CHAR = "█"
WINDOW_WALL_COLOR = (153, 51, 0) # RGB
WINDOW_PADDING_CHAR = " "
WINDOW_SCORE_TEXT = "SCORE: "
WINDOW_SCORE_COLOR_FILL = (255,200,100)
WINDOW_SCORE_COLOR_BG = (0,0,0)
WINDOW_SCORE_POS_Y = 2
WINDOW_SCORE_POS_X = 6
WINDOW_GOODBYE_TITLE = "Goodbye :D"
WINDOW_GOODBYE_TEXT = "R: New Game | Other keys: exit now | Stay 6s: exit auto"


game_score = 0

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

def number_to_color_number(number,colors_dics):
  for key in list(colors_dics.keys()):
    if int(number) <= int(key):
      return key
  return list(colors_dics.keys())[-1]

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
  global game_score;
  new_table = copy.deepcopy(table)
  x = 0
  while(x < TABLE_SIZE):
    y = 0
    while(y < TABLE_SIZE - 1): # "-1": NO LAST CELL
      if new_table[y][x] != 0:# not empty
        if new_table[y][x] == new_table[y+1][x]:
          new_table[y][x] *= 2
          game_score+=new_table[y][x]
          new_table = move_col_top(new_table, y+1, x)
      y += 1
    x += 1
  return new_table

def sum_to_left(table:list):
  global game_score;
  new_table = copy.deepcopy(table)
  y = 0
  while(y < TABLE_SIZE):
    x = 0
    while(x < TABLE_SIZE - 1): # "-1": NO LAST CELL
      if new_table[y][x] != 0: # not empty
        if new_table[y][x] == new_table[y][x+1]:
          new_table[y][x] *= 2
          game_score+=new_table[y][x]
          new_table = move_row_left(new_table, y, x+1)
      x += 1
    y += 1
  return new_table

def sum_to_down(table:list):
  global game_score;
  new_table = copy.deepcopy(table)
  x = 0
  while(x < TABLE_SIZE):
    y = TABLE_SIZE - 1
    while(y > 0): # "> 0": NO FIRST CELL
      if new_table[y][x] != 0:# not empty
        if new_table[y][x] == new_table[y-1][x]:
          new_table[y][x] *= 2
          game_score+=new_table[y][x]
          new_table = move_col_down(new_table, y-1, x)
      y -= 1
    x += 1
  return new_table

def sum_to_right(table:list):
  global game_score;
  new_table = copy.deepcopy(table)
  y = 0
  while(y < TABLE_SIZE):
    x = TABLE_SIZE - 1
    while(x > 0): # "> 0": NO FIRST CELL
      if new_table[y][x] != 0: # not empty
        if new_table[y][x] == new_table[y][x-1]:
          new_table[y][x] *= 2
          game_score+=new_table[y][x]
          new_table = move_row_right(new_table, y, x-1)
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
  border_y = (WINDOW_WALL_CHAR * term.width)
  # text color
  color = term.color_rgb(WINDOW_WALL_COLOR[0],
                          WINDOW_WALL_COLOR[1],
                          WINDOW_WALL_COLOR[2])
  ## bg color
  # on_color = term.color_rgb(255 - WINDOW_WALL_COLOR[0],
  #                         255 - WINDOW_WALL_COLOR[1],
  #                         255 - WINDOW_WALL_COLOR[2])

  for y in range(WINDOW_BORDER_Y):
    # top border
    print(term.move_xy(0,y)+color+f'{border_y}{term.normal}',end='')
    # bottom border
    print(term.move_xy(0, term.height-1-y)+color+f'{border_y}{term.normal}',end='')

  border_x = (WINDOW_WALL_CHAR * WINDOW_BORDER_X)
  for y in range(term.height):
    # left border
    print(term.move_xy(0, y)+color+f'{border_x}{term.normal}',end='')
    # right border
    print(term.move_xy(term.width-WINDOW_BORDER_X, y)+color+f'{border_x}{term.normal}',end='')

def draw_empty_cell(term, y_pos, x_pos,color_number,custom=()):
  row = (CELL_EMPTY_CHAR*CELL_PADDING_X)+(CELL_EMPTY_CHAR*CELL_SIZE_x)+(CELL_EMPTY_CHAR*CELL_PADDING_X)
  col = CELL_SIZE_Y+(CELL_PADDING_Y*2)

  left_start = WINDOW_BORDER_X + WINDOW_PADDING_X +(x_pos*len(row))+(x_pos*CELL_GAP_X)
  top_start = WINDOW_BORDER_Y + WINDOW_PADDING_Y +(y_pos*col)+(y_pos*CELL_GAP_Y)

  color_number = number_to_color_number(number=color_number,colors_dics=COLORS)
  color = term.color_rgb(COLORS[color_number][0], COLORS[color_number][1], COLORS[color_number][2])
  if custom != () :
    color = term.color_rgb(custom[0],custom[1],custom[2])
  for y in range(col):
    print(term.move_xy(x=left_start+0, y=top_start+y)+ color+ (row)+ term.normal)

def draw_empty_table(term,table):
  for y in range(TABLE_SIZE):
    for x in range(TABLE_SIZE):
      draw_empty_cell(term=term,y_pos=y,x_pos=x,color_number=str(table[y][x]))

def draw_number_in_cell(term, number, cell_pos_y, cell_pos_x,custom=()):
  number_length = len(str(number))*len(NUMBERS[0][0])

  if(number>=10):
    # add gaps between numbers to number_length
    number_length += len(str(number))

  # row text
  row = (CELL_EMPTY_CHAR*CELL_PADDING_X)+(CELL_EMPTY_CHAR*CELL_SIZE_x)+(CELL_EMPTY_CHAR*CELL_PADDING_X)

  # col number length
  col = CELL_SIZE_Y+(CELL_PADDING_Y*2)

  left_start = WINDOW_BORDER_X + WINDOW_PADDING_X +(cell_pos_x*len(row))+(cell_pos_x*CELL_GAP_X)+CELL_PADDING_X

  if (len(row)>number_length+len(NUMBERS[0][0])):
    delta = len(row) - number_length

    left_start = left_start + delta//2 - len(NUMBERS[0][0])//2

  top_start = WINDOW_BORDER_Y + WINDOW_PADDING_Y +(cell_pos_y*col)+(cell_pos_y*CELL_GAP_Y)+CELL_PADDING_Y*2

  color_number_fill = number_to_color_number(number=(number),colors_dics=COLORS_FILL)

  color_fill = term.color_rgb(COLORS_FILL[color_number_fill][0], COLORS_FILL[color_number_fill][1], COLORS_FILL[color_number_fill][2])
  if custom != ():
    color_fill = term.color_rgb(custom[0],custom[1],custom[2])


  for i in str(number):
    num_index = int(i)
    num_arr = NUMBERS[num_index]
    for y in range(len(num_arr)):
      for x in range(len(num_arr[0])):
        if num_arr[y][x]==1:
          print(term.move_xy(x=left_start+x, y=top_start+y)
                + color_fill
                + CELL_FILL_CHAR
                + term.normal)
    left_start += len(NUMBERS[0][0])+1

def draw_table(term,table):
  draw_empty_table(term=term,table=table)

  for y in range(TABLE_SIZE):
    for x in range(TABLE_SIZE):
      number = table[y][x]
      if(number != 0):
        draw_number_in_cell(term=term,number=number,cell_pos_y=y,cell_pos_x=x)

def draw_score_simple(term):
  global game_score;
  width = CELL_SIZE_x*TABLE_SIZE + (TABLE_SIZE*2)
  text = f"{WINDOW_SCORE_TEXT}{game_score}"
  pos_y = CELL_SIZE_Y*(TABLE_SIZE+1) + (TABLE_SIZE+1) +1 +WINDOW_BORDER_Y
  pos_x = WINDOW_SCORE_POS_X + (width-len(text))//2

  color_fill = term.color_rgb(
                              WINDOW_SCORE_COLOR_FILL[0],
                              WINDOW_SCORE_COLOR_FILL[1],
                              WINDOW_SCORE_COLOR_FILL[2])

  #clear
  print(term.move_xy(x=pos_x, y=pos_y)
                + color_fill
                + (" "*(len(text)+10))
                + term.normal)
  #print
  print(term.move_xy(x=pos_x, y=pos_y)
                + color_fill
                + term.bold
                + text
                + term.normal)


def draw_score_cell_style(term):
  draw_empty_cell(term=term,x_pos=TABLE_SIZE,y_pos=0,color_number=0,custom=WINDOW_SCORE_COLOR_BG)
  draw_number_in_cell(term,game_score,cell_pos_x=TABLE_SIZE,cell_pos_y=0,custom=WINDOW_SCORE_COLOR_FILL)


def draw_score(term):
  width = (CELL_SIZE_x * (TABLE_SIZE+1)) + (TABLE_SIZE+2+2)*2 + WINDOW_PADDING_X*2 + WINDOW_BORDER_X*2
  if term.width<width:
    draw_score_simple(term=term)
  else:
    draw_score_cell_style(term)





def new_game():
  global game_score
  game_score = 0
  table = new_empty_table(TABLE_SIZE)
  table = add_next_number(table=table)
  table = add_next_number(table=table)
  return table



def main():
  game_table = new_game()
  # p(game_table)

  term = Terminal()


  print(term.clear)
  # draw_border(term)
  # draw_table(term=term, table=game_table)
  # input()

  with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    exit = False
    while exit != True:
      draw_border(term)
      key = ''
      while key.lower() != 'q':
        draw_table(term=term, table=game_table)
        draw_score(term=term)

        key = term.inkey(timeout=10)
        if key:
          # print("key pressed: {0}".format(key))
          # move_table
          key = key.upper()
          if key in KEYS_MOVES:
            game_table=move_table(table=game_table, move=KEYS_MOVES[key])




      print(term.clear)

      print(term.move_xy(term.width//2 - (len(WINDOW_GOODBYE_TITLE)//2), term.height//2 - 1)+term.bold(f'{WINDOW_GOODBYE_TITLE}{term.normal}'))
      print(term.move_xy(term.width//2 - (len(WINDOW_GOODBYE_TEXT)//2), term.height//2 + 1)+term.bold(f'{WINDOW_GOODBYE_TEXT}{term.normal}'))

      exit = True
      if term.inkey(timeout=6).lower()=="r":

        key = ""
        game_table = new_game()
        exit = False
        print(term.clear)


    # clear screen after end game
    print(term.clear)








# start app
if __name__ == "__main__":
    main()