def test_basic_table_parse():
    c = 'speed of light in vacuum'
    assert_equal(codata.value(c), constants.c)
    assert_equal(codata.value(c), constants.speed_of_light)
