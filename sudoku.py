#!/usr/bin/python

import math
import sys

def create2d(n):
    """ Create 2d array """
    ar = lambda n : [0] * n
    return list([ar(n) for i in range(n)])

class Sudoku(object):
    """
    Class which represents a sudoku object
    """
    def __init__(self, n):
        self.board = create2d(n)

    @property
    def n(self):
        """ Returns length of sudoku board """
        return len(self.board)

    @property
    def sn(self):
        """ Returns length of a box of sudoku board (i.e. 3 for 9x9 sudoku)"""
        return math.ceil(math.sqrt(self.n))

    def __str__(self):
        n = self.n
        sn = self.sn
        dg = int(1 + math.log(n, 10))
        fmt = "%%%dd" % dg
        tostr = lambda ar: ' '.join([ (fmt % i) for i in ar])
        slice = lambda ar, n: '|'.join([tostr(ar[i*n:(i+1)*n]) for i in range(n)])
        arr = [slice(s, sn) for s in self.board]
        arr = ['\n'.join(arr[i*sn:(i+1)*sn]) for i in range(sn)]
        return ('\n%s\n' % ('-' * ((dg + 1) * n))).join(arr)


    def genRow(self, row):
        for c in range(self.n):
            yield self.board[row][c]

    def genCol(self, col):
        for r in range(self.n):
            yield self.board[r][col]

    def genBox(self, row, col):
        sn = self.sn
        sr = sn * math.floor(row / sn)
        sc = sn * math.floor(col / sn)
        for r in range(sn):
            for c in range(sn):
                yield self.board[sr + r][sc + c]

    def genAll(self, row, col):
        for i in self.genRow(row):
            yield i
        for i in self.genCol(col):
            yield i
        for i in self.genBox(row, col):
            yield i

    def canBe(self, row, col, val):
        """ Tests whether a 'val' value can be in a 'row' 'col' position """
        for v in self.genAll(row, col):
            if v == val:
                return False
        return True

    def getPossibilities(self, r, c):
        """ Return a list of possible value for 'r' 'c' cell """
        g = []
        for i in range(1, self.n + 1):
            if self.canBe(r, c, i):
                g.append(i)
        return g


    def solve(self):
        """ Solve sudoku puzzle """
        smallest = None
        for r in range(self.n):
            for c in range(self.n):
                if self.board[r][c] != 0:
                    continue
                g = self.getPossibilities(r, c)
                if not smallest or len(smallest[0]) > len(g):
                    smallest = [g, (r, c)]
        if not smallest:
            return True
        r, c = smallest[1]
        for v in smallest[0]:
            self.set(r, c, v)
            if self.solve():
                return True
            self.set(r, c, 0)
        return False


    def set(self, row, col, val):
        self.board[row][col] = val

    def verify(self):
        """ Verify that sudoku is solved """
        n = self.n
        expected = list(range(1, 1 + n))
        check = lambda l: sorted(l) != expected
        for r in range(n):
            for c in range(n):
                if check(self.genRow(r)):
                    return False
                if check(self.genCol(c)):
                    return False
                if check(self.genBox(r, c)):
                    return False
        return True


def sudokuRead(fname):
    """
    Parse sudoku puzzle
    """
    s = None
    r = 0
    for line in open(fname):
        line = line.rstrip('\n');
        if not s:
            s = Sudoku(len(line.split(',')))
        c = 0
        for i in line.split(','):
            s.set(r, c, int(i))
            c += 1
        r += 1
    return s

def solve(fname):
    """
    Solve a sudoku puzzle from a file
    """ 
    s = sudokuRead(fname)
    print(s)
    if s.solve() and s.verify():
        print("Solution found!")
        print(s)
    else:
        print("Puzzle is unsolvable")


if __name__=="__main__":
    for fname in sys.argv[1:]:
        solve(fname)
