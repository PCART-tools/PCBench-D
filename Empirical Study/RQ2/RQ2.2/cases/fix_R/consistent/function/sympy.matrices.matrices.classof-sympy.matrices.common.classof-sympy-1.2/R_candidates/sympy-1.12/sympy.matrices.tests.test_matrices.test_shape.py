def test_shape():
    M = Matrix([[x, 0, 0],
                [0, y, 0]])
    assert M.shape == (2, 3)
