import numpy as np

class MinesweeperGame:

  def __init__(self, board_height, board_width, num_mines):
    # store parameters
    self.board_height = board_height
    self.board_width = board_width
    self.num_mines = num_mines
    # create board
    # board has two layers: the mine layer and the mask layer
    # create empty versions of these boards
    self.layer_mine = np.zeros((self.board_height, self.board_width), dtype=np.int)
    self.layer_mask = np.zeros((self.board_height, self.board_width), dtype=np.int)

    # now we need to randomly generate the mine positions
    mine_positions = np.random.choice(self.board_height * self.board_width, self.num_mines, replace=False)

    # parse the mine positions into x and y coords
    mine_positions_y = mine_positions / self.board_width
    mine_positions_x = mine_positions % self.board_width
    mine_positions_y = mine_positions_y.astype(int)
    mine_positions_x = mine_positions_x.astype(int)

    # Now we calculate all clues in advance
    for y, x in zip(mine_positions_y, mine_positions_x):
      for i in [-1, 0, 1]:
        if y + i in range(self.board_height):
          for j in [-1, 0, 1]:
            if x + j in range(self.board_width):
              self.layer_mine[y + i, x + j] += 1

    # and reset all true mine positions to -1
    for y, x in zip(mine_positions_y, mine_positions_x):
      self.layer_mine[y, x] = -1

    # construct player view
    self.player_board = np.full((self.board_height, self.board_width), -1, dtype=np.int)
    print(self.player_board)

    # start the game
    self.run()

  def run(self):
    # iterate until a win or loss condition is triggered
    while True:
      x, y, flag = self.check_input()
      if flag:
        self.flag_block(x, y)
      else:
        self.select_block(x, y)
      self.win_condition()


  def check_input(self):
    # keep asking until a valid input is given
    while True:
      text = input("Select or Flag coordinate ([F] x, y): ")
      flag = False
      try:
        if text[0] == "F":
          text = text[1:]
          flag = True
        x, y = text.split(",")
        x = int(x.strip())
        y = int(y.strip()) 
        if 0 <= x and x < self.board_width and 0 <= y and y < self.board_height:
          break
      except Exception as e:
        pass
      print("Invalid input")
    return x, y, flag


  def flag_block(self, x, y):
    if self.player_board[y, x] == -2:
      # unflag tile and update
      self.player_board[y, x] = -1
      self.update_viewer()
    else:
      # flag tile
      self.player_board[y, x] = -2
      print(self.player_board)



  def select_block(self, x, y):
    if self.layer_mine[y, x] != -1:
      # unmask tile
      self.layer_mask[y, x] = 1
      # check if other tiles were unmasked
      self.recurse(y, x)
      # check the win conditions
      self.win_condition()
      # update user's view
      self.update_viewer()
    else:
      # a mine was selected
      print("You lose!")
      exit()


  def recurse(self, y, x):
    # recursively reveal tiles until hints are found
    if self.layer_mine[y, x] == 0:
      for i in [-1, 0, 1]:
        if y + i in range(self.board_height):
          for j in [-1, 0, 1]:
            if x + j in range(self.board_width):
              if self.layer_mask[y + i, x + j] == 0:
                self.layer_mask[y + i, x + j] = 1
                self.recurse(y + i, x + j)


  def win_condition(self):
    # check if all non-mine tiles are revealed or all mine tiles are flagged
    if np.sum(self.layer_mask) == (self.board_height * self.board_width) - self.num_mines or \
       (np.where(self.player_board == -2)[0].shape == np.where(self.layer_mine == -1)[0].shape and \
       np.equal(np.where(self.player_board == -2), np.where(self.layer_mine == -1)).all()):
      print("\n", self.layer_mine)
      print("You win!")
      exit()


  def update_viewer(self):
    # update player board to show what has been unmasked
    for y in range(self.board_height):
      for x in range(self.board_width):
        if self.layer_mask[y, x] == 1:
          self.player_board[y, x] = self.layer_mine[y, x]
    print(self.player_board)



if __name__ == "__main__":
  # prompt user for necessary game parameters
  height = int(input("Please input board height: "))
  width = int(input("Please input board width: "))
  num_mines = int(input("Please input number of mines: "))

  MG = MinesweeperGame(height, width, num_mines)