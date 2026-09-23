    def grad(x):
        g = zeros(x.shape, float64)
        t1 = x[1] - x[0] ** 2
        g[0] = 2 * (x[0] - 1) - 16 * x[0] * t1
        for i in range(1, g.shape[0] - 1):
            t2 = t1
            t1 = x[i + 1] - x[i] ** 2
            g[i] = 8 * t2 - 16*x[i] * t1
        g[-1] = 8 * t1
        return g
