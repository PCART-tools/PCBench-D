@pytest.mark.parametrize('ufunc', ['frexp', 'modf'])
def test_ufunc_2results(ufunc):

    dafunc = getattr(da, ufunc)
    npfunc = getattr(np, ufunc)

    arr = np.random.randint(1, 100, size=(20, 20))
    darr = da.from_array(arr, 3)

    # applying Dask ufunc doesn't trigger computation
    res1, res2 = dafunc(darr)
    assert isinstance(res1, da.Array)
    assert isinstance(res2, da.Array)
    exp1, exp2 = npfunc(arr)
    assert_eq(res1, exp1)
    assert_eq(res2, exp2)

    # applying NumPy ufunc triggers computation
    res1, res2 = npfunc(darr)
    assert isinstance(res1, np.ndarray)
    assert isinstance(res2, np.ndarray)
    exp1, exp2 = npfunc(arr)
    assert_eq(res1, exp1)
    assert_eq(res2, exp2)

    # applying Dask ufunc to normal ndarray triggers computation
    res1, res2 = npfunc(darr)
    assert isinstance(res1, np.ndarray)
    assert isinstance(res2, np.ndarray)
    exp1, exp2 = npfunc(arr)
    assert_eq(res1, exp1)
    assert_eq(res2, exp2)
