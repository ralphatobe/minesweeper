import scipy as scipy
import random
import numpy as np


class MinesweeperGame(object):

	def __init__(self, board_size, num_mines):
		
		self.board_size = board_size
		self.num_mines = num_mines

		mine_indices = random.sample(range(board_size**2), num_mines)
		mine_indices = np.asarray(mine_indices)

		mine_x = mine_indices/board_size
		mine_y = mine_indices%board_size

		self.bottom_board = np.zeros([board_size, board_size], dtype=int)
		self.middle_board = np.zeros([board_size, board_size], dtype=int)
		self.top_board = np.zeros([board_size, board_size], dtype=int)
		
		self.viewer_board = np.ones([board_size, board_size], dtype=int) * -1

		for x, y in zip(mine_x, mine_y):
			self.bottom_board[x][y] = 1

			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					if x + i >= 0 and x + i < board_size and  \
					   y + j >= 0 and y + j < board_size and  \
					   not(x == 0 and y == 0):
					    self.middle_board[x + i][y + j] += 1

		for x, y in zip(mine_x, mine_y):
			self.middle_board[x][y] = -1

		print(self.viewer_board)


	def select_block(self, x, y):
		if self.bottom_board[x][y] == 0:
			self.top_board[x][y] = 1
			self.recurse(x, y)

		self.update_viewer()
		print(self.viewer_board)


	def recurse(self, x, y):
		if self.middle_board[x][y] == 0:
			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					if x + i >= 0 and x + i < self.board_size and  \
					   y + j >= 0 and y + j < self.board_size and  \
					   self.top_board[x + i][y + j] == 0:
					    self.top_board[x + i][y + j] = 1
					    self.recurse(x + i, y + j)

	def update_viewer(self):
		for x, y in zip(range(self.board_size), range(self.board_size)):
			if self.top_board[x][y] == 1:
				self.viewer_board[x][y] = self.middle_board[x][y]

MG = MinesweeperGame(6, 5)
MG.select_block(2, 2)
MG.select_block(4, 5)