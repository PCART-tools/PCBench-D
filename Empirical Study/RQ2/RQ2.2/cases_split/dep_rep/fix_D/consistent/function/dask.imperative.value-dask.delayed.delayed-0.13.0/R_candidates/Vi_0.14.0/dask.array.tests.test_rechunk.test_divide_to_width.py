def test_divide_to_width():
    chunks = divide_to_width((8, 9, 10), 10)
    assert chunks == (8, 9, 10)
    chunks = divide_to_width((8, 2, 9, 10, 11, 12), 4)
    # Note how 9 gives (3, 3, 3), not (4, 4, 1) or whatever
    assert chunks == (4, 4,
                      2,
                      3, 3, 3,
                      3, 3, 4,
                      3, 4, 4,
                      4, 4, 4,
                      )
