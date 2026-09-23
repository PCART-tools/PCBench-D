@skip
def test_slicing_exhaustively():
    x = np.random.rand(6, 7, 8)
    a = da.from_array(x, chunks=(3, 3, 3))
    I = ReturnItem()

    # independent indexing along different axes
    indexers = [0, -2, I[:], I[:5], [0, 1], [0, 1, 2], [4, 2], I[::-1], None, I[:0], []]
    for i in indexers:
        assert_eq(x[i], a[i]), i
        for j in indexers:
            assert_eq(x[i][:, j], a[i][:, j]), (i, j)
            assert_eq(x[:, i][j], a[:, i][j]), (i, j)
            for k in indexers:
                assert_eq(x[..., i][:, j][k], a[..., i][:, j][k]), (i, j, k)

    # repeated indexing along the first axis
    first_indexers = [I[:], I[:5], np.arange(5), [3, 1, 4, 5, 0], np.arange(6) < 6]
    second_indexers = [0, -1, 3, I[:], I[:3], I[2:-1], [2, 4], [], I[:0]]
    for i in first_indexers:
        for j in second_indexers:
            assert_eq(x[i][j], a[i][j]), (i, j)
