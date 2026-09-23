def test_copy_mutate():
    x = da.arange(5, chunks=(2,))
    y = x.copy()
    memo = {}
    y2 = copy.deepcopy(x, memo=memo)
    x[x % 2 == 0] = -1

    xx = np.arange(5)
    xx[xx % 2 == 0] = -1
    assert_eq(x, xx)

    assert_eq(y, np.arange(5))
    assert_eq(y2, np.arange(5))
    assert memo[id(x)] is y2
