def test_one_chunk_along_axis():
    a = np.arange(2 * 9).reshape(2, 9)
    darr = da.from_array(a, chunks=((2,), (2, 2, 2, 3)))
    g = overlap(darr, depth=0, boundary=0)
    assert a.shape == g.shape
