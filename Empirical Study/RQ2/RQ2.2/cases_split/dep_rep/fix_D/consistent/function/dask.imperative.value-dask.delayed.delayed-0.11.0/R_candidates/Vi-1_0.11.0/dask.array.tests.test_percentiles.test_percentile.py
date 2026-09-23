def test_percentile():
    d = da.ones((16,), chunks=(4,))
    assert eq(da.percentile(d, [0, 50, 100]), [1, 1, 1])

    x = np.array([0, 0, 5, 5, 5, 5, 20, 20])
    d = da.from_array(x, chunks=(3,))
    assert eq(da.percentile(d, [0, 50, 100]), [0, 5, 20])
    assert same_keys(da.percentile(d, [0, 50, 100]),
                    da.percentile(d, [0, 50, 100]))
    assert not same_keys(da.percentile(d, [0, 50, 100]),
                        da.percentile(d, [0, 50]))

    x = np.array(['a', 'a', 'd', 'd', 'd', 'e'])
    d = da.from_array(x, chunks=(3,))
    assert eq(da.percentile(d, [0, 50, 100]), ['a', 'd', 'e'])
