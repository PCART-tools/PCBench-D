def test_vindex_merge():
    from dask.array.core import _vindex_merge
    locations = [1], [2, 0]
    values = [np.array([[1, 2, 3]]),
              np.array([[10, 20, 30], [40, 50, 60]])]

    assert (_vindex_merge(locations, values) == np.array([[40, 50, 60],
                                                          [1, 2, 3],
                                                          [10, 20, 30]])).all()
