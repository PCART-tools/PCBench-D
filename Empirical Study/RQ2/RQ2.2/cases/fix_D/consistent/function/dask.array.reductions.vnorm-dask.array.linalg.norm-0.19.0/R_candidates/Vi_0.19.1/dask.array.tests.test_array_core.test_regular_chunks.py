@pytest.mark.parametrize('data', [[( ), True],
                                  [((1, ),), True],
                                  [((1, 1, 1),), True],
                                  [((1, ), (1, )), True],
                                  [((2, 2, 1), ), True],
                                  [((2, 2, 3), ), False],
                                  [((1, 1, 1), (2, 2, 3)), False],
                                  [((1, 2, 1), ), False]
                                  ])
def test_regular_chunks(data):
    chunkset, expected = data
    assert da.core._check_regular_chunks(chunkset) == expected
