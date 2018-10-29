############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Qiyi Shan"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import collections


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
        self.board = {(r, c): {ele} if ele != 0 else {1, 2, 3, 4, 5, 6, 7, 8, 9}
                      for r, row in enumerate(board) for c, ele in enumerate(row)}

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
        return ({(r, c) for r in range(box_row * 3, box_row * 3 + 3) for c in range(box_col * 3, box_col * 3 + 3)} | \
                {(row, c) for c in range(9)} | {(r, col) for r in range(9)}) - {cell}

    def box(self, cell):
        row, col = cell
        box_row = row // 3
        box_col = col // 3
        return {(r, c) for r in range(box_row * 3, box_row * 3 + 3) for c in range(box_col * 3, box_col * 3 + 3)} - {
            cell}

    def row(self, cell):
        return {(cell[0], c) for c in range(9)} - {cell}

    def col(self, cell):
        return {(r, cell[1]) for r in range(9)} - {cell}

    def remove_extra_value(self, cell):
        for cells in [self.box(cell), self.row(cell), self.col(cell)]:
            for num in self.board[cell]:
                unique = True
                for test_cell in cells:
                    if num in self.board[test_cell]:
                        unique = False
                if unique:
                    self.board[cell] = {num}
                    for neighbor in self.neighbor(cell):
                        self.board[neighbor] -= {num}
                    return True
        return False

    def infer_ac3(self, arc_queue=None):
        if arc_queue:
            queue = arc_queue
        else:
            queue = collections.deque()
            for arc in Sudoku.ARCS:
                queue.append(arc)
        while len(queue) != 0:
            xi, xj = queue.popleft()
            if self.remove_inconsistent_values(xi, xj):
                for xk in self.neighbor(xi) - {xj}:
                    queue.append((xk, xi))

    def infer_improved(self):
        got_anything = True
        while got_anything:
            got_anything = False
            self.infer_ac3()
            # begin improve part
            for cell in Sudoku.CELLS:
                if len(self.board[cell]) > 1:
                    if self.remove_extra_value(cell):
                        got_anything = True

    def successors(self):
        min_suc_cell = min(self.board, key=lambda x: len(self.board[x]) if len(self.board[x]) > 1 else 100)
        # print "min_suc:", min_suc_cell
        for num in self.board[min_suc_cell]:
            new_board = KnownSudoku({(cell[0], cell[1]): {e for e in val} for cell, val in self.board.items()})
            # set the number at the cell
            new_board.board[min_suc_cell] = {num}
            for neig in new_board.neighbor(min_suc_cell):
                new_board.board[neig] -= {num}
            yield new_board

    def rec_infer(self):
        self.infer_improved()
        if self.conflict():
            return False
        if self.solved():
            return True
        for new_board in self.successors():
            if new_board.rec_infer():
                self.board = new_board.board
                return True

    def infer_with_guessing(self):
        self.rec_infer()

    def __str__(self):
        return self._simple_board()

    def _simple_board(self):
        return "\n".join(
            [" ".join([str(next(iter(self.board[(r, c)]))) if len(self.board[(r, c)]) == 1 else "_" for c in range(9)])
             for r in range(9)])

    def _detail_board(self):
        out = ""
        for r in range(9):
            for offset in range(0, 9, 3):
                for c in range(9):
                    nums = list(self.board[(r, c)])
                    out += " ".join(str(nums[i]) if i < len(nums) else " " for i in range(offset, offset + 3)) + "|"
                out += "\n"
            out += "-" * 53 + "\n"
        return out

    def solved(self):
        return all([True if len(nums) == 1 else False for nums in self.board.values()])

    def conflict(self):
        return any([True if len(nums) == 0 else False for nums in self.board.values()])


class KnownSudoku(Sudoku):

    def __init__(self, board):
        super(KnownSudoku, self).__init__([])
        self.board = board


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
12 hours
"""

feedback_question_2 = """
I made a lot of dumb mistakes during coding,the section that spent most of my time is infer_improved.
There are not extremely challenging part.
"""

feedback_question_3 = """
I like infer_with_guess.
"""
