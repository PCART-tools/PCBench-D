def test_view_fortran():
    x = np.asfortranarray(np.arange(64).reshape((8, 8)))
    d = da.from_array(x, chunks=(2, 3))
    assert_eq(x.T.view('i4').T, d.view('i4', order='F'))
    assert_eq(x.T.view('i2').T, d.view('i2', order='F'))
