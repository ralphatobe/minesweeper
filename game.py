import numpy as np

class MinesweeperGame:
  def __init__(self, board_height, board_width, num_mines):
    # create board
    # board has two layers: the mine layer and the mask layer
    # create empty versions of these boards
    self.layer_mine = np.zeros((board_height, board_width), dtype=np.int)
    self.layer_mask = np.full((board_height, board_width), np.inf)

    # now we need to randomly generate the mine positions
    mine_positions = np.random.choice(board_height * board_width, num_mines, replace=False)

    # parse the mine positions into x and y coords
    mine_positions_y = np.empty((num_mines), dtype=np.int)
    mine_positions_x = np.empty((num_mines), dtype=np.int)
    for i, mine_position in enumerate(mine_positions):
      mine_positions_y[i] = int(mine_position / board_width)
      mine_positions_x[i] = int(mine_position % board_width)
      self.layer_mine[mine_positions_y[i], mine_positions_x[i]] = -1

    # Now we calculate all clues in advance
    for y, x in zip(mine_positions_y, mine_positions_x):
      for i in range(-1, 2):
        if y + i in range(board_height):
          for j in range(-1, 2):
            if x + j in range(board_width):
              self.layer_mine[y + i, x + j] += 1

    # and reset all true mine positions to -1
    for y, x in zip(mine_positions_y, mine_positions_x):
      self.layer_mine[y, x] = -1

    # we can now combine the two board layers to make the player board
    self.player_board = np.multiply(np.absolute(self.layer_mine), self.layer_mask)

    print(self.player_board)



if __name__ == "__main__":
  height = 2
  width = 3
  num_mines = 2

  MinesweeperGame(height, width, num_mines)