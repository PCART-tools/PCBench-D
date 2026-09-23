def test_eigh_of_sparse():
    # This tests the rejection of inputs that eigh cannot currently handle.
    import scipy.sparse
    a = scipy.sparse.identity(2).tocsc()
    b = np.atleast_2d(a)
    assert_raises(ValueError, eigh, a)
    assert_raises(ValueError, eigh, b)
