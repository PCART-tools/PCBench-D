def test_complex():
    def func(z):
        return z**2 - 1 + 2j
    x0 = 2.0j

    ftol = 1e-4
    sol = root(func, x0, tol=ftol, method='DF-SANE')

    assert_(sol.success)

    f0 = np.linalg.norm(func(x0))
    fx = np.linalg.norm(func(sol.x))
    assert_(fx <= ftol*f0)
