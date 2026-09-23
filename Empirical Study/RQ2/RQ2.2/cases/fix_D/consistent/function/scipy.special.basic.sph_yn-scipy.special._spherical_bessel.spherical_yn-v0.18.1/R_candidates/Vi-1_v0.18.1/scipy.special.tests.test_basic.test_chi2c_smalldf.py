def test_chi2c_smalldf():
    assert_almost_equal(special.chdtrc(0.6,3), 1-0.957890536704110)
