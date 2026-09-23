def test_col_join():
    assert eye(3).col_join(Matrix([[7, 7, 7]])) == \
        Matrix([[1, 0, 0],
                [0, 1, 0],
                [0, 0, 1],
                [7, 7, 7]])
