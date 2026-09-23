def test_point_slicing_with_full_slice():
    from dask.array.core import _vindex_transpose, _get_axis
    x = np.arange(4 * 5 * 6 * 7).reshape((4, 5, 6, 7))
    d = da.from_array(x, chunks=(2, 3, 3, 4))

    inds = [[[1, 2, 3], None, [3, 2, 1], [5, 3, 4]],
            [[1, 2, 3], None, [4, 3, 2], None],
            [[1, 2, 3], [3, 2, 1]],
            [[1, 2, 3], [3, 2, 1], [3, 2, 1], [5, 3, 4]],
            [[], [], [], None],
            [np.array([1, 2, 3]), None, np.array([4, 3, 2]), None],
            [None, None, [1, 2, 3], [4, 3, 2]],
            [None, [0, 2, 3], None, [0, 3, 2]]]

    for ind in inds:
        slc = [i if isinstance(i, (np.ndarray, list)) else slice(None, None)
               for i in ind]
        result = d.vindex[tuple(slc)]

        # Rotate the expected result accordingly
        axis = _get_axis(ind)
        expected = _vindex_transpose(x[tuple(slc)], axis)

        assert_eq(result, expected)

        # Always have the first axis be the length of the points
        k = len(next(i for i in ind if isinstance(i, (np.ndarray, list))))
        assert result.shape[0] == k
