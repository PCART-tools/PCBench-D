def test_chi2_inv_smalldf():
    assert_almost_equal(special.chdtri(0.6,1-0.957890536704110), 3)
