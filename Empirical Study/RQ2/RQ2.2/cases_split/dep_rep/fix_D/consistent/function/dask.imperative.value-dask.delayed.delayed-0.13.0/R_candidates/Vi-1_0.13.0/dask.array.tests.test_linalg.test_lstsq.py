@pytest.mark.parametrize(("nrow", "ncol", "chunk"),
                         [(20, 10, 5), (100, 10, 10)])
def test_lstsq(nrow, ncol, chunk):
    np.random.seed(1)
    A = np.random.random_integers(1, 20, (nrow, ncol))
    b = np.random.random_integers(1, 20, nrow)

    dA = da.from_array(A, (chunk, ncol))
    db = da.from_array(b, chunk)

    x, r, rank, s = np.linalg.lstsq(A, b)
    dx, dr, drank, ds = da.linalg.lstsq(dA, db)

    assert_eq(dx, x)
    assert_eq(dr, r)
    assert drank.compute() == rank
    assert_eq(ds, s)

    # reduce rank causes multicollinearity, only compare rank
    A[:, 1] = A[:, 2]
    dA = da.from_array(A, (chunk, ncol))
    db = da.from_array(b, chunk)
    x, r, rank, s = np.linalg.lstsq(A, b)
    assert rank == ncol - 1
    dx, dr, drank, ds = da.linalg.lstsq(dA, db)
    assert drank.compute() == rank
