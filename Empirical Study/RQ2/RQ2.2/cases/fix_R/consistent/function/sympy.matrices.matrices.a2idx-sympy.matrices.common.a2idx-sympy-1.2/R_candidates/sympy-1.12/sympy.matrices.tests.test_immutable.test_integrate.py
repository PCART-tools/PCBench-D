def test_integrate():
    intIM = integrate(IM, x)
    assert intIM.shape == IM.shape
    assert all([intIM[i, j] == (1 + j + 3*i)*x for i, j in
                product(range(3), range(3))])
