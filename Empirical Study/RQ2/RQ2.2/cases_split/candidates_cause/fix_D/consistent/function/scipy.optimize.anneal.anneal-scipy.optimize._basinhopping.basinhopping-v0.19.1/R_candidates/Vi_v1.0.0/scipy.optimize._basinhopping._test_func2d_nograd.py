def _test_func2d_nograd(x):
    f = (cos(14.5 * x[0] - 0.3) + (x[1] + 0.2) * x[1] + (x[0] + 0.2) * x[0]
         + 1.010876184442655)
    return f
