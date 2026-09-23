def test_solve():
    A = Matrix([[1,2], [2,4]])
    b = Matrix([[3], [4]])
    raises(ValueError, lambda: A.solve(b)) #no solution
    b = Matrix([[ 4], [8]])
    raises(ValueError, lambda: A.solve(b)) #infinite solution
