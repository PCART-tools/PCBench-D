def test_chi2_smalldf():
    assert_almost_equal(special.chdtr(0.6,3), 0.957890536704110)
