@pytest.mark.parametrize('func', functions)
def test_mixed_random(func):
    d = da.random.random((4, 3, 4), chunks=(1, 2, 2))
    d[d < 0.7] = 0

    fn = lambda x: sparse.COO.from_numpy(x) if random.random() < 0.5 else x
    s = d.map_blocks(fn)

    dd = func(d)
    ss = func(s)

    assert_eq(dd, ss)
