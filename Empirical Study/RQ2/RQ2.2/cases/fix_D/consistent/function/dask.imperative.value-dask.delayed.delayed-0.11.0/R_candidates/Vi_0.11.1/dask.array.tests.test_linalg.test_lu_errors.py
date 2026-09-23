def test_lu_errors():
    A = np.random.random_integers(0, 10, (10, 10, 10))
    dA = da.from_array(A, chunks=(5, 5, 5))
    assert raises(ValueError, lambda: da.linalg.lu(dA))

    A = np.random.random_integers(0, 10, (10, 8))
    dA = da.from_array(A, chunks=(5, 4))
    assert raises(ValueError, lambda: da.linalg.lu(dA))

    A = np.random.random_integers(0, 10, (20, 20))
    dA = da.from_array(A, chunks=(5, 4))
    assert raises(ValueError, lambda: da.linalg.lu(dA))
