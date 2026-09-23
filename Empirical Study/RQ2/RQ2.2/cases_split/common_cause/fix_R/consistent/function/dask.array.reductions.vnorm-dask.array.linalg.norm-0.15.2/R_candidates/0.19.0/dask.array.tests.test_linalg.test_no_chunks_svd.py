def test_no_chunks_svd():
    x = np.random.random((100, 10))
    u, s, v = np.linalg.svd(x, full_matrices=0)

    for chunks in [((np.nan,) * 10, (10,)),
                   ((np.nan,) * 10, (np.nan,))]:
        dx = da.from_array(x, chunks=(10, 10))
        dx._chunks = chunks

        du, ds, dv = da.linalg.svd(dx)

        assert_eq(s, ds)
        assert_eq(u.dot(np.diag(s)).dot(v),
                  du.dot(da.diag(ds)).dot(dv))
        assert_eq(du.T.dot(du), np.eye(10))
        assert_eq(dv.T.dot(dv), np.eye(10))

        dx = da.from_array(x, chunks=(10, 10))
        dx._chunks = ((np.nan,) * 10, (np.nan,))
        assert_eq(abs(v), abs(dv))
        assert_eq(abs(u), abs(du))
