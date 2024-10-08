from wxcover.wincmat import IncidenceMatrix
from wxcover.dlx import algox


def printNSolve(m):
    print(m)
    for sol in algox(m):
        print(f"Solution weight = {sol}")


mat = IncidenceMatrix([1, 2, 3, 4])
mat.addSet([1, 3])
mat.addSet([1, 2, 3])
mat.addSet([2, 4])
mat.addSet([4])
printNSolve(mat)

mat = IncidenceMatrix([1, 2, 3, 4, 5, 6, 7])
mat.addSet([1, 4, 7])
mat.addSet([1, 4])
mat.addSet([4, 5, 7])
mat.addSet([3, 5, 6])
mat.addSet([2, 3, 6, 7])
mat.addSet([2, 7])
printNSolve(mat)
