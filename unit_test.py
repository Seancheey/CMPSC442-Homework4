from qxs20 import *
import time


def timeit(func):
    def wrapper(self):
        t1 = time.time()
        func(self)
        print "time:", time.time() - t1, "\n"

    return wrapper


@timeit
def test(path):
    print(path)
    b = read_board(path)
    Sudoku(b).infer_with_guessing()


def stat(board):
    print("solve ratio: %.2f%%" % (
            sum([1 for r in range(9) for c in range(9) if len(board.board[(r, c)]) == 1]) / 0.81))


def classic_test():
    test("sudoku/hw4-easy.txt")
    test("sudoku/hw4-medium1.txt")
    test("sudoku/hw4-medium2.txt")
    test("sudoku/hw4-medium3.txt")
    test("sudoku/hw4-medium4.txt")
    test("sudoku/hw4-hard1.txt")
    test("sudoku/hw4-hard2.txt")
    test("sudoku/tester.txt")


def correctness_test():
    b = read_board("sudoku/hw4-medium3.txt")
    s = Sudoku(b)
    c = (1, 1)
    assert (s.box(c) | s.row(c) | s.col(c)) == s.neighbor(c)
    s.infer_ac3()
    print s
    print s._detail_board()
    s.infer_improved()
    print s


if __name__ == "__main__":
    classic_test()
