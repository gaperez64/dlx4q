class Cell:
    # We have rows, columns, a header row to which we keep pointers for
    # convenience, and weights (uniform per row).
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
    # A header cell has a column number and remembers the element of the set
    # it represents. It also has flags to know whether it is a soft target or
    # a cut, i.e. we want only to assert coverage and not enumerate covers.
    def __init__(self, c, e, soft=False, cut=False):
        self.elem = e
        self.above = self
        self.below = self
        self.right = None
        self.left = None
        self.col = c
        self.soft = soft
        self.cut = cut


class IncidenceMatrix:
    def __init__(self, target, cuttgt=[], sectgt=[]):
        self.target = target
        self.sectgt = sectgt
        self.cuttgt = cuttgt
        self.tgtset = set(target)
        self.secset = set(sectgt)
        self.cutset = set(cuttgt)
        self.root = self.header()
        self.nxtrow = 0

    def header(self):
        row = []
        # The order of enumeration is important! The algorithm assumes that
        # columns are given in the order: primary, cut, secondary columns
        for i, t in enumerate(self.target + self.cuttgt + self.sectgt):
            nxt = HeaderCell(i, t, soft=(t in self.secset),
                             cut=(t in self.cutset))
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
            if head.cut:
                headsec = "!"
            elif head.soft:
                headsec = "?"
            else:
                headsec = "."
            hdrset[head.col] = f"{head.elem}{headsec}"
            head = head.right
            if head == self.root:
                break
        while True:
            r = head.below
            while r != head:
                while len(rowsets) <= r.row:
                    rowsets.append(["-"] * len(self.target))
                rowsets[r.row][r.col] = "X "
                r = r.below
            if head.right == self.root:
                break
            else:
                head = head.right
        rowsets = [" ".join(hdrset)] + [" ".join(rs) for rs in rowsets]
        return "\n".join(rowsets)
