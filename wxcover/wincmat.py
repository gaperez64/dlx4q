class Cell:
    def __init__(self, r, c, w):
        self.weight = w
        self.above = None
        self.below = None
        self.right = None
        self.left = None
        self.row = r
        self.col = c

    def wrapLeft(self, other):
        other.right = self
        self.left = other

    def wrapUp(self, other):
        other.below = self
        self.above = other


class HeaderCell(Cell):
    def __init__(self, e):
        self.elem = e
        self.above = self
        self.below = self
        self.right = None
        self.left = None


class IncidenceMatrix:
    def __init__(self, target):
        self.target = target
        self.tgtset = set(target)
        self.matrix = [self.header()]

    def header(self):
        row = []
        for t in self.target:
            nxt = HeaderCell(t)
            if len(row) > 0:
                nxt.wrapLeft(row[-1])
            row.append(nxt)
        row[0].wrapLeft(row[-1])
        return row

    def addSet(self, s, w):
        assert s <= self.tgtset
        row = []
        for e in s:
            idx = self.target.index(e)
            nxt = Cell(len(row), idx, w)
            head = self.matrix[0][idx]
            nxt.wrapUp(head.above)
            head.wrapUp(nxt)
            if len(row) > 0:
                nxt.wrapLeft(row[-1])
            row.append(nxt)
        row[0].wrapLeft(row[-1])
        return row

    def __str__(self):
        rowsets = ""
        for r in self.matrix[1:]:
            rowsets.append(set())
            c = r
            elems = []
            while True:
                elems.append(self.target[c.col])
                if c.right == r:
                    break
                else:
                    c = c.right
            rowsets += f"{elems}\n"
        return f"Target={self.target}\n"\
               f"{rowsets}"
