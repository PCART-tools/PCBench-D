def test_find_single():
    assert_equal(codata.find('Wien freq', disp=False)[0],
                 'Wien frequency displacement law constant')
