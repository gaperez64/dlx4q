class Cell:
    def __init__(self, r, c, h, w):
        self.weight = w
        self.above = None
        self.below = None
        self.right = None
        self.left = None
        self.row = r
        self.col = c
        self.head = h

    def wrapLeft(self, other):
        other.right = self
        self.left = other

    def wrapUp(self, other):
        other.below = self
        self.above = other

    def __repr__(self):
        return f"(row={self.row}, col={self.col})"


class HeaderCell(Cell):
    def __init__(self, c, e):
        self.elem = e
        self.above = self
        self.below = self
        self.right = None
        self.left = None
        self.col = c


class IncidenceMatrix:
    def __init__(self, target):
        self.target = target
        self.tgtset = set(target)
        self.root = self.header()
        self.nxtrow = 0

    def header(self):
        row = []
        for i, t in enumerate(self.target):
            nxt = HeaderCell(i, t)
            if len(row) > 0:
                nxt.wrapLeft(row[-1])
            row.append(nxt)
        row[0].wrapLeft(row[-1])
        return row[0]

    def addSet(self, s, w=1):
        s = set(s)
        assert s <= self.tgtset
        row = []
        for e in s:
            # find index of column
            idx = self.target.index(e)
            # find the actual column header in list
            head = self.root
            for _ in range(idx):
                head = head.right
            # create the new cell
            nxt = Cell(self.nxtrow, idx, head, w)
            # make all cardinal links
            nxt.wrapUp(head.above)
            head.wrapUp(nxt)
            if len(row) > 0:
                nxt.wrapLeft(row[-1])
            row.append(nxt)
        row[0].wrapLeft(row[-1])

        # NOTE: remember to update the next free row index!
        self.nxtrow += 1
        return row[0]

    def __repr__(self):
        rowsets = []
        head = self.root
        hdrset = ["-" for _ in self.target]
        while True:
            hdrset[head.col] = str(head.elem)
            head = head.right
            if head == self.root:
                break
        while True:
            r = head.below
            while r != head:
                while len(rowsets) <= r.row:
                    rowsets.append(["-"] * len(self.target))
                rowsets[r.row][r.col] = "X"
                r = r.below
            if head.right == self.root:
                break
            else:
                head = head.right
        rowsets = [" ".join(hdrset)] + [" ".join(rs) for rs in rowsets]
        return "\n".join(rowsets)

    def __str__(self):
        rowsets = dict()
        head = self.root
        while True:
            r = head.below
            while r != head:
                if r.row not in rowsets:
                    rowsets[r.row] = []
                rowsets[r.row].append(self.target[r.col])
                r = r.below
            if head.right == self.root:
                break
            else:
                head = head.right
        rowsets = [str(rs) for rs in rowsets.values()]
        rowsets = "\n".join(rowsets)
        return f"Target={self.target}\n"\
               f"{rowsets}"
