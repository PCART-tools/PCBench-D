def _drv_moment(self, n, *args):
    n = asarray(n)
    return sum(self.xk**n[newaxis,...] * self.pk, axis=0)
