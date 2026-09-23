def _drv_pmf(self, xk, *args):
    try:
        return self.P[xk]
    except KeyError:
        return 0.0
