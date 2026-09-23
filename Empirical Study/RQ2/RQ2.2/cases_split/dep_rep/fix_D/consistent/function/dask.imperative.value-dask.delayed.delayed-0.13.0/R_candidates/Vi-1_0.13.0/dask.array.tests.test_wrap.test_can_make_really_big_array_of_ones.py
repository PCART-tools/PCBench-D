def test_can_make_really_big_array_of_ones():
    ones((1000000, 1000000), chunks=(100000, 100000))
    ones(shape=(1000000, 1000000), chunks=(100000, 100000))
