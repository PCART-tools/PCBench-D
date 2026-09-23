    def fun(x, r=[4, 2, 4, 2, 1]):
        """ Objective function """
        return exp(x[0]) * (r[0] * x[0]**2 + r[1] * x[1]**2 +
                            r[2] * x[0] * x[1] + r[3] * x[1] +
                            r[4])
