def test_view():
    x = np.arange(56).reshape((7, 8))
    d = da.from_array(x, chunks=(2, 3))

    assert_eq(x.view('i4'), d.view('i4'))
    assert_eq(x.view('i2'), d.view('i2'))
    assert all(isinstance(s, int) for s in d.shape)

    x = np.arange(8, dtype='i1')
    d = da.from_array(x, chunks=(4,))
    assert_eq(x.view('i4'), d.view('i4'))

    with pytest.raises(ValueError):
        x = np.arange(8, dtype='i1')
        d = da.from_array(x, chunks=(3,))
        d.view('i4')

    with pytest.raises(ValueError):
        d.view('i4', order='asdf')
