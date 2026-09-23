@slow
def test_eigen_slow():
    # issue 15125
    from sympy.core.function import count_ops
    q = Symbol("q", positive = True)
    m = Matrix([[-2, exp(-q), 1], [exp(q), -2, 1], [1, 1, -2]])
    assert count_ops(m.eigenvals(simplify=False)) > \
        count_ops(m.eigenvals(simplify=True))
    assert count_ops(m.eigenvals(simplify=lambda x: x)) > \
        count_ops(m.eigenvals(simplify=True))
