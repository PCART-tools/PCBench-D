def test_slicing_none_int_ellipes():
    shape = (2,3,5,7,11)
    x = np.arange(np.prod(shape)).reshape(shape)
    y = da.core.asarray(x)
    for ind in itertools.product(indexers, indexers, indexers, indexers):
        if ind.count(Ellipsis) > 1:
            continue

        assert_eq(x[ind], y[ind])
