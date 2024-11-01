# from blessed import Terminal

# config:
TABLE_SIZE = 4

# funcs
def new_empty_table(table_size):
  table = [[0]*table_size]*table_size
  return table





def main():
  game_table = new_empty_table(TABLE_SIZE)
  print(game_table)





# start app
if __name__ == "__main__":
    main()