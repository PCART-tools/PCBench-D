def test_angle():
    real = np.random.randint(1, 100, size=(20, 20))
    imag = np.random.randint(1, 100, size=(20, 20)) * 1j
    comp = real + imag
    dacomp = da.from_array(comp, 3)

    assert_eq(da.angle(dacomp), np.angle(comp))
    assert_eq(da.angle(dacomp, deg=True), np.angle(comp, deg=True))
    assert isinstance(da.angle(comp), np.ndarray)
    assert_eq(da.angle(comp), np.angle(comp))
