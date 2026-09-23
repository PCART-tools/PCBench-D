def test_sph_harm_ufunc_loop_selection():
    # see https://github.com/scipy/scipy/issues/4895
    dt = np.dtype(np.complex128)
    assert_equal(special.sph_harm(0, 0, 0, 0).dtype, dt)
    assert_equal(special.sph_harm([0], 0, 0, 0).dtype, dt)
    assert_equal(special.sph_harm(0, [0], 0, 0).dtype, dt)
    assert_equal(special.sph_harm(0, 0, [0], 0).dtype, dt)
    assert_equal(special.sph_harm(0, 0, 0, [0]).dtype, dt)
    assert_equal(special.sph_harm([0], [0], [0], [0]).dtype, dt)
