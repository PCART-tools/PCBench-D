def test_timedelta_op():
    x = np.array([np.timedelta64(10, 'h')])
    y = np.timedelta64(1, 'h')
    a = da.from_array(x, chunks=(1,)) / y
    assert a.compute() == x / y
