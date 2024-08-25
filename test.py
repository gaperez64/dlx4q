from wxcover.wincmat import IncidenceMatrix


mat = IncidenceMatrix([1, 2, 3, 4])
mat.addSet([1, 3])
mat.addSet([1, 2, 3])
mat.addSet([2, 4])
print(repr(mat))
print(mat)

mat = IncidenceMatrix([1, 2, 3, 4, 5, 6, 7])
mat.addSet([1, 4, 7])
mat.addSet([1, 4])
mat.addSet([4, 5, 7])
mat.addSet([3, 5, 6])
mat.addSet([2, 3, 6, 7])
mat.addSet([2, 7])
print(repr(mat))
print(mat)
