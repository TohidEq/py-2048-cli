# from blessed import Terminal

# config:
TABLE_SIZE = 4

# funcs
def new_empty_table(table_size):
  table = [[0]*table_size]*table_size
  return table


def get_empty_cells(table:list):
  empty_cells=[]

  rows = len(table)
  cols = len(table[0])

  # find empty cells and put them in empty_cells var
  for y in range(rows):
    for x in range(cols):
      if table[y][x]==0:
        empty_cells.append([y,x])

  return empty_cells




def main():
  game_table = new_empty_table(TABLE_SIZE)
  print(game_table)
  print(get_empty_cells(game_table))





# start app
if __name__ == "__main__":
    main()