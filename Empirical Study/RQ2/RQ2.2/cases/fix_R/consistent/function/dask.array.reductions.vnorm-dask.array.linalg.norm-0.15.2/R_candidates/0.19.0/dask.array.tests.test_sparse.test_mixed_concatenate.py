@pytest.mark.parametrize('func', functions)
def test_mixed_concatenate(func):
    x = da.random.random((2, 3, 4), chunks=(1, 2, 2))

    y = da.random.random((2, 3, 4), chunks=(1, 2, 2))
    y[y < 0.8] = 0
    yy = y.map_blocks(sparse.COO.from_numpy)

    d = da.concatenate([x, y], axis=0)
    s = da.concatenate([x, yy], axis=0)

    dd = func(d)
    ss = func(s)

    assert_eq(dd, ss)
