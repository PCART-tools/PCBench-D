@pytest.mark.parametrize('npfunc,daskfunc', [
    (np.sort, da.topk),
    (np.argsort, da.argtopk),
])
@pytest.mark.parametrize('split_every', [None, 2, 4, 8])
def test_topk_argtopk1(npfunc, daskfunc, split_every):
    # Test data
    k = 5
    # Test at least 3 levels of aggregation when split_every=2
    # to stress the different chunk, combine, aggregate kernels
    a = da.random.random(800, chunks=((120, 80, 100, 200, 300), ))
    b = da.random.random((10, 20, 30), chunks=(4, 8, 8))

    # 1-dimensional arrays
    # top 5 elements, sorted descending
    assert_eq(npfunc(a)[-k:][::-1],
              daskfunc(a, k, split_every=split_every))
    # bottom 5 elements, sorted ascending
    assert_eq(npfunc(a)[:k],
              daskfunc(a, -k, split_every=split_every))

    # n-dimensional arrays
    # also testing when k > chunk
    # top 5 elements, sorted descending
    assert_eq(npfunc(b, axis=0)[-k:, :, :][::-1, :, :],
              daskfunc(b, k, axis=0, split_every=split_every))
    assert_eq(npfunc(b, axis=1)[:, -k:, :][:, ::-1, :],
              daskfunc(b, k, axis=1, split_every=split_every))
    assert_eq(npfunc(b, axis=-1)[:, :, -k:][:, :, ::-1],
              daskfunc(b, k, axis=-1, split_every=split_every))
    with pytest.raises(ValueError):
        daskfunc(b, k, axis=3, split_every=split_every)

    # bottom 5 elements, sorted ascending
    assert_eq(npfunc(b, axis=0)[:k, :, :],
              daskfunc(b, -k, axis=0, split_every=split_every))
    assert_eq(npfunc(b, axis=1)[:, :k, :],
              daskfunc(b, -k, axis=1, split_every=split_every))
    assert_eq(npfunc(b, axis=-1)[:, :, :k],
              daskfunc(b, -k, axis=-1, split_every=split_every))
    with pytest.raises(ValueError):
        daskfunc(b, -k, axis=3, split_every=split_every)
