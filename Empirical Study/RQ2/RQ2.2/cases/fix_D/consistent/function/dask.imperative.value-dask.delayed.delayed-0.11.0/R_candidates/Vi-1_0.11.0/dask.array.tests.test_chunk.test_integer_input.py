def test_integer_input():
    assert da.zeros((4, 6), chunks=2).rechunk(3).chunks == ((3, 1), (3, 3))
