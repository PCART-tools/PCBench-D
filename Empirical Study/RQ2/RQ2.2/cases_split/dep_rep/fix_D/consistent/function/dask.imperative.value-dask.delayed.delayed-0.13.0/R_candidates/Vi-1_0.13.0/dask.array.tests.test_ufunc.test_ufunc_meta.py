def test_ufunc_meta():
    assert da.log.__name__ == 'log'
    assert da.log.__doc__.replace('    # doctest: +SKIP', '') == np.log.__doc__

    assert da.modf.__name__ == 'modf'
    assert da.modf.__doc__.replace('    # doctest: +SKIP', '') == np.modf.__doc__

    assert da.frexp.__name__ == 'frexp'
    assert da.frexp.__doc__.replace('    # doctest: +SKIP', '') == np.frexp.__doc__
