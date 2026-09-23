def _drv_moment_gen(self, t, *args):
    t = asarray(t)
    return sum(exp(self.xk * t[newaxis,...]) * self.pk, axis=0)
