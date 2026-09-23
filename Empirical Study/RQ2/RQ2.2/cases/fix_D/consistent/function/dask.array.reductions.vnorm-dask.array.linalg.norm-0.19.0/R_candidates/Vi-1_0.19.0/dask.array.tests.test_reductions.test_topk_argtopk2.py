@pytest.mark.parametrize('npfunc,daskfunc', [
    (np.sort, da.topk),
    (np.argsort, da.argtopk),
])
@pytest.mark.parametrize('split_every', [None, 2, 3, 4])
@pytest.mark.parametrize('chunksize', [1, 2, 3, 4, 5, 10])
def test_topk_argtopk2(npfunc, daskfunc, split_every, chunksize):
    """Fine test use cases when k is larger than chunk size"""
    a = da.random.random((10, ), chunks=chunksize)
    k = 5

    # top 5 elements, sorted descending
    assert_eq(npfunc(a)[-k:][::-1],
              daskfunc(a, k, split_every=split_every))
    # bottom 5 elements, sorted ascending
    assert_eq(npfunc(a)[:k],
              daskfunc(a, -k, split_every=split_every))
