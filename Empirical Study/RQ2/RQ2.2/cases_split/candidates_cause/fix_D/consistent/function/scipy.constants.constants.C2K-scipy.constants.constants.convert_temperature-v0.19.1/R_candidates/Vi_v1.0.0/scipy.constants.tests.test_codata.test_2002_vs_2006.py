def test_2002_vs_2006():
    assert_almost_equal(codata.value('magn. flux quantum'),
                        codata.value('mag. flux quantum'))
