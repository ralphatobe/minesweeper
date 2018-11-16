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
    self.layer_mask = np.full((self.board_height, self.board_width), -1, dtype=np.int)

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

    self.player_board = np.full((self.board_height, self.board_width), -1, dtype=np.int)
    print(self.player_board)


  def select_block(self, x, y):
    if self.layer_mine[y, x] != -1:
      self.layer_mask[y, x] = 1
      self.recurse(y, x)
      self.win_condition()
      self.update_viewer()
    else:
      print("You lose!")
      exit()


  def recurse(self, y, x):
    if self.layer_mine[y, x] == 0:
      for i in [-1, 0, 1]:
        if y + i in range(self.board_height):
          for j in [-1, 0, 1]:
            if x + j in range(self.board_width):
              if self.layer_mask[y + i, x + j] == -1:
                self.layer_mask[y + i, x + j] = 1
                self.recurse(y + i, x + j)


  def win_condition(self):
    if np.sum(self.layer_mask) == self.num_mines:
      print("You win!")
      exit()


  def update_viewer(self):
    for y in range(self.board_height):
      for x in range(self.board_width):
        if self.layer_mask[y, x] == 1:
          self.player_board[y, x] = self.layer_mine[y, x]
    print(self.player_board)



if __name__ == "__main__":
  height = 6
  width = 5
  num_mines = 5

  MG = MinesweeperGame(height, width, num_mines)
  MG.select_block(1, 0)
  MG.select_block(2, 1)