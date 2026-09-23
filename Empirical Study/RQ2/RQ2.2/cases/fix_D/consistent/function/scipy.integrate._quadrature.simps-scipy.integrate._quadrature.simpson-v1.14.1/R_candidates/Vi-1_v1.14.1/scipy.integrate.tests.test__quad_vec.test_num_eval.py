@quadrature_params
def test_num_eval(quadrature):
    def f(x):
        count[0] += 1
        return x**5

    count = [0]
    res = quad_vec(f, 0, 1, norm='max', full_output=True, quadrature=quadrature)
    assert res[2].neval == count[0]
