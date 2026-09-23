def test_3925():
    x = da.from_array(np.array(['a', 'b', 'c'], dtype=object), chunks=-1)
    assert (x[0] == x[0]).compute(scheduler='sync')
