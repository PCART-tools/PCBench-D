def test_ufunc():
    for attr in ['nin', 'nargs', 'nout', 'ntypes', 'identity',
                 'signature', 'types']:
        assert getattr(da.log, attr) == getattr(np.log, attr)

    with pytest.raises(AttributeError):
        da.log.not_an_attribute

    assert repr(da.log) == repr(np.log)
    assert 'nin' in dir(da.log)
    assert 'outer' in dir(da.log)
