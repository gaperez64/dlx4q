from wxcover.wincmat import IncidenceMatrix


mat = IncidenceMatrix([1, 2, 3 ,4])
mat.addSet([1, 3])
mat.addSet([1, 2, 3])
mat.addSet([2, 4])
print(mat)
