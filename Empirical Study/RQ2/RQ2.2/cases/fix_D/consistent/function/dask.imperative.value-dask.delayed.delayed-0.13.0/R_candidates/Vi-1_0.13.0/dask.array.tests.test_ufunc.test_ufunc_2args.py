@pytest.mark.parametrize('ufunc', ['logaddexp', 'logaddexp2', 'arctan2',
                                   'hypot', 'copysign', 'nextafter', 'ldexp',
                                   'fmod', 'logical_and', 'logical_or',
                                   'logical_xor', 'maximum', 'minimum',
                                   'fmax', 'fmin'])
def test_ufunc_2args(ufunc):

    dafunc = getattr(da, ufunc)
    npfunc = getattr(np, ufunc)

    arr1 = np.random.randint(1, 100, size=(20, 20))
    darr1 = da.from_array(arr1, 3)

    arr2 = np.random.randint(1, 100, size=(20, 20))
    darr2 = da.from_array(arr2, 3)

    # applying Dask ufunc doesn't trigger computation
    assert isinstance(dafunc(darr1, darr2), da.Array)
    assert_eq(dafunc(darr1, darr2), npfunc(arr1, arr2))

    # applying NumPy ufunc triggers computation
    assert isinstance(npfunc(darr1, darr2), np.ndarray)
    assert_eq(npfunc(darr1, darr2), npfunc(arr1, arr2))

    # applying Dask ufunc to normal ndarray triggers computation
    assert isinstance(dafunc(arr1, arr2), np.ndarray)
    assert_eq(dafunc(arr1, arr2), npfunc(arr1, arr2))

    # with scalar
    assert isinstance(dafunc(darr1, 10), da.Array)
    assert_eq(dafunc(darr1, 10), npfunc(arr1, 10))

    assert isinstance(dafunc(10, darr1), da.Array)
    assert_eq(dafunc(10, darr1), npfunc(10, arr1))

    assert isinstance(dafunc(arr1, 10), np.ndarray)
    assert_eq(dafunc(arr1, 10), npfunc(arr1, 10))

    assert isinstance(dafunc(10, arr1), np.ndarray)
    assert_eq(dafunc(10, arr1), npfunc(10, arr1))
