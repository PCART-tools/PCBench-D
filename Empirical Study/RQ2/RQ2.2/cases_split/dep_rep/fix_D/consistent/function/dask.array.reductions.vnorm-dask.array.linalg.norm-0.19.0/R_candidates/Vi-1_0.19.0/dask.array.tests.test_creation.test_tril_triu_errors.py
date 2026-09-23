def test_tril_triu_errors():
    A = np.random.randint(0, 11, (10, 10, 10))
    dA = da.from_array(A, chunks=(5, 5, 5))
    pytest.raises(ValueError, lambda: da.triu(dA))
