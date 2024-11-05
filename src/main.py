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



def move_col_top(table,y,x):
  new_table = table;
  for i in range(y, TABLE_SIZE-1):
    new_table[i][x] = table[i+1][x]
  new_table[TABLE_SIZE-1][x]=0;
  return new_table

def move_row_left(table,y,x):
  new_table = table;
  for i in range(x, TABLE_SIZE-1):
    new_table[y][i] = table[y][i+1]
  new_table[y][TABLE_SIZE-1]=0;
  return new_table

def move_col_down(table,y,x):
  new_table = table;
  for i in range(y, 0, -1): # "-1" -> reversed
    new_table[i][x] = table[i-1][x]
  new_table[0][x]=0;
  return new_table


def move_row_right(table,y,x):
  new_table = table;
  for i in range(x, 0, -1): # "-1" -> reversed
    new_table[y][i] = table[y][i-1]
  new_table[y][0]=0;
  return new_table




def move_table(table:list, move:str):
  # move = top, left, down, right
  table
  empty_cells = get_empty_cells(table)
  # sort a row:
  match move:
    case "top":
      print("move to the top")

    case "left":
      print("move to the left")

    case "down":
      print("move to the down")

    case "right":
      print("move to the right")

      # way one:
      # for y in range(0, TABLE_SIZE):
      #   for x in range(TABLE_SIZE-1, 0, -1): # -1 : reversed
      #     if table[y][x]==0:
      #       print("move row to right")
      #       table=move_row_right(table, y, x)
      #       print(table)

      # way two:
      for empty_cell in empty_cells:
        if empty_cell["x"] != 0:
          table = move_row_right(table, empty_cell["y"], empty_cell["x"])

    case _:
      print("incorrect move")


  return table;




def main():
  # game_table = new_empty_table(TABLE_SIZE)
  # print(game_table)
  # print(get_empty_cells(game_table))
  # print(get_random_cell(get_empty_cells(game_table)))

  test_table = [[0, 6, 0, 5],
                [0, 1, 0, 2],
                [0, 2, 3, 0],
                [0, 3, 4, 0]]

  print(test_table)
  print("----")
  table = move_table(test_table,"right")
  print("----")
  print(test_table)

  # print(move_row_right(test_table,0,2))
  # print(move_row_left(test_table,0,0))
  # print(move_col_top(test_table,2,1))
  # print(move_col_down(test_table,2,1))






# start app
if __name__ == "__main__":
    main()