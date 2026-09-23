@pytest.mark.parametrize('func', functions)
def test_basic(func):
    x = da.random.random((2, 3, 4), chunks=(1, 2, 2))
    x[x < 0.8] = 0

    y = x.map_blocks(sparse.COO.from_numpy)

    xx = func(x)
    yy = func(y)

    assert_eq(xx, yy)

    if yy.shape:
        zz = yy.compute()
        if not isinstance(zz, sparse.COO):
            assert (zz != 1).sum() > np.prod(zz.shape) / 2  # mostly dense
