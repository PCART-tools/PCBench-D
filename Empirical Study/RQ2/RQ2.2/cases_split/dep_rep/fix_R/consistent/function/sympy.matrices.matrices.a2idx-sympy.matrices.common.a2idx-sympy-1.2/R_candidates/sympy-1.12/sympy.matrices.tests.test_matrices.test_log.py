def test_log():
    l = Symbol('lamda')

    m = Matrix.jordan_block(1, l)
    assert m._eval_matrix_log_jblock() == Matrix([[log(l)]])

    m = Matrix.jordan_block(4, l)
    assert m._eval_matrix_log_jblock() == \
        Matrix(
            [
                [log(l), 1/l, -1/(2*l**2), 1/(3*l**3)],
                [0, log(l), 1/l, -1/(2*l**2)],
                [0, 0, log(l), 1/l],
                [0, 0, 0, log(l)]
            ]
        )

    m = Matrix(
        [[0, 0, 1],
        [0, 0, 0],
        [-1, 0, 0]]
    )
    raises(MatrixError, lambda: m.log())
