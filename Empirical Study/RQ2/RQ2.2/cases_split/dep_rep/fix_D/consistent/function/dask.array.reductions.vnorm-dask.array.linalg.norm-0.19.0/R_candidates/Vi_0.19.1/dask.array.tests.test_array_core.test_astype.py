def test_astype():
    x = np.ones((5, 5), dtype='f8')
    d = da.from_array(x, chunks=(2,2))

    assert d.astype('i8').dtype == 'i8'
    assert_eq(d.astype('i8'), x.astype('i8'))
    assert same_keys(d.astype('i8'), d.astype('i8'))

    with pytest.raises(TypeError):
        d.astype('i8', casting='safe')

    with pytest.raises(TypeError):
        d.astype('i8', not_a_real_kwarg='foo')

    # smoketest with kwargs
    assert_eq(d.astype('i8', copy=False), x.astype('i8', copy=False))

    # Check it's a noop
    assert d.astype('f8') is d
