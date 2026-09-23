@pytest.mark.parametrize('ufunc', unary_ufuncs)
def test_unary_ufunc(ufunc):
    if ufunc == 'fix' and np.__version__ >= '1.13.0':
        pytest.skip('fix calls floor in a way that we do not yet support')
    dafunc = getattr(da, ufunc)
    npfunc = getattr(np, ufunc)

    arr = np.random.randint(1, 100, size=(20, 20))
    darr = da.from_array(arr, 3)

    with pytest.warns(None):  # some invalid values (arccos, arcsin, etc.)
        # applying Dask ufunc doesn't trigger computation
        assert isinstance(dafunc(darr), da.Array)
        assert_eq(dafunc(darr), npfunc(arr), equal_nan=True)

    with pytest.warns(None):  # some invalid values (arccos, arcsin, etc.)
        # applying NumPy ufunc is lazy
        if isinstance(npfunc, np.ufunc) and np.__version__ >= '1.13.0':
            assert isinstance(npfunc(darr), da.Array)
        else:
            assert isinstance(npfunc(darr), np.ndarray)
        assert_eq(npfunc(darr), npfunc(arr), equal_nan=True)

    with pytest.warns(None):  # some invalid values (arccos, arcsin, etc.)
        # applying Dask ufunc to normal ndarray triggers computation
        assert isinstance(dafunc(arr), np.ndarray)
        assert_eq(dafunc(arr), npfunc(arr), equal_nan=True)
