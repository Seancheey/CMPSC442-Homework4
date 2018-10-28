############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Qiyi Shan"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import collections, copy, itertools


############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    return [(r, c) for r in range(9) for c in range(9)]


def sudoku_arcs():
    return {((y, x1), (y, x2)) for y in range(9) for x1 in range(9) for x2 in range(9) if x1 != x2} | \
           {((y1, x), (y2, x)) for x in range(9) for y1 in range(9) for y2 in range(9) if y1 != y2} | \
           {((br * 3 + r1, bc * 3 + c1), (br * 3 + r2, bc * 3 + c2)) for br in range(3) for bc in range(3) for r1 in
            range(3) for c1 in range(3) for
            r2 in range(3) for c2 in range(3) if r1 != r2 or c1 != c2}


def read_board(path):
    with open(path) as f:
        sudoku = [[int(e) if e != "*" else 0 for e in line if e not in ("\r", "\n")] for line in f]
        return sudoku


class Sudoku(object):
    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    __slots__ = "board"

    def __init__(self, board):
        self.board = {(r, c): {ele} if ele != 0 else {1, 2, 3, 4, 5, 6, 7, 8, 9} for r, row in enumerate(board) for
                      c, ele
                      in enumerate(row)}

    # get the cell's box
    def box(self, row, col):
        box_row = row // 3
        box_col = col // 3
        for r in range(box_row * 3, box_row * 3 + 3):
            for c in range(box_col * 3, box_col * 3 + 3):
                yield self.board[r][c]

    def row(self, row):
        for c in range(9):
            yield self.board[row][c]

    def col(self, col):
        for r in range(9):
            yield self.board[r][col]

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        val1, val2 = self.get_values(cell1), self.get_values(cell2)
        if len(val2) == 1 and (cell1, cell2) in Sudoku.ARCS:
            if val2 <= self.board[cell1]:
                self.board[cell1] -= val2
                return True
        return False

    def neighbor(self, cell):
        row, col = cell
        box_row = row // 3
        box_col = col // 3
        return {(r, c) for r in range(box_row * 3, box_row * 3 + 3) for c in range(box_col * 3, box_col * 3 + 3)} | \
               {(row, c) for c in range(9)} | \
               {(r, col) for r in range(9)}

    def infer_ac3(self):
        queue = collections.deque()
        for arc in Sudoku.ARCS:
            queue.append(arc)
        while len(queue) != 0:
            xi, xj = queue.popleft()
            if self.remove_inconsistent_values(xi, xj):
                for xk in self.neighbor(xi) - {xj}:
                    queue.append((xk, xi))

    def infer_improved(self):
        pass

    def infer_with_guessing(self):
        pass

    def __str__(self):
        return "".join([str(next(iter(self.board[(r, c)]))) for r in range(9) for c in range(9)])


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
