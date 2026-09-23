def test_to_delayed():
    x = da.random.random((4, 4), chunks=(2, 2))
    y = x + 10

    [[a, b], [c, d]] = y.to_delayed()
    assert_eq(a.compute(), y[:2, :2])

    s = 2
    x = da.from_array(np.array(s), chunks=0)
    a = x.to_delayed()[tuple()]
    assert a.compute() == s
