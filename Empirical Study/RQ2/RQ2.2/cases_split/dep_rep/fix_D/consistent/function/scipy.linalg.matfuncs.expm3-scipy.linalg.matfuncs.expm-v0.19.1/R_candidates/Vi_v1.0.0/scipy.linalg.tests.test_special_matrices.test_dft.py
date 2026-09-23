def test_dft():
    m = dft(2)
    expected = array([[1.0, 1.0], [1.0, -1.0]])
    assert_array_almost_equal(m, expected)
    m = dft(2, scale='n')
    assert_array_almost_equal(m, expected/2.0)
    m = dft(2, scale='sqrtn')
    assert_array_almost_equal(m, expected/sqrt(2.0))

    x = array([0, 1, 2, 3, 4, 5, 0, 1])
    m = dft(8)
    mx = m.dot(x)
    fx = fftpack.fft(x)
    assert_array_almost_equal(mx, fx)
