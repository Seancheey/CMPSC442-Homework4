from qxs20 import *

b = read_board("sudoku/hw4-medium1.txt")
print Sudoku(b)
print Sudoku(b).get_values((0, 1))

print sudoku_cells()
