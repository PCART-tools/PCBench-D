def F(x):
    x = np.asmatrix(x).T
    d = matrix(diag([3,2,1.5,1,0.5]))
    c = 0.01
    f = -d*x - c*float(x.T*x)*x
    return f
