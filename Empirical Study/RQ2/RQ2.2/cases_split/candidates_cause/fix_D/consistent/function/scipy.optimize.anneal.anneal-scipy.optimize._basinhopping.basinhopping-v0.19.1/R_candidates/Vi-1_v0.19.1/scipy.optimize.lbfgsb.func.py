    def func(x):
        f = 0.25 * (x[0] - 1) ** 2
        for i in range(1, x.shape[0]):
            f += (x[i] - x[i-1] ** 2) ** 2
        f *= 4
        return f
