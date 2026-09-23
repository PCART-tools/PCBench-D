def random_rot(dim):
    """Return a random rotation matrix, drawn from the Haar distribution
    (the only uniform distribution on SO(n)).
    The algorithm is described in the paper
    Stewart, G.W., 'The efficient generation of random orthogonal
    matrices with an application to condition estimators', SIAM Journal
    on Numerical Analysis, 17(3), pp. 403-409, 1980.
    For more information see
    http://en.wikipedia.org/wiki/Orthogonal_matrix#Randomization"""
    H = eye(dim)
    D = ones((dim,))
    for n in range(1, dim):
        x = normal(size=(dim-n+1,))
        D[n-1] = sign(x[0])
        x[0] -= D[n-1]*sqrt((x*x).sum())
        # Householder transformation

        Hx = eye(dim-n+1) - 2.*outer(x, x)/(x*x).sum()
        mat = eye(dim)
        mat[n-1:,n-1:] = Hx
        H = dot(H, mat)
    # Fix the last sign such that the determinant is 1
    D[-1] = -D.prod()
    H = (D*H.T).T
    return H
