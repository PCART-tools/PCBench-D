def test_basic_lookup():
    assert_equal('%d %s' % (codata.c, codata.unit('speed of light in vacuum')),
                 '299792458 m s^-1')
