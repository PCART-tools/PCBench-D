def check_eigenvector(A, l, x):
    nx = np.linalg.norm(x)
    # Check zeroness.
    assert not nx == pytest.approx(0, abs=1e-7)
    y = A @ x
    ny = np.linalg.norm(y)
    # Check collinearity.
    assert x @ y == pytest.approx(nx * ny, abs=1e-7)
    # Check eigenvalue.
    assert ny == pytest.approx(l * nx, abs=1e-7)
