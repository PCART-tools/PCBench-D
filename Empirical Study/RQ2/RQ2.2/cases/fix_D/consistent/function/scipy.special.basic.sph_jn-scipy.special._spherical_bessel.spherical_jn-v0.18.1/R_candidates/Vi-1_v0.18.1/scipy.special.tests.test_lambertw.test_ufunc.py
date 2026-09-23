def test_ufunc():
    assert_array_almost_equal(
        lambertw(r_[0., e, 1.]), r_[0., 1., 0.567143290409783873])
