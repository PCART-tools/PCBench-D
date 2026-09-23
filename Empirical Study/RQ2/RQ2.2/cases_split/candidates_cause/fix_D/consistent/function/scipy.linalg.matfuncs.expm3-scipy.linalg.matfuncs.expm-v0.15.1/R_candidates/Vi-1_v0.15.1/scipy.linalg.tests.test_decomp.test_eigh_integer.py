def test_eigh_integer():
    a = array([[1,2],[2,7]])
    b = array([[3,1],[1,5]])
    w,z = eigh(a)
    w,z = eigh(a,b)
