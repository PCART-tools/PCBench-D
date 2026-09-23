@pytest.mark.parametrize('ufunc', ['isreal', 'iscomplex', 'real', 'imag'])
def test_complex(ufunc):

    dafunc = getattr(da, ufunc)
    npfunc = getattr(np, ufunc)

    real = np.random.randint(1, 100, size=(20, 20))
    imag = np.random.randint(1, 100, size=(20, 20)) * 1j
    comp = real + imag

    dareal = da.from_array(real, 3)
    daimag = da.from_array(imag, 3)
    dacomp = da.from_array(comp, 3)

    assert_eq(dacomp.real, comp.real)
    assert_eq(dacomp.imag, comp.imag)
    assert_eq(dacomp.conj(), comp.conj())

    for darr, arr in [(dacomp, comp), (dareal, real), (daimag, imag)]:
        # applying Dask ufunc doesn't trigger computation
        assert isinstance(dafunc(darr), da.Array)
        assert_eq(dafunc(darr), npfunc(arr))

        # applying NumPy ufunc triggers computation
        assert isinstance(npfunc(darr), np.ndarray)
        assert_eq(npfunc(darr), npfunc(arr))

        # applying Dask ufunc to normal ndarray triggers computation
        assert isinstance(dafunc(arr), np.ndarray)
        assert_eq(dafunc(arr), npfunc(arr))
