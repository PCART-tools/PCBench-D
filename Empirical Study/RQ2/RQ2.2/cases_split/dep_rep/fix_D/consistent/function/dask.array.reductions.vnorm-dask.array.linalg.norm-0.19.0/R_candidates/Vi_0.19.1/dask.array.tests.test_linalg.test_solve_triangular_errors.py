def test_solve_triangular_errors():
    A = np.random.randint(0, 10, (10, 10, 10))
    b = np.random.randint(1, 10, 10)
    dA = da.from_array(A, chunks=(5, 5, 5))
    db = da.from_array(b, chunks=5)
    pytest.raises(ValueError, lambda: da.linalg.solve_triangular(dA, db))

    A = np.random.randint(0, 10, (10, 10))
    b = np.random.randint(1, 10, 10)
    dA = da.from_array(A, chunks=(3, 3))
    db = da.from_array(b, chunks=5)
    pytest.raises(ValueError, lambda: da.linalg.solve_triangular(dA, db))
