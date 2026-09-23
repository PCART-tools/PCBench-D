def F3(x):
    A = np.mat('-2 1 0; 1 -2 1; 0 1 -2')
    b = np.mat('1 2 3')
    return np.dot(A, x) - b
