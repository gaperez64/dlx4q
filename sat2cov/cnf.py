from wxcover.wincmat import IncidenceMatrix


class CNF:
    def __init__(self, maxvar=0):
        self.maxvar = maxvar
        self.clauses = []

    # 0 not allowed as id, and negatives are negative literals
    def addClause(self, clause):
        m = max(clause)
        self.maxvar = max(self.maxvar, m)
        assert all([x != 0 for x in clause])
        self.clauses.append(clause)

    # this implements the reduction given in
    # https://cs.stackexchange.com/questions/118054/how-to-prove-that-exact-cover-is-np-complete-using-sat
    def toXCover(self):
        varsets = [f"x{i}" for i in range(1, self.maxvar + 1)]
        clausesets = [f"C{i}" for i, _ in enumerate(self.clauses)]
        occursets = [f"p{i},{j}" for i in range(1, self.maxvar + 1)
                     for j, c in enumerate(self.clauses)
                     if i in c or -i in c]
        print(occursets)
        target = varsets + clausesets + occursets
        mat = IncidenceMatrix(target)

        # For every variable xi we create two sets
        # 1) it contains xi with pij for every clause j where i appears
        # negatively
        # 2) it contains xi with pij for every clause j where i appears
        # positively
        # In addition, for every element pij, we create a singleton {pij}
        # and a pair {Cj, pij}
        for i in range(1, self.maxvar + 1):
            trueset = [f"x{i}"]
            falseset = [f"x{i}"]
            for j, c in enumerate(self.clauses):
                if -i in c:
                    trueset.append(f"p{i},{j}")
                if i in c:
                    falseset.append(f"p{i},{j}")
                mat.addSet(["p{i},{j}"])
                mat.addSet(["C{j}", "p{i},{j}"])
            mat.addSet(trueset)
            mat.addSet(falseset)
        return mat
